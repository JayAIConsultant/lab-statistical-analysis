import pandas as pd
import re

df = pd.read_csv("data/final_shop_6modata.csv")

def extract_device(ad_group: str) -> str:
    if " Desk " in ad_group or " Desk -" in ad_group:
        return "Desktop"
    elif " Mob " in ad_group or " Mob -" in ad_group:
        return "Mobile"
    return "Unknown"

def extract_match_type(ad_group: str) -> str:
    if "1:1" in ad_group:
        return "1:1"
    elif "Exact" in ad_group:
        return "Exact"
    elif "Phrase" in ad_group:
        return "Phrase"
    return "Unknown"

df["Device"] = df["Ad Group"].apply(extract_device)
df["Match_Type"] = df["Ad Group"].apply(extract_match_type)
df["Channel"] = df["Device"] + " - " + df["Match_Type"]

print("Derived channel groups:")
print(df["Channel"].value_counts())
print()
print("Any 'Unknown' rows (parsing failures)?")
print(df[(df["Device"] == "Unknown") | (df["Match_Type"] == "Unknown")])

df.to_csv("marketing_data.csv", index=False)
print("\nSaved marketing_data.csv, shape:", df.shape)