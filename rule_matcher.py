import pandas as pd

def match_detections(logs_df, detections):
    # Stub: flag no logs as alerts
    alerts = logs_df.copy()
    alerts['alert'] = False
    return alerts