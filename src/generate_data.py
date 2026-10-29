"""Create overlapping, reproducible synthetic network traffic records."""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42

def generate_dataset(normal_count: int = 1800, unusual_count: int = 200) -> pd.DataFrame:
    """Generate synthetic normal/unusual rows with overlapping feature ranges.

    Labels are only for educational evaluation. They are never passed as a model feature.
    """
    rng = np.random.default_rng(SEED)
    total = normal_count + unusual_count

    # Normal traffic spans a wide range, including some high-volume sessions.
    normal_protocol = rng.choice(["TCP", "UDP"], normal_count, p=[0.72, 0.28])
    normal_ports = rng.choice([53, 80, 123, 443, 8080, 8443, 22, 445, 3389], normal_count,
                              p=[0.10, 0.22, 0.05, 0.35, 0.10, 0.06, 0.05, 0.04, 0.03])
    normal_packets = np.clip(rng.lognormal(mean=2.3, sigma=1.0, size=normal_count), 1, 500).astype(int)
    normal_bytes = np.clip(normal_packets * rng.lognormal(mean=5.4, sigma=0.9, size=normal_count), 60, 250000).astype(int)
    normal_duration = np.clip(rng.lognormal(mean=1.1, sigma=1.0, size=normal_count), 0.01, 180).round(2)

    normal = pd.DataFrame({
        "protocol": normal_protocol,
        "destination_port": normal_ports,
        "packet_count": normal_packets,
        "bytes_sent": normal_bytes,
        "duration_seconds": normal_duration,
        "synthetic_label": 0,
    })

    # Unusual rows are only moderately shifted; many deliberately overlap normal ranges.
    unusual_protocol = rng.choice(["TCP", "UDP"], unusual_count, p=[0.60, 0.40])
    unusual_ports = rng.choice([53, 80, 443, 8080, 4444, 5555, 9001, 31337, 3389], unusual_count,
                               p=[0.08, 0.10, 0.15, 0.10, 0.12, 0.12, 0.10, 0.10, 0.13])
    unusual_packets = np.clip(rng.lognormal(mean=3.5, sigma=1.05, size=unusual_count), 1, 650).astype(int)
    unusual_bytes = np.clip(unusual_packets * rng.lognormal(mean=6.0, sigma=1.0, size=unusual_count), 60, 400000).astype(int)
    unusual_duration = np.clip(rng.lognormal(mean=0.2, sigma=1.25, size=unusual_count), 0.01, 180).round(2)

    unusual = pd.DataFrame({
        "protocol": unusual_protocol,
        "destination_port": unusual_ports,
        "packet_count": unusual_packets,
        "bytes_sent": unusual_bytes,
        "duration_seconds": unusual_duration,
        "synthetic_label": 1,
    })

    df = pd.concat([normal, unusual], ignore_index=True)
    return df.sample(frac=1, random_state=SEED).reset_index(drop=True)

def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output = root / "data" / "network_traffic.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    df = generate_dataset()
    df.to_csv(output, index=False)
    print(f"Dataset created: {output}")
    print(f"Rows: {len(df)}")
    print(f"Normal: {(df['synthetic_label'] == 0).sum()}")
    print(f"Unusual: {(df['synthetic_label'] == 1).sum()}")
    print(df.head().to_string(index=False))

if __name__ == "__main__":
    main()
