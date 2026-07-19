"""Shared classification/regression metrics used by the evaluation scripts."""
from typing import List

from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, precision_score, recall_score


def classification_metrics(y_true: List, y_pred: List) -> dict:
    return {
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, average="weighted", zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, average="weighted", zero_division=0), 4),
        "f1": round(f1_score(y_true, y_pred, average="weighted", zero_division=0), 4),
    }


def regression_metrics(y_true: List[float], y_pred: List[float]) -> dict:
    return {"mae": round(mean_absolute_error(y_true, y_pred), 4)}
