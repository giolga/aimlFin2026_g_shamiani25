import pandas as pd
import re
from datetime import datetime

log_file = "g_shamiani25_94687_server.log"

# Regex to extract timestamp
log_pattern = r'\[(.*?)\]'

timestamps = []

with open(log_file, "r") as f:
    for line in f:
        match = re.search(log_pattern, line)
        if match:
            ts = datetime.strptime(match.group(1)[:19], "%Y-%m-%d %H:%M:%S")
            timestamps.append(ts)

# Create DataFrame and aggregate per minute
df = pd.DataFrame({"timestamp": timestamps})
df['minute'] = df['timestamp'].dt.floor('T')
traffic_per_minute = df.groupby('minute').size().reset_index(name='requests')

# Save CSV for later use
traffic_per_minute.to_csv("traffic_per_minute.csv", index=False)
print(traffic_per_minute.head())

# Add summary
print(f"Total log entries processed: {len(timestamps)}")
print(f"Time range: {timestamps[0]} to {timestamps[-1]}")

# Optional quick visualization
import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.plot(traffic_per_minute['minute'], traffic_per_minute['requests'])
plt.xticks(rotation=45)
plt.xlabel("Time")
plt.ylabel("Requests per minute")
plt.title("Web Traffic Overview")
plt.tight_layout()
plt.savefig("traffic_overview.png")
plt.show()
