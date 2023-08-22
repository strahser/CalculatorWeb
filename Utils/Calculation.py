import pandas as pd


def _filter_df(df: pd.DataFrame, column_name: str, column_value):
	query = df[column_name] == column_value
	return df[query]