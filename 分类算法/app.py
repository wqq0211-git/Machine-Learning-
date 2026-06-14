from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from sklearn.datasets import load_breast_cancer


ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
MODELS_DIR = ROOT_DIR / "models"
REPORT_DIR = ROOT_DIR / "report"
FIGURES_DIR = REPORT_DIR / "figures"

DISPLAY_NAME_TO_KEY = {
    "Logistic Regression": "logistic_regression",
    "Random Forest": "random_forest",
    "SVM": "svm",
}

RISK_ACTIONS = {
    "高风险": "建议尽快安排专科复查，并结合影像或病理进一步检查。",
    "中风险": "建议短期复查，并由临床医生结合更多检查结果综合评估。",
    "低风险": "建议常规随访，继续结合医生意见进行后续观察。",
}


def artifacts_ready() -> bool:
    required_paths = [
        MODELS_DIR / "metadata.json",
        MODELS_DIR / "logistic_regression.joblib",
        MODELS_DIR / "random_forest.joblib",
        MODELS_DIR / "svm.joblib",
        REPORT_DIR / "metrics.csv",
        REPORT_DIR / "dataset_summary.json",
    ]
    return all(path.exists() for path in required_paths)


@st.cache_resource
def load_artifacts():
    metadata = json.loads((MODELS_DIR / "metadata.json").read_text(encoding="utf-8"))
    models = {
        model_key: joblib.load(MODELS_DIR / model_file)
        for model_key, model_file in metadata["model_files"].items()
    }
    dataset_summary = json.loads(
        (REPORT_DIR / "dataset_summary.json").read_text(encoding="utf-8")
    )
    return metadata, models, dataset_summary


@st.cache_data
def load_metrics() -> pd.DataFrame:
    return pd.read_csv(REPORT_DIR / "metrics.csv")


@st.cache_data
def load_dataset_frame() -> pd.DataFrame:
    dataset_path = DATA_DIR / "breast_cancer.csv"
    if dataset_path.exists():
        return pd.read_csv(dataset_path)

    dataset = load_breast_cancer(as_frame=True)
    frame = dataset.data.copy()
    frame["target"] = dataset.target
    frame["target_name"] = frame["target"].map(
        lambda value: dataset.target_names[int(value)]
    )
    return frame


def get_recommended_model_key(metrics_df: pd.DataFrame) -> str:
    priority_order = {
        "Logistic Regression": 0,
        "Random Forest": 1,
        "SVM": 2,
    }
    ranked = metrics_df.copy()
    ranked["Priority"] = ranked["Model"].map(priority_order).fillna(99)
    ranked = ranked.sort_values(
        by=["Recall", "AUC", "Accuracy", "Priority"],
        ascending=[False, False, False, True],
    )
    best_display_name = ranked.iloc[0]["Model"]
    return DISPLAY_NAME_TO_KEY[best_display_name]


def get_model_classes(model) -> list[int]:
    if hasattr(model, "classes_"):
        return list(model.classes_)
    estimator = model.named_steps["model"]
    return list(estimator.classes_)


def get_probability_columns(model, feature_frame: pd.DataFrame) -> dict[str, list[float]]:
    probabilities = model.predict_proba(feature_frame)
    classes = get_model_classes(model)
    class_to_index = {int(class_id): index for index, class_id in enumerate(classes)}
    malignant_scores = probabilities[:, class_to_index[0]]
    benign_scores = probabilities[:, class_to_index[1]]
    return {
        "malignant_probability": malignant_scores,
        "benign_probability": benign_scores,
    }


def risk_level_from_probability(
    malignant_probability: float,
    medium_threshold: float,
    high_threshold: float,
) -> str:
    if malignant_probability >= high_threshold:
        return "高风险"
    if malignant_probability >= medium_threshold:
        return "中风险"
    return "低风险"


def get_risk_color(risk_level: str) -> str:
    return {
        "高风险": "#b91c1c",
        "中风险": "#c2410c",
        "低风险": "#166534",
    }.get(risk_level, "#334155")


def get_risk_action(risk_level: str) -> str:
    return RISK_ACTIONS[risk_level]


def build_case_results(
    feature_frame: pd.DataFrame,
    selected_model_keys: list[str],
    models: dict,
    metadata: dict,
    case_ids: list[str],
    medium_threshold: float,
    high_threshold: float,
) -> pd.DataFrame:
    target_names = metadata["target_names"]
    display_names = metadata["model_display_names"]
    rows = []

    for model_key in selected_model_keys:
        model = models[model_key]
        predictions = model.predict(feature_frame)
        probability_columns = get_probability_columns(model, feature_frame)
        malignant_probabilities = probability_columns["malignant_probability"]
        benign_probabilities = probability_columns["benign_probability"]

        for index, class_id in enumerate(predictions):
            malignant_probability = float(malignant_probabilities[index])
            risk_level = risk_level_from_probability(
                malignant_probability,
                medium_threshold,
                high_threshold,
            )
            rows.append(
                {
                    "案例编号": case_ids[index],
                    "模型键": model_key,
                    "模型": display_names[model_key],
                    "预测类别": target_names[int(class_id)],
                    "恶性概率": malignant_probability,
                    "良性概率": float(benign_probabilities[index]),
                    "风险等级": risk_level,
                    "分诊建议": get_risk_action(risk_level),
                }
            )

    result_df = pd.DataFrame(rows)
    return result_df.sort_values(
        by=["案例编号", "恶性概率"],
        ascending=[True, False],
    ).reset_index(drop=True)


def validate_uploaded_frame(
    frame: pd.DataFrame,
    feature_names: list[str],
):
    missing_columns = [name for name in feature_names if name not in frame.columns]
    if missing_columns:
        return None, None, None, f"上传文件缺少字段：{', '.join(missing_columns)}"

    cleaned = frame[feature_names].copy()
    for feature_name in feature_names:
        cleaned[feature_name] = pd.to_numeric(cleaned[feature_name], errors="coerce")

    invalid_columns = [name for name in feature_names if cleaned[name].isna().any()]
    if invalid_columns:
        return (
            None,
            None,
            None,
            f"以下字段包含空值或无法转换为数值的内容：{', '.join(invalid_columns)}",
        )

    extra_columns = [column for column in frame.columns if column not in feature_names]
    preserved_context = frame[extra_columns].copy() if extra_columns else pd.DataFrame(index=frame.index)
    return cleaned, preserved_context, extra_columns, None


def get_case_ids_from_context(context_df: pd.DataFrame | None, row_count: int) -> list[str]:
    if context_df is not None and not context_df.empty:
        priority_columns = [
            "patient_id",
            "case_id",
            "sample_id",
            "id",
            "患者编号",
            "编号",
        ]
        lowered = {column.lower(): column for column in context_df.columns}
        for preferred in priority_columns:
            lookup_key = preferred.lower()
            if lookup_key in lowered:
                column_name = lowered[lookup_key]
                return context_df[column_name].astype(str).fillna("").replace("", pd.NA).fillna(
                    pd.Series(
                        [f"CASE-{index + 1:03d}" for index in range(row_count)],
                        index=context_df.index,
                    )
                ).tolist()
        return [f"CASE-{index + 1:03d}" for index in range(row_count)]
    return [f"CASE-{index + 1:03d}" for index in range(row_count)]


def build_primary_case_summary(
    case_result_df: pd.DataFrame,
    primary_model_key: str,
) -> pd.Series:
    primary_result = case_result_df.loc[
        case_result_df["模型键"] == primary_model_key
    ].iloc[0]
    return primary_result


def summarize_model_consensus(case_result_df: pd.DataFrame) -> tuple[int, int]:
    malignant_votes = int((case_result_df["预测类别"] == "malignant").sum())
    total_votes = int(len(case_result_df))
    return malignant_votes, total_votes


def get_feature_groups(feature_names: list[str]) -> dict[str, list[str]]:
    return {
        "平均值特征": [name for name in feature_names if name.startswith("mean ")],
        "误差特征": [name for name in feature_names if name.endswith(" error")],
        "最差值特征": [name for name in feature_names if name.startswith("worst ")],
    }


def compute_logistic_contributions(
    sample_frame: pd.DataFrame,
    model,
    feature_names: list[str],
    top_n: int,
) -> pd.DataFrame:
    scaler = model.named_steps["scaler"]
    estimator = model.named_steps["model"]
    transformed = scaler.transform(sample_frame[feature_names])[0]
    coefficients = estimator.coef_[0]
    malignant_contributions = -transformed * coefficients

    contribution_df = pd.DataFrame(
        {
            "特征": feature_names,
            "当前值": sample_frame.iloc[0][feature_names].values,
            "恶性风险贡献": malignant_contributions,
        }
    )
    contribution_df["影响方向"] = contribution_df["恶性风险贡献"].apply(
        lambda value: "提高恶性风险" if value >= 0 else "降低恶性风险"
    )
    contribution_df["绝对贡献"] = contribution_df["恶性风险贡献"].abs()
    return contribution_df.sort_values("绝对贡献", ascending=False).head(top_n)


def compute_attention_features(
    sample_frame: pd.DataFrame,
    dataset_frame: pd.DataFrame,
    feature_names: list[str],
    weights: list[float],
    top_n: int,
) -> pd.DataFrame:
    medians = dataset_frame[feature_names].median()
    iqr = dataset_frame[feature_names].quantile(0.75) - dataset_frame[feature_names].quantile(0.25)
    safe_iqr = iqr.replace(0, 1e-9)

    sample_values = sample_frame.iloc[0][feature_names]
    standardized_shift = ((sample_values - medians) / safe_iqr).abs()
    attention_score = standardized_shift * pd.Series(weights, index=feature_names)

    attention_df = pd.DataFrame(
        {
            "特征": feature_names,
            "当前值": sample_values.values,
            "数据集中位数": medians.values,
            "偏离程度": standardized_shift.values,
            "关注分数": attention_score.values,
        }
    )
    attention_df["相对中位数"] = attention_df.apply(
        lambda row: "高于中位数" if row["当前值"] >= row["数据集中位数"] else "低于中位数",
        axis=1,
    )
    return attention_df.sort_values("关注分数", ascending=False).head(top_n)


def render_risk_banner(primary_result: pd.Series) -> None:
    risk_level = primary_result["风险等级"]
    color = get_risk_color(risk_level)
    st.markdown(
        f"""
        <div style="padding:16px 18px;border-radius:8px;background:{color};color:white;">
            <div style="font-size:14px;opacity:0.92;">主模型分诊结论</div>
            <div style="font-size:26px;font-weight:700;margin-top:6px;">{risk_level}</div>
            <div style="font-size:14px;margin-top:8px;line-height:1.6;">{primary_result["分诊建议"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_summary_cards(primary_result: pd.Series, primary_model_name: str) -> None:
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("主模型", primary_model_name)
    col_b.metric("恶性概率", f"{primary_result['恶性概率']:.2%}")
    col_c.metric("良性概率", f"{primary_result['良性概率']:.2%}")
    col_d.metric("预测类别", str(primary_result["预测类别"]))


def render_case_comparison(case_result_df: pd.DataFrame) -> None:
    display_df = case_result_df[
        ["模型", "预测类别", "恶性概率", "良性概率", "风险等级", "分诊建议"]
    ].copy()
    st.dataframe(
        display_df.style.format(
            {
                "恶性概率": "{:.2%}",
                "良性概率": "{:.2%}",
            }
        ),
        use_container_width=True,
    )


def render_consensus_hint(case_result_df: pd.DataFrame) -> None:
    malignant_votes, total_votes = summarize_model_consensus(case_result_df)
    if total_votes <= 1:
        return

    if malignant_votes == total_votes:
        st.error("三模型结论一致：均提示恶性风险，应优先复查。")
    elif malignant_votes == 0:
        st.success("三模型结论一致：均倾向良性，可作为低风险样本处理。")
    else:
        st.warning(
            f"模型结论存在分歧：{malignant_votes}/{total_votes} 个模型提示恶性风险，建议人工重点复核。"
        )


def render_logistic_explanation(
    sample_frame: pd.DataFrame,
    logistic_model,
    feature_names: list[str],
    top_n: int,
) -> None:
    contribution_df = compute_logistic_contributions(
        sample_frame,
        logistic_model,
        feature_names,
        top_n,
    ).sort_values("恶性风险贡献")

    fig, ax = plt.subplots(figsize=(8, 4.8))
    colors = [
        "#b91c1c" if value >= 0 else "#166534"
        for value in contribution_df["恶性风险贡献"]
    ]
    ax.barh(contribution_df["特征"], contribution_df["恶性风险贡献"], color=colors)
    ax.axvline(0, color="#0f172a", linewidth=1)
    ax.set_title("Logistic Regression 局部解释")
    ax.set_xlabel("对恶性风险的贡献")
    ax.set_ylabel("")
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)

    st.dataframe(
        contribution_df[["特征", "当前值", "恶性风险贡献", "影响方向"]].style.format(
            {
                "当前值": "{:.4f}",
                "恶性风险贡献": "{:.4f}",
            }
        ),
        use_container_width=True,
    )


def render_attention_explanation(
    sample_frame: pd.DataFrame,
    dataset_frame: pd.DataFrame,
    feature_names: list[str],
    weights: list[float],
    title: str,
    help_text: str,
    top_n: int,
) -> None:
    attention_df = compute_attention_features(
        sample_frame,
        dataset_frame,
        feature_names,
        weights,
        top_n,
    ).sort_values("关注分数", ascending=True)

    st.caption(help_text)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.barh(attention_df["特征"], attention_df["关注分数"], color="#92400e")
    ax.set_title(title)
    ax.set_xlabel("关注分数")
    ax.set_ylabel("")
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)

    st.dataframe(
        attention_df[["特征", "当前值", "数据集中位数", "偏离程度", "相对中位数"]].style.format(
            {
                "当前值": "{:.4f}",
                "数据集中位数": "{:.4f}",
                "偏离程度": "{:.4f}",
            }
        ),
        use_container_width=True,
    )


def render_case_explanation(
    primary_model_key: str,
    sample_frame: pd.DataFrame,
    dataset_frame: pd.DataFrame,
    feature_names: list[str],
    models: dict,
    top_n: int,
) -> None:
    st.subheader("模型解释与重点关注特征")
    if primary_model_key == "logistic_regression":
        render_logistic_explanation(
            sample_frame,
            models["logistic_regression"],
            feature_names,
            top_n,
        )
        return

    if primary_model_key == "random_forest":
        importances = models["random_forest"].named_steps["model"].feature_importances_
        render_attention_explanation(
            sample_frame,
            dataset_frame,
            feature_names,
            list(importances),
            "Random Forest 重点关注特征",
            "该图结合特征重要性和样本相对中位数偏离程度，用于辅助医生快速定位异常项。",
            top_n,
        )
        return

    logistic_coefficients = (
        models["logistic_regression"].named_steps["model"].coef_[0].copy()
    )
    render_attention_explanation(
        sample_frame,
        dataset_frame,
        feature_names,
        list(abs(logistic_coefficients)),
        "SVM 辅助解释视图",
        "SVM 为非线性模型，局部可解释性较弱。这里借助可解释模型的风险权重与样本偏离程度，给出辅助复核视图。",
        top_n,
    )


def render_overview_tab(
    dataset_frame: pd.DataFrame,
    dataset_summary: dict,
    metrics_df: pd.DataFrame,
    recommended_model_key: str,
    metadata: dict,
) -> None:
    recommended_model_name = metadata["model_display_names"][recommended_model_key]

    st.subheader("应用场景")
    st.markdown(
        """
        本系统面向乳腺癌早筛辅助分诊场景，适用于体检中心、基层门诊或教学演示环境。
        医护人员可输入患者检查特征，系统将输出恶性风险概率、风险等级、分诊建议，并支持批量筛查与高风险样本优先排序。
        """
    )

    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("样本总数", dataset_summary["sample_count"])
    col_b.metric("特征总数", dataset_summary["feature_count"])
    col_c.metric("推荐部署模型", recommended_model_name)
    col_d.metric(
        "推荐模型 Recall",
        f"{metrics_df.loc[metrics_df['Model'] == recommended_model_name, 'Recall'].iloc[0]:.4f}",
    )

    st.info(
        "筛查场景优先关注 Recall（召回率），因为漏诊代价通常高于误报代价。当前系统默认优先推荐 Recall 与 AUC 综合表现较优的模型。"
    )

    st.subheader("类别分布")
    class_distribution_df = (
        pd.Series(dataset_summary["class_distribution"], name="数量")
        .rename_axis("类别")
        .reset_index()
    )
    st.bar_chart(class_distribution_df, x="类别", y="数量")

    st.subheader("核心工作流")
    st.markdown(
        """
        1. 输入单个病例特征，完成即时风险分诊。  
        2. 上传批量病例 CSV，生成高风险优先处理队列。  
        3. 查看模型解释与重点关注特征，辅助医生复核。  
        4. 在模型中心对比三种算法的效果与图表。  
        """
    )

    st.subheader("关键字段预览")
    preview_columns = [*dataset_summary["feature_names"][:8], "target_name"]
    st.dataframe(dataset_frame[preview_columns].head(10), use_container_width=True)


def render_manual_case_input(
    dataset_frame: pd.DataFrame,
    feature_names: list[str],
) -> tuple[str, pd.DataFrame] | tuple[None, None]:
    defaults = dataset_frame[feature_names].median()
    feature_groups = get_feature_groups(feature_names)

    with st.form("single_case_form"):
        case_id = st.text_input("病例编号", value="CASE-001")
        st.caption("默认值使用数据集各特征中位数，输入结果仅用于教学演示，不替代医生诊断。")
        for group_name, group_features in feature_groups.items():
            with st.expander(group_name, expanded=(group_name == "平均值特征")):
                columns = st.columns(2)
                for index, feature_name in enumerate(group_features):
                    with columns[index % 2]:
                        st.number_input(
                            feature_name,
                            value=float(defaults[feature_name]),
                            format="%.6f",
                            key=f"manual_{feature_name}",
                        )
        submitted = st.form_submit_button("生成分诊结论", use_container_width=True)

    if not submitted:
        return None, None

    values = {
        feature_name: st.session_state[f"manual_{feature_name}"]
        for feature_name in feature_names
    }
    feature_frame = pd.DataFrame([values], columns=feature_names)
    return case_id or "CASE-001", feature_frame


def render_single_case_tab(
    dataset_frame: pd.DataFrame,
    metadata: dict,
    models: dict,
    primary_model_key: str,
    compare_model_keys: list[str],
    medium_threshold: float,
    high_threshold: float,
    top_n_features: int,
) -> None:
    st.subheader("单例分诊")
    feature_names = metadata["feature_names"]

    case_id, feature_frame = render_manual_case_input(dataset_frame, feature_names)
    if feature_frame is None:
        st.caption("填写病例特征后点击“生成分诊结论”，系统会给出风险等级与分诊建议。")
        return

    case_results = build_case_results(
        feature_frame,
        compare_model_keys,
        models,
        metadata,
        [case_id],
        medium_threshold,
        high_threshold,
    )
    primary_result = build_primary_case_summary(case_results, primary_model_key)

    render_risk_banner(primary_result)
    st.write("")
    render_summary_cards(primary_result, metadata["model_display_names"][primary_model_key])
    st.write("")

    if len(compare_model_keys) > 1:
        render_consensus_hint(case_results)
        st.subheader("模型对比")
        render_case_comparison(case_results)

    render_case_explanation(
        primary_model_key,
        feature_frame,
        dataset_frame,
        feature_names,
        models,
        top_n_features,
    )


def render_batch_screening_tab(
    dataset_frame: pd.DataFrame,
    metadata: dict,
    models: dict,
    primary_model_key: str,
    compare_model_keys: list[str],
    medium_threshold: float,
    high_threshold: float,
) -> None:
    st.subheader("批量筛查")
    feature_names = metadata["feature_names"]
    sample_csv = dataset_frame[feature_names].head(8).to_csv(index=False).encode("utf-8-sig")

    col_a, col_b = st.columns([1, 1.2])
    with col_a:
        st.download_button(
            "下载示例 CSV",
            data=sample_csv,
            file_name="breast_cancer_screening_template.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_b:
        uploaded_file = st.file_uploader("上传待筛查 CSV", type=["csv"])

    if uploaded_file is None:
        st.caption("上传包含 30 个特征字段的 CSV 后，系统会自动生成分诊队列并按恶性概率排序。")
        return

    uploaded_df = pd.read_csv(uploaded_file)
    feature_frame, context_df, extra_columns, error_message = validate_uploaded_frame(
        uploaded_df,
        feature_names,
    )
    if error_message:
        st.error(error_message)
        return

    if extra_columns:
        st.warning("已保留但不参与建模的附加字段：" + ", ".join(extra_columns))

    case_ids = get_case_ids_from_context(context_df, len(feature_frame))
    batch_results = build_case_results(
        feature_frame,
        compare_model_keys,
        models,
        metadata,
        case_ids,
        medium_threshold,
        high_threshold,
    )

    primary_queue = (
        batch_results.loc[batch_results["模型键"] == primary_model_key]
        .copy()
        .sort_values("恶性概率", ascending=False)
        .reset_index(drop=True)
    )

    if context_df is not None and not context_df.empty:
        primary_queue = pd.concat(
            [context_df.reset_index(drop=True), primary_queue.reset_index(drop=True)],
            axis=1,
        )

    total_cases = len(primary_queue)
    high_risk_cases = int((primary_queue["风险等级"] == "高风险").sum())
    medium_risk_cases = int((primary_queue["风险等级"] == "中风险").sum())
    low_risk_cases = int((primary_queue["风险等级"] == "低风险").sum())

    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("批量样本数", total_cases)
    col_b.metric("高风险", high_risk_cases)
    col_c.metric("中风险", medium_risk_cases)
    col_d.metric("低风险", low_risk_cases)

    st.subheader("优先处理队列")
    queue_columns = [
        column
        for column in [
            "案例编号",
            "模型",
            "预测类别",
            "恶性概率",
            "良性概率",
            "风险等级",
            "分诊建议",
        ]
        if column in primary_queue.columns
    ]
    leading_columns = [
        column
        for column in primary_queue.columns
        if column not in queue_columns and column not in {"模型键"}
    ]
    display_queue = primary_queue[leading_columns + queue_columns].copy()
    st.dataframe(
        display_queue.style.format(
            {
                "恶性概率": "{:.2%}",
                "良性概率": "{:.2%}",
            }
        ),
        use_container_width=True,
    )
    st.download_button(
        "下载批量筛查结果",
        data=display_queue.to_csv(index=False).encode("utf-8-sig"),
        file_name="screening_results.csv",
        mime="text/csv",
        use_container_width=True,
    )

    if len(compare_model_keys) > 1:
        disagreement_summary = (
            batch_results.pivot_table(
                index="案例编号",
                columns="模型",
                values="预测类别",
                aggfunc="first",
            )
            .reset_index()
        )
        prediction_columns = [column for column in disagreement_summary.columns if column != "案例编号"]
        disagreement_summary["是否存在分歧"] = disagreement_summary[prediction_columns].nunique(axis=1) > 1
        disagreement_cases = disagreement_summary.loc[disagreement_summary["是否存在分歧"]].copy()
        st.subheader("模型分歧样本")
        if disagreement_cases.empty:
            st.success("当前批量样本中，已选模型没有出现预测分歧。")
        else:
            st.warning(f"共有 {len(disagreement_cases)} 个样本存在模型分歧，建议人工重点复核。")
            st.dataframe(disagreement_cases, use_container_width=True)


def render_model_center_tab(
    metrics_df: pd.DataFrame,
    recommended_model_key: str,
    metadata: dict,
) -> None:
    st.subheader("模型中心")
    recommended_model_name = metadata["model_display_names"][recommended_model_key]
    st.success(f"当前推荐部署模型：{recommended_model_name}")

    display_df = metrics_df.copy()
    display_df["部署建议"] = display_df["Model"].apply(
        lambda value: "推荐部署" if value == recommended_model_name else "研究对比"
    )
    st.dataframe(
        display_df.style.format(
            {
                "Accuracy": "{:.4f}",
                "Precision": "{:.4f}",
                "Recall": "{:.4f}",
                "F1-score": "{:.4f}",
                "AUC": "{:.4f}",
            }
        ),
        use_container_width=True,
    )

    st.info(
        "乳腺癌早筛系统通常更看重 Recall 和 AUC：Recall 越高，越能减少高风险样本被漏掉的概率；AUC 越高，模型整体区分能力越强。"
    )

    figure_paths = [
        ("指标对比", FIGURES_DIR / "metrics_comparison.png"),
        ("ROC 曲线", FIGURES_DIR / "roc_curves.png"),
        ("Random Forest 特征重要性", FIGURES_DIR / "random_forest_feature_importance.png"),
        ("Logistic Regression 系数解释", FIGURES_DIR / "logistic_regression_coefficients.png"),
        ("Logistic Regression 混淆矩阵", FIGURES_DIR / "logistic_regression_confusion_matrix.png"),
        ("Random Forest 混淆矩阵", FIGURES_DIR / "random_forest_confusion_matrix.png"),
        ("SVM 混淆矩阵", FIGURES_DIR / "svm_confusion_matrix.png"),
    ]

    for title, path in figure_paths:
        if path.exists():
            st.subheader(title)
            st.image(str(path), use_container_width=True)


def main() -> None:
    st.set_page_config(
        page_title="乳腺癌早筛辅助分诊系统",
        page_icon="🩺",
        layout="wide",
    )
    st.title("乳腺癌早筛辅助分诊系统")
    st.caption("面向机器学习课程大作业的真实场景化演示系统")
    st.warning("本系统仅用于教学演示与算法对比，不替代医生诊断意见。")

    if not artifacts_ready():
        st.error("未找到完整模型产物，请先在项目根目录运行训练脚本。")
        st.code("python src/train.py", language="bash")
        st.stop()

    metadata, models, dataset_summary = load_artifacts()
    metrics_df = load_metrics()
    dataset_frame = load_dataset_frame()
    recommended_model_key = get_recommended_model_key(metrics_df)

    st.sidebar.header("筛查配置")
    primary_model_key = st.sidebar.selectbox(
        "主模型",
        options=list(metadata["model_display_names"].keys()),
        format_func=lambda key: metadata["model_display_names"][key],
        index=list(metadata["model_display_names"].keys()).index(recommended_model_key),
    )
    compare_mode = st.sidebar.checkbox("开启三模型对比", value=True)
    if compare_mode:
        compare_model_keys = list(metadata["model_display_names"].keys())
    else:
        compare_model_keys = [primary_model_key]

    medium_threshold = st.sidebar.slider("中风险阈值", 0.10, 0.90, 0.35, 0.01)
    default_high_threshold = max(0.70, medium_threshold + 0.10)
    high_threshold = st.sidebar.slider(
        "高风险阈值",
        min_value=medium_threshold + 0.05,
        max_value=0.99,
        value=min(default_high_threshold, 0.90),
        step=0.01,
    )
    top_n_features = st.sidebar.slider("解释区展示特征数", 5, 10, 6, 1)

    st.sidebar.markdown("---")
    st.sidebar.success(
        f"推荐部署模型：{metadata['model_display_names'][recommended_model_key]}"
    )
    st.sidebar.caption(
        "默认按 Recall、AUC 和 Accuracy 综合排序，更适合筛查场景。"
    )

    overview_tab, single_case_tab, batch_tab, model_center_tab = st.tabs(
        ["场景总览", "单例分诊", "批量筛查", "模型中心"]
    )
    with overview_tab:
        render_overview_tab(
            dataset_frame,
            dataset_summary,
            metrics_df,
            recommended_model_key,
            metadata,
        )
    with single_case_tab:
        render_single_case_tab(
            dataset_frame,
            metadata,
            models,
            primary_model_key,
            compare_model_keys,
            medium_threshold,
            high_threshold,
            top_n_features,
        )
    with batch_tab:
        render_batch_screening_tab(
            dataset_frame,
            metadata,
            models,
            primary_model_key,
            compare_model_keys,
            medium_threshold,
            high_threshold,
        )
    with model_center_tab:
        render_model_center_tab(metrics_df, recommended_model_key, metadata)


if __name__ == "__main__":
    main()
