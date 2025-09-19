# Problem-Statement
Statement06
Title Name: IOT Energy Consumption Optimization Agent. Problem Statements: Optimizing energy consumption across IoT- enabled devices in digital engineering setups is challenging without real-time Insights and recommendations. Steps: Build an AI agent that analyzes energy usage data from IoT devices. Use Langchain or Llamaindex to Identify in efficiencies and suggest optimization strategies. Allow users to query energy consumption patterns and recieve recommendations. Test with sample IoT energy data. Data requirements: Energy consumption logs, device metadata, operational schedules. Sample data can be genereated or sourced from open IoT energy datasets. Expected Output: Textual reports on energy usage and optimization suggestions.


# sample_data.py
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_energy_logs(n_devices=5, days=7, seed=42):
    random.seed(seed)
    data = []
    start_time = datetime.now() - timedelta(days=days)

    for d in range(n_devices):
        device_id = f"device_{d+1}"
        rated_power = random.randint(50, 300)  # watts
        for h in range(days * 24):
            timestamp = start_time + timedelta(hours=h)

            # Simulated usage (higher during 9am–6pm, lower otherwise)
            if 9 <= timestamp.hour < 18:
                kwh = round(random.uniform(0.2, 2.0), 2)
            else:
                kwh = round(random.uniform(0.05, 0.5), 2)

            data.append([timestamp, device_id, rated_power, kwh])

    df = pd.DataFrame(data, columns=["timestamp", "device_id", "rated_power_w", "kwh"])
    return df

def generate_device_metadata(n_devices=5):
    types = ["AC Unit", "3D Printer", "Conveyor", "CNC Machine", "Lighting"]
    return pd.DataFrame({
        "device_id": [f"device_{i+1}" for i in range(n_devices)],
        "device_type": random.choices(types, k=n_devices),
        "location": [f"Zone_{random.randint(1,3)}" for _ in range(n_devices)]
    })

def generate_schedules(n_devices=5):
    schedules = []
    for i in range(n_devices):
        device_id = f"device_{i+1}"
        schedules.append({
            "device_id": device_id,
            "active_hours": "09:00-18:00"  # baseline working hours
        })
    return pd.DataFrame(schedules)

if __name__ == "__main__":
    logs = generate_energy_logs()
    metadata = generate_device_metadata()
    schedules = generate_schedules()

    logs.to_csv("energy_logs.csv", index=False)
    metadata.to_csv("device_metadata.csv", index=False)
    schedules.to_csv("device_schedules.csv", index=False)

    print("✅ Sample data generated: energy_logs.csv, device_metadata.csv, device_schedules.csv")
# analysis_pipeline.py
import pandas as pd

def analyze_energy(logs: pd.DataFrame, metadata: pd.DataFrame, schedules: pd.DataFrame):
    report = []

    # Total energy
    total_energy = logs["kwh"].sum()
    report.append(f"🔋 Total energy consumed: {total_energy:.2f} kWh")

    # Device-level totals
    device_totals = logs.groupby("device_id")["kwh"].sum().sort_values(ascending=False)
    top_device = device_totals.idxmax()
    report.append(f"📌 Top consuming device: {top_device} ({device_totals.max():.2f} kWh)")

    # Idle-time usage (consumption < 0.2 kWh assumed idle)
    idle_usage = logs[logs["kwh"] < 0.2]["kwh"].sum()
    report.append(f"💤 Idle-time energy waste: {idle_usage:.2f} kWh")

    # Peak vs Off-peak usage
    logs["hour"] = logs["timestamp"].dt.hour
    peak = logs[(logs["hour"] >= 9) & (logs["hour"] < 18)]["kwh"].sum()
    offpeak = logs[(logs["hour"] < 9) | (logs["hour"] >= 18)]["kwh"].sum()
    report.append(f"🌞 Peak hours: {peak:.2f} kWh | 🌙 Off-peak: {offpeak:.2f} kWh")

    # Compare to schedule (detect if device runs outside active hours)
    for _, row in schedules.iterrows():
        device_id = row["device_id"]
        active_start, active_end = [int(x.split(":")[0]) for x in row["active_hours"].split("-")]
        dev_logs = logs[logs["device_id"] == device_id]
        outside_usage = dev_logs[
            (dev_logs["hour"] < active_start) | (dev_logs["hour"] >= active_end)
        ]["kwh"].sum()
        if outside_usage > 0.5:
            report.append(f"⚠️ {device_id} consumed {outside_usage:.2f} kWh outside schedule.")

    return "\n".join(report)

if __name__ == "__main__":
    logs = pd.read_csv("energy_logs.csv", parse_dates=["timestamp"])
    metadata = pd.read_csv("device_metadata.csv")
    schedules = pd.read_csv("device_schedules.csv")

    report = analyze_energy(logs, metadata, schedules)
    print("=== Energy Usage Report ===")
    print(report)

