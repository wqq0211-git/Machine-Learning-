from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from evaluate import (
    METRIC_COLUMNS,
    evaluate_classifier,
    plot_confusion_matrix,
    plot_feature_importance,
    plot_logistic_coefficients,
    plot_metrics_comparison,
    plot_roc_curves,
)
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
MODELS_DIR = ROOT_DIR / "models"
REPORT_DIR = ROOT_DIR / "report"
FIGURES_DIR = REPORT_DIR / "figures"

RANDOM_STATE = 42
TEST_SIZE = 0.2

MODEL_DISPLAY_NAMES = {
    "logistic_regression": "Logistic Regression",
    "random_forest": "Random Forest",
    "svm": "SVM",
}


def ensure_directories() -> None:
    for path in [DATA_DIR, MODELS_DIR, REPORT_DIR, FIGURES_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def build_models() -> dict[str, Pipeline]:
    return {
        "logistic_regression": Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        max_iter=5000,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=300,
                        random_state=RANDOM_STATE,
                        class_weight="balanced",
                    ),
                )
            ]
        ),
        "svm": Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "model",
                    SVC(
                        kernel="rbf",
                        probability=True,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
    }


def load_dataset() -> tuple[pd.DataFrame, pd.Series, list[str], list[str]]:
    dataset = load_breast_cancer(as_frame=True)
    features = dataset.data
    target = dataset.target
    feature_names = list(dataset.feature_names)
    target_names = list(dataset.target_names)

    export_df = features.copy()
    export_df["target"] = target
    export_df["target_name"] = target.map(lambda value: target_names[int(value)])
    export_df.to_csv(DATA_DIR / "breast_cancer.csv", index=False, encoding="utf-8-sig")

    return features, target, feature_names, target_names


def save_dataset_summary(
    features: pd.DataFrame,
    target: pd.Series,
    feature_names: list[str],
    target_names: list[str],
) -> None:
    class_counts = target.value_counts().sort_index()
    summary = {
        "dataset_name": "Breast Cancer Wisconsin (Diagnostic)",
        "dataset_source": "sklearn.datasets.load_breast_cancer",
        "sample_count": int(features.shape[0]),
        "feature_count": int(features.shape[1]),
        "target_names": target_names,
        "feature_names": feature_names,
        "class_distribution": {
            target_names[int(class_id)]: int(count)
            for class_id, count in class_counts.items()
        },
    }
    (REPORT_DIR / "dataset_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def save_metadata(feature_names: list[str], target_names: list[str]) -> None:
    metadata = {
        "dataset_name": "Breast Cancer Wisconsin (Diagnostic)",
        "dataset_source": "sklearn.datasets.load_breast_cancer",
        "feature_names": feature_names,
        "target_names": target_names,
        "model_display_names": MODEL_DISPLAY_NAMES,
        "model_files": {
            model_key: f"{model_key}.joblib"
            for model_key in MODEL_DISPLAY_NAMES
        },
        "metrics_file": "report/metrics.csv",
        "figures_dir": "report/figures",
    }
    (MODELS_DIR / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    ensure_directories()
    features, target, feature_names, target_names = load_dataset()
    save_dataset_summary(features, target, feature_names, target_names)

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=target,
    )

    models = build_models()
    metrics_rows = []
    roc_records = []

    for model_key, model in models.items():
        display_name = MODEL_DISPLAY_NAMES[model_key]
        print(f"Training {display_name}...")
        model.fit(x_train, y_train)

        metrics, predictions, scores = evaluate_classifier(model, x_test, y_test)
        metrics_rows.append(
            {
                "ModelKey": model_key,
                "Model": display_name,
                **metrics,
            }
        )
        roc_records.append(
            {
                "model": display_name,
                "target": y_test,
                "scores": scores,
            }
        )

        joblib.dump(model, MODELS_DIR / f"{model_key}.joblib")
        plot_confusion_matrix(
            y_test,
            predictions,
            target_names,
            f"{display_name} Confusion Matrix",
            FIGURES_DIR / f"{model_key}_confusion_matrix.png",
        )

    metrics_df = pd.DataFrame(metrics_rows)
    metrics_df = metrics_df[["ModelKey", "Model", *METRIC_COLUMNS]]
    metrics_df.to_csv(REPORT_DIR / "metrics.csv", index=False, encoding="utf-8-sig")

    plot_metrics_comparison(metrics_df, FIGURES_DIR / "metrics_comparison.png")
    plot_roc_curves(roc_records, FIGURES_DIR / "roc_curves.png")

    random_forest = models["random_forest"].named_steps["model"]
    plot_feature_importance(
        feature_names,
        random_forest.feature_importances_,
        FIGURES_DIR / "random_forest_feature_importance.png",
    )

    logistic_regression = models["logistic_regression"].named_steps["model"]
    plot_logistic_coefficients(
        feature_names,
        logistic_regression.coef_[0],
        FIGURES_DIR / "logistic_regression_coefficients.png",
    )

    save_metadata(feature_names, target_names)

    print("\nTraining complete. Metrics:")
    print(metrics_df.to_string(index=False))
    print(f"\nModels saved to: {MODELS_DIR}")
    print(f"Reports saved to: {REPORT_DIR}")


if __name__ == "__main__":
    main()
