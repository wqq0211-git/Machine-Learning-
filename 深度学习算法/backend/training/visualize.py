from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from training.config import backend_dir
from training.utils import read_json


def plot_history(model_name: str, history: list[dict], figures_dir: Path) -> None:
    if not history:
        print(f"No training history for {model_name}.")
        return
    epochs = [row["epoch"] for row in history]
    plt.figure()
    plt.plot(epochs, [row["train_loss"] for row in history], label="train loss")
    plt.plot(epochs, [row["val_loss"] for row in history], label="val loss")
    plt.title(f"{model_name} Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / f"{model_name}_loss.png")
    plt.close()

    plt.figure()
    plt.plot(epochs, [row["train_accuracy"] for row in history], label="train acc")
    plt.plot(epochs, [row["val_accuracy"] for row in history], label="val acc")
    plt.title(f"{model_name} Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / f"{model_name}_accuracy.png")
    plt.close()


def main() -> None:
    root = backend_dir()
    figures = root / "results" / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    history = read_json(root / "results" / "training_history.json", {"cnn": [], "resnet18": []})
    for model_name in ("cnn", "resnet18"):
        plot_history(model_name, history.get(model_name, []), figures)
    print(f"Figures saved to {figures}")


if __name__ == "__main__":
    main()

