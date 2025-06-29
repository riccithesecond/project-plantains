import os
import pandas as pd

class EnrichmentEngine:
    def __init__(self, assets_path, users_path):
        self.assets_df = pd.read_csv(assets_path) if os.path.exists(assets_path) else pd.DataFrame()
        self.users_df = pd.read_csv(users_path) if os.path.exists(users_path) else pd.DataFrame()

    def enrich(self, df):
        enriched = df.copy()
        # Enrich on hostname
        if 'hostname' in enriched.columns and not self.assets_df.empty:
            enriched = enriched.merge(self.assets_df, how='left', on='hostname')
        # Enrich on user
        if 'user' in enriched.columns and not self.users_df.empty:
            enriched = enriched.merge(self.users_df, how='left', left_on='user', right_on='username')
        return enriched