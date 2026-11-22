"""Metrik evaluasi bersama untuk semua model NYC Taxi Demand 2026.

Regresi / time series: MAE, RMSE, WAPE, MASE (+ R2).
Klasifikasi: accuracy, precision, recall, macro-F1, confusion matrix.

Semua fungsi nerima array-like (list / numpy / pandas Series).
"""

import numpy as np


def _arr(x):
    return np.asarray(x, dtype=float)


def mae(y_true, y_pred):
    y_true, y_pred = _arr(y_true), _arr(y_pred)
    return float(np.mean(np.abs(y_true - y_pred)))


def rmse(y_true, y_pred):
    y_true, y_pred = _arr(y_true), _arr(y_pred)
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def wape(y_true, y_pred):
    """Weighted Absolute Percentage Error = sum|err| / sum|aktual|."""
    y_true, y_pred = _arr(y_true), _arr(y_pred)
    denom = np.sum(np.abs(y_true))
    if denom == 0:
        return float("nan")
    return float(np.sum(np.abs(y_true - y_pred)) / denom)


def r2(y_true, y_pred):
    y_true, y_pred = _arr(y_true), _arr(y_pred)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0:
        return float("nan")
    return float(1 - ss_res / ss_tot)


def mase_scale(y_train, lag_train):
    """Pembagi MASE: rata-rata |aktual - seasonal naive| di data training."""
    return float(np.mean(np.abs(_arr(y_train) - _arr(lag_train))))


def mase(y_true, y_pred, scale):
    if scale == 0 or np.isnan(scale):
        return float("nan")
    return float(mae(y_true, y_pred) / scale)


def regression_metrics(y_true, y_pred, scale=None):
    """Kumpulkan metrik regresi jadi dict. `scale` = mase_scale() dari training."""
    out = {
        "mae": mae(y_true, y_pred),
        "rmse": rmse(y_true, y_pred),
        "wape": wape(y_true, y_pred),
        "r2": r2(y_true, y_pred),
    }
    out["mase"] = mase(y_true, y_pred, scale) if scale is not None else float("nan")
    return out


def confusion_matrix(y_true, y_pred, labels=None):
    """Confusion matrix (baris = aktual, kolom = prediksi)."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    if labels is None:
        labels = sorted(set(y_true) | set(y_pred))
    label_to_idx = {lab: i for i, lab in enumerate(labels)}
    cm = np.zeros((len(labels), len(labels)), dtype=int)
    for t, p in zip(y_true, y_pred):
        if t in label_to_idx and p in label_to_idx:
            cm[label_to_idx[t], label_to_idx[p]] += 1
    return cm, list(labels)


def classification_metrics(y_true, y_pred, labels=None):
    """Accuracy + macro precision/recall/F1, plus confusion matrix."""
    cm, labels = confusion_matrix(y_true, y_pred, labels)
    total = cm.sum()
    accuracy = float(np.trace(cm) / total) if total else float("nan")

    precision, recall, f1 = [], [], []
    for i in range(len(labels)):
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp
        p = tp / (tp + fp) if (tp + fp) else 0.0
        r = tp / (tp + fn) if (tp + fn) else 0.0
        f = 2 * p * r / (p + r) if (p + r) else 0.0
        precision.append(p)
        recall.append(r)
        f1.append(f)

    return {
        "accuracy": accuracy,
        "precision_macro": float(np.mean(precision)),
        "recall_macro": float(np.mean(recall)),
        "f1_macro": float(np.mean(f1)),
        "confusion": cm,
        "labels": labels,
    }
