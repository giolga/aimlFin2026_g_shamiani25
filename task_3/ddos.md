DDoS Attack Analysis Report
1. Resource Links

Log File: g_shamiani25_94687_server.log

Processing Script: parser_logs.py

Analysis Script: regression_analysis.py

2. Executive Summary

This report identifies potential DDoS (Distributed Denial of Service) attack intervals within the provided web server log.
By using Linear Regression Analysis, we detected significant deviations in traffic that are likely caused by abnormal request bursts.

3. Detected DDoS Intervals

Based on regression residuals (Threshold: $\mu + 2\sigma$), the following intervals were detected:

Start Time	End Time	Max Requests per Minute
2024-03-22 18:05:00	2024-03-22 18:12:00	[Insert Max RPM]

Note: Multiple intervals can appear if the attack occurs in bursts. Values can be updated from ddos_minutes output.

4. Analysis Methodology
4.1 Log Parsing

Extracted timestamps from each log entry.

Aggregated requests into 1-minute intervals to compute Requests Per Minute (RPM).

Code snippet:

df['minute'] = df['timestamp'].dt.floor('T')
traffic_per_minute = df.groupby('minute').size().reset_index(name='requests')

4.2 Regression Analysis

Applied Linear Regression:

$X$: Time index

$y$: Requests per minute

Residuals $\epsilon = y_{actual} - y_{predicted}$ were calculated.

Any point where $\epsilon > 2 \times \text{std(residuals)}$ was flagged as a potential DDoS spike.

Code snippet:

model = LinearRegression().fit(X, y)
y_pred = model.predict(X)
residuals = y - y_pred
threshold = residuals.mean() + 2*residuals.std()


Notes:

Using 2 standard deviations captures ~95% of normal traffic. Anything above is statistically anomalous.

Linear Regression gives a baseline; if traffic is nonlinear, consider Polynomial Regression.

5. Visualizations

Red points indicate traffic spikes significantly above the expected trend (orange line). These correspond to potential DDoS intervals.

6. How to Reproduce

Ensure the .log file is in the same directory as the scripts.

Run:

python parser_logs.py


to generate traffic_per_minute.csv.
3. Run:

python regression_analysis.py


to detect attack intervals and generate ddos_analysis.png.

7. Tips & Observations

Timezone Handling: Currently, the timezone (+04:00) is ignored; fine for this dataset.

Curve in Traffic: If traffic has daily peaks, consider Polynomial Regression to improve baseline.

Grouping Intervals: Consecutive spike minutes are grouped to identify attack periods clearly.