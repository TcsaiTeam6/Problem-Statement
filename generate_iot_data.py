import pandas as pd
import random
from datetime import datetime, timedelta

# -----------------------------
# 1. Generate Energy Logs
# -----------------------------
def generate_energy_logs(n_devices=5, days=7, seed=42):
    random.seed(seed)
    data = []
    start_time = datetime.now() - timedelta(days=days)

    for d in range(n_devices):
        device_id = f"device_{d+1}"
        rated_power = random.randint(50, 300)  # watts
        for h in range(days * 24):
            timestamp = start_time + timedelta(hours=h)

            # Simulate usage: higher during 9–18h (work hours), lower otherwise
            if 9 <= timestamp.hour < 18:
                kwh = round(random.uniform(0.2, 2.0), 2)
            else:
                kwh = round(random.uniform(0.05, 0.5), 2)

            data.append([timestamp, device_id, rated_power, kwh])

    df = pd.DataFrame(data, columns=["timestamp", "device_id", "rated_power_w", "kwh"])
    return df

# -----------------------------
# 2. Generate Device Metadata
# -----------------------------
def generate_device_metadata(n_devices=5):
    types = ["AC Unit", "3D Printer", "Conveyor", "CNC Machine", "Lighting"]
    return pd.DataFrame({
        "device_id": [f"device_{i+1}" for i in range(n_devices)],
        "device_type": random.choices(types, k=n_devices),
        "location": [f"Zone_{random.randint(1,3)}" for _ in range(n_devices)]
    })

# -----------------------------
# 3. Generate Device Schedules
# -----------------------------
def generate_schedules(n_devices=5):
    schedules = []
    for i in range(n_devices):
        device_id = f"device_{i+1}"
        schedules.append({
            "device_id": device_id,
            "active_hours": "09:00-18:00"  # Work hours
        })
    return pd.DataFrame(schedules)

# -----------------------------
# 4. Run & Save All CSVs
# -----------------------------
if __name__ == "__main__":
    n_devices = 5
    days = 7

    logs = generate_energy_logs(n_devices=n_devices, days=days)
    metadata = generate_device_metadata(n_devices=n_devices)
    schedules = generate_schedules(n_devices=n_devices)

    # Save CSVs in same folder as script
    logs.to_csv("energy_logs.csv", index=False)
    metadata.to_csv("device_metadata.csv", index=False)
    schedules.to_csv("device_schedules.csv", index=False)

    print("✅ CSV files generated in current folder:")
    print(" - energy_logs.csv")
    print(" - device_metadata.csv")
    print(" - device_schedules.csv")

    # Show previews
    print("\n--- Energy Logs Preview ---")
    print(logs.head())
    print("\n--- Device Metadata ---")
    print(metadata)
    print("\n--- Device Schedules ---")
    print(schedules)
