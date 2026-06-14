from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    auc,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)


METRIC_COLUMNS = ["Accuracy", "Precision", "Recall", "F1-score", "AUC"]


def get_positive_scores(model, features):
    if hasattr(model, "predict_proba"):
        return model.predict_proba(features)[:, 1]
    if hasattr(model, "decision_function"):
        return model.decision_function(features)
    raise ValueError("The model must provide predict_proba or decision_function.")


def evaluate_classifier(model, features, target):
    predictions = model.predict(features)
    scores = get_positive_scores(model, features)
    metrics = {
        "Accuracy": accuracy_score(target, predictions),
        "Precision": precision_score(target, predictions, zero_division=0),
        "Recall": recall_score(target, predictions, zero_division=0),
        "F1-score": f1_score(target, predictions, zero_division=0),
        "AUC": roc_auc_score(target, scores),
    }
    return metrics, predictions, scores


def plot_metrics_comparison(metrics_df: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.6))
    plot_df = metrics_df.set_index("Model")[METRIC_COLUMNS]
    plot_df.plot(kind="bar", ax=ax, width=0.78)
    ax.set_title("Classification Metrics Comparison")
    ax.set_xlabel("Model")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="lower right", ncol=2)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_confusion_matrix(
    target,
    predictions,
    target_names,
    title: str,
    output_path: Path,
) -> None:
    matrix = confusion_matrix(target, predictions)
    fig, ax = plt.subplots(figsize=(5.4, 4.8))
    sns.heatmap(
        matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        xticklabels=target_names,
        yticklabels=target_names,
        ax=ax,
    )
    ax.set_title(title)
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("True label")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_roc_curves(roc_records: list[dict], output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    for record in roc_records:
        false_positive_rate, true_positive_rate, _ = roc_curve(
            record["target"],
            record["scores"],
        )
        roc_auc = auc(false_positive_rate, true_positive_rate)
        ax.plot(
            false_positive_rate,
            true_positive_rate,
            linewidth=2,
            label=f"{record['model']} (AUC={roc_auc:.3f})",
        )
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray", linewidth=1)
    ax.set_title("ROC Curves")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.grid(alpha=0.25)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_feature_importance(
    feature_names,
    importances,
    output_path: Path,
    top_n: int = 10,
) -> None:
    importance_df = (
        pd.DataFrame({"Feature": feature_names, "Importance": importances})
        .sort_values("Importance", ascending=False)
        .head(top_n)
        .sort_values("Importance", ascending=True)
    )
    fig, ax = plt.subplots(figsize=(8, 5.8))
    ax.barh(importance_df["Feature"], importance_df["Importance"], color="#4C78A8")
    ax.set_title(f"Random Forest Top {top_n} Feature Importances")
    ax.set_xlabel("Importance")
    ax.set_ylabel("")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_logistic_coefficients(
    feature_names,
    coefficients,
    output_path: Path,
    top_n: int = 10,
) -> None:
    coefficient_df = pd.DataFrame(
        {
            "Feature": feature_names,
            "Coefficient": coefficients,
            "AbsCoefficient": abs(coefficients),
        }
    )
    coefficient_df = (
        coefficient_df.sort_values("AbsCoefficient", ascending=False)
        .head(top_n)
        .sort_values("Coefficient", ascending=True)
    )
    colors = ["#D95F02" if value < 0 else "#1B9E77" for value in coefficient_df["Coefficient"]]
    fig, ax = plt.subplots(figsize=(8, 5.8))
    ax.barh(coefficient_df["Feature"], coefficient_df["Coefficient"], color=colors)
    ax.axvline(0, color="black", linewidth=1)
    ax.set_title(f"Logistic Regression Top {top_n} Coefficients")
    ax.set_xlabel("Coefficient")
    ax.set_ylabel("")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
