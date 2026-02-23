import pandas as pd
import json
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

logs =[]

with open("app.log") as f:
    for line in f:
        try:
            logs.append(json.loads(line))
        except:
            pass

df = pd.DataFrame(logs)

# Selecting the particular columns
features = df[['latency', 'error_count','retry_count', 'timeout_flag']]

# Make all features come into same measurement scale
scaler = StandardScaler()
scaled = scaler.fit_transform(features)

model = IsolationForest(contamination=0.05)

df['anomaly'] = model.fit_predict(scaled)

print(df[df['anomaly']== -1])