from __future__ import annotations

from pathlib import Path

import torch
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

from training.config import CIFAR10_MEAN, CIFAR10_STD, IMAGENET_MEAN, IMAGENET_STD


def get_train_transform(model_name: str) -> transforms.Compose:
    if model_name == "cnn":
        return transforms.Compose([
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(CIFAR10_MEAN, CIFAR10_STD),
        ])
    if model_name == "resnet18":
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ])
    raise ValueError(f"Unsupported model_name: {model_name}")


def get_eval_transform(model_name: str) -> transforms.Compose:
    if model_name == "cnn":
        return transforms.Compose([
            transforms.Resize((32, 32)),
            transforms.ToTensor(),
            transforms.Normalize(CIFAR10_MEAN, CIFAR10_STD),
        ])
    if model_name == "resnet18":
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ])
    raise ValueError(f"Unsupported model_name: {model_name}")


def create_dataloaders(
    model_name: str,
    data_dir: str | Path,
    batch_size: int,
    num_workers: int = 0,
    seed: int = 42,
    download: bool = True,
) -> tuple[DataLoader, DataLoader, DataLoader]:
    data_path = Path(data_dir)
    generator = torch.Generator().manual_seed(seed)
    train_full = datasets.CIFAR10(root=data_path, train=True, download=download, transform=get_train_transform(model_name))
    val_source = datasets.CIFAR10(root=data_path, train=True, download=False, transform=get_eval_transform(model_name))
    test_set = datasets.CIFAR10(root=data_path, train=False, download=download, transform=get_eval_transform(model_name))

    train_size = int(len(train_full) * 0.9)
    val_size = len(train_full) - train_size
    train_set, _ = random_split(train_full, [train_size, val_size], generator=generator)
    _, val_set = random_split(val_source, [train_size, val_size], generator=torch.Generator().manual_seed(seed))

    loader_kwargs = {"batch_size": batch_size, "num_workers": num_workers, "pin_memory": torch.cuda.is_available()}
    return (
        DataLoader(train_set, shuffle=True, **loader_kwargs),
        DataLoader(val_set, shuffle=False, **loader_kwargs),
        DataLoader(test_set, shuffle=False, **loader_kwargs),
    )
