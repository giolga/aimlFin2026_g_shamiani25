import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
from itertools import groupby
from operator import itemgetter

# Read traffic data
df = pd.read_csv("traffic_per_minute.csv")
df['time_index'] = np.arange(len(df))  # X = time index

X = df[['time_index']]
y = df['requests']

# Fit linear regression
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

# Calculate residuals
residuals = y - y_pred
threshold = residuals.mean() + 2*residuals.std()  # spike threshold

# Detect DDoS intervals (individual minutes)
ddos_minutes = df['minute'][residuals > threshold]
print(f"Number of potential DDoS intervals detected: {len(ddos_minutes)}")
print("Potential DDoS attack minutes:")
for t in ddos_minutes:
    print(t)

# Group consecutive DDoS minutes into intervals
ddos_list = pd.to_datetime(ddos_minutes).tolist()

intervals = []
for k, g in groupby(enumerate(ddos_list), lambda ix: ix[0] - int(ix[1].timestamp() / 60)):
    group = list(map(itemgetter(1), g))
    intervals.append((group[0], group[-1]))

print("\nDDoS intervals (start -> end):")
for start, end in intervals:
    print(f"{start} -> {end}")

# Visualization
plt.figure(figsize=(12,6))
plt.plot(df['minute'], y, label="Requests per minute")
plt.plot(df['minute'], y_pred, label="Regression line", color='orange')
plt.scatter(ddos_minutes, df['requests'][residuals > threshold], color='red', label="DDoS spike")
plt.xticks(rotation=45)
plt.xlabel("Time")
plt.ylabel("Requests")
plt.title("DDoS Detection via Regression Analysis")
plt.legend()
plt.tight_layout()
plt.savefig("ddos_analysis.png")
plt.show()
