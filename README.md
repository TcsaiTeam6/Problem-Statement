# Problem-Statement
Statement06
Title Name: IOT Energy Consumption Optimization Agent. Problem Statements: Optimizing energy consumption across IoT- enabled devices in digital engineering setups is challenging without real-time Insights and recommendations. Steps: Build an AI agent that analyzes energy usage data from IoT devices. Use Langchain or Llamaindex to Identify in efficiencies and suggest optimization strategies. Allow users to query energy consumption patterns and recieve recommendations. Test with sample IoT energy data. Data requirements: Energy consumption logs, device metadata, operational schedules. Sample data can be genereated or sourced from open IoT energy datasets. Expected Output: Textual reports on energy usage and optimization suggestions.


Code: # iot_energy_agent.py
import pandas as pd
import random
from datetime import datetime, timedelta
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# Step 1: Generate Sample IoT Energy Data
def generate_sample_data(n_devices=5, days=7):
    data = []
    start_time = datetime.now() - timedelta(days=days)
    for d in range(n_devices):
        device_id = f"device_{d+1}"
        for h in range(days * 24):
            timestamp = start_time + timedelta(hours=h)
            kwh = round(random.uniform(0.1, 2.5), 2)  # simulated usage
            data.append([timestamp, device_id, kwh])
    df = pd.DataFrame(data, columns=["timestamp", "device_id", "kwh"])
    return df

# Step 2: Analysis Functions
def analyze_energy(df):
    report = []
    total = df["kwh"].sum()
    max_device = df.groupby("device_id")["kwh"].sum().idxmax()
    idle_usage = df[df["kwh"] < 0.3]["kwh"].sum()
    report.append(f"Total energy consumed: {total:.2f} kWh")
    report.append(f"Highest consuming device: {max_device}")
    report.append(f"Idle-time energy waste: {idle_usage:.2f} kWh")
    return "\n".join(report)

# Step 3: LLM-powered Recommendations
def get_recommendations(summary):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    prompt = PromptTemplate(
        input_variables=["summary"],
        template="""
        You are an IoT Energy Optimization Expert.
        Based on this energy summary:
        {summary}
        
        Suggest 3 actionable ways to optimize energy consumption.
        """
    )
    chain = LLMChain(prompt=prompt, llm=llm)
    return chain.run(summary)

# Example Run
if __name__ == "__main__":
    df = generate_sample_data()
    summary = analyze_energy(df)
    print("=== Energy Analysis ===")
    print(summary)
    print("\n=== Recommendations ===")
    print(get_recommendations(summary))
