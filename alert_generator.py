import os
import json

def generate_alerts(alerts_df, out_path='gh0st-siem/alerts.json'):
    records = alerts_df.to_dict(orient='records')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(records, f, indent=2)