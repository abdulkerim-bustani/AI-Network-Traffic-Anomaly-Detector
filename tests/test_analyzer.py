import pandas as pd
import pytest
from src.analyzer import analyze_data, validate_data
from src.generate_data import generate_dataset

def test_generated_dataset_has_expected_size_and_overlap():
    df = generate_dataset()
    assert len(df) == 2000
    assert int(df["synthetic_label"].sum()) == 200
    # Ranges are intentionally not perfectly separated.
    normal = df[df.synthetic_label == 0]
    unusual = df[df.synthetic_label == 1]
    assert normal["destination_port"].isin(unusual["destination_port"]).any()

def test_evaluation_uses_held_out_split():
    result = analyze_data(generate_dataset(), contamination=0.10, test_size=0.25)
    assert result.train_rows == 1500
    assert result.test_rows == 500
    assert result.evaluation is not None
    assert "anomaly_score" in result.scored_data
    assert len(result.scored_data) == 2000

def test_missing_columns_raise_error():
    with pytest.raises(ValueError):
        validate_data(pd.DataFrame({"protocol": ["TCP"]}))
