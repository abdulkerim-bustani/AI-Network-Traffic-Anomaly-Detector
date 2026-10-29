
from collections import defaultdict
from scapy.all import PcapReader, IP, IPv6, TCP, UDP
import pandas as pd
from pathlib import Path

PCAP_FILE = Path("my_network_capture.pcapng")
CSV_FILE = Path("data/real_network_traffic.csv")

flows = defaultdict(lambda: {
    "packet_count": 0,
    "bytes_sent": 0,
    "first_time": None,
    "last_time": None,
})

with PcapReader(str(PCAP_FILE)) as packets:
    for packet in packets:
        if IP in packet:
            ip = packet[IP]
            src_ip, dst_ip = ip.src, ip.dst
        elif IPv6 in packet:
            ip = packet[IPv6]
            src_ip, dst_ip = ip.src, ip.dst
        else:
            continue

        if TCP in packet:
            protocol = "TCP"
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
        elif UDP in packet:
            protocol = "UDP"
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
        else:
            protocol = "OTHER"
            src_port = 0
            dst_port = 0

        key = (src_ip, dst_ip, src_port, dst_port, protocol)
        flow = flows[key]
        timestamp = float(packet.time)

        flow["packet_count"] += 1
        flow["bytes_sent"] += len(packet)
        flow["first_time"] = (
            timestamp if flow["first_time"] is None
            else min(flow["first_time"], timestamp)
        )
        flow["last_time"] = (
            timestamp if flow["last_time"] is None
            else max(flow["last_time"], timestamp)
        )

rows = []

for (src_ip, dst_ip, src_port, dst_port, protocol), flow in flows.items():
    duration = max(
        0.001,
        flow["last_time"] - flow["first_time"]
    )

    rows.append({
        "protocol": protocol,
        "destination_port": dst_port,
        "packet_count": flow["packet_count"],
        "bytes_sent": flow["bytes_sent"],
        "duration_seconds": round(duration, 6),
        "src_ip": src_ip,
        "dst_ip": dst_ip,
    })

CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
df = pd.DataFrame(rows)

if df.empty:
    raise SystemExit(
        "لم نعثر على حزم IP أو IPv6 في الملف. تحقق من ملف الالتقاط."
    )

df.to_csv(CSV_FILE, index=False)

print(f"تم تحويل الالتقاط إلى: {CSV_FILE}")
print(f"عدد التدفقات: {len(df)}")
print(df.head(10).to_string(index=False))
