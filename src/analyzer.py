"""Leakage-aware train/test evaluation for anomaly detection."""
from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

REQUIRED_COLUMNS = [
    "protocol",
    "destination_port",
    "packet_count",
    "bytes_sent",
    "duration_seconds",
]
LABEL_COLUMN = "synthetic_label"
NUMERIC_COLUMNS = [
    "destination_port",
    "packet_count",
    "bytes_sent",
    "duration_seconds",
]
CATEGORICAL_COLUMNS = ["protocol"]

@dataclass
class AnalysisResult:
    scored_data: pd.DataFrame
    evaluation: dict | None
    train_rows: int
    test_rows: int

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError("الأعمدة التالية غير موجودة: " + ", ".join(missing))

    clean = df.copy()
    clean["protocol"] = clean["protocol"].astype("string").fillna("UNKNOWN").str.upper()
    for column in NUMERIC_COLUMNS:
        clean[column] = pd.to_numeric(clean[column], errors="coerce")
    clean = clean.dropna(subset=NUMERIC_COLUMNS)
    if clean.empty:
        raise ValueError("لا توجد سجلات صالحة بعد تنظيف القيم غير الرقمية.")
    if (clean[["destination_port", "packet_count", "bytes_sent"]] < 0).any().any():
        raise ValueError("لا ينبغي أن تكون المنافذ أو أعداد الحزم أو البايتات سالبة.")
    if LABEL_COLUMN in clean.columns:
        clean[LABEL_COLUMN] = pd.to_numeric(clean[LABEL_COLUMN], errors="coerce")
    return clean.reset_index(drop=True)

def build_model(contamination: float = 0.10, random_state: int = 42) -> Pipeline:
    preprocess = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), NUMERIC_COLUMNS),
            ("protocol", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLUMNS),
        ],
        remainder="drop",
    )
    detector = IsolationForest(
        n_estimators=250,
        contamination=contamination,
        random_state=random_state,
    )
    return Pipeline([("preprocess", preprocess), ("detector", detector)])

def _evaluate(y_true: pd.Series, y_pred: pd.Series) -> dict:
    return {
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist(),
        "classification_report": classification_report(
            y_true, y_pred,
            labels=[0, 1],
            target_names=["Normal (0)", "Unusual (1)"],
            output_dict=True,
            zero_division=0,
        ),
    }

def analyze_data(
    df: pd.DataFrame,
    contamination: float = 0.10,
    test_size: float = 0.25,
    random_state: int = 42,
) -> AnalysisResult:
    clean = validate_data(df)
    features = clean[REQUIRED_COLUMNS].copy()

    has_labels = LABEL_COLUMN in clean.columns and clean[LABEL_COLUMN].isin([0, 1]).all() and clean[LABEL_COLUMN].nunique() == 2
    evaluation = None
    train_rows = len(clean)
    test_rows = 0

    if has_labels:
        labels = clean[LABEL_COLUMN].astype(int)
        train_idx, test_idx = train_test_split(
            clean.index,
            test_size=test_size,
            random_state=random_state,
            stratify=labels,
        )
        # Train only on the training split; labels are not model features.
        model = build_model(contamination=contamination, random_state=random_state)
        model.fit(features.loc[train_idx])

        test_predictions = (model.predict(features.loc[test_idx]) == -1).astype(int)
        evaluation = _evaluate(labels.loc[test_idx], pd.Series(test_predictions, index=test_idx))
        train_rows, test_rows = len(train_idx), len(test_idx)

        # Refit a separate model on all records only for interactive scoring of the table.
        # The metrics above remain from the held-out test split.
        display_model = build_model(contamination=contamination, random_state=random_state)
        display_model.fit(features)
        predictions = (display_model.predict(features) == -1)
        scores = display_model.decision_function(features)
    else:
        # For unlabeled uploads, no supervised-style evaluation is possible.
        display_model = build_model(contamination=contamination, random_state=random_state)
        display_model.fit(features)
        predictions = display_model.predict(features) == -1
        scores = display_model.decision_function(features)
        model = display_model

    scored = clean.copy()
    scored["anomaly"] = predictions
    scored["anomaly_score"] = scores
    scored["status"] = scored["anomaly"].map({True: "غير معتاد", False: "طبيعي"})
    return AnalysisResult(scored_data=scored, evaluation=evaluation, train_rows=train_rows, test_rows=test_rows)
