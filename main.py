import pandas as pd
import numpy as np
from pathlib import Path

# ----------------------------------------------
# Extract price band percentage
# ----------------------------------------------
def get_band_percent(value):
    if pd.isna(value):
        return 0
    try:
        txt = str(value).replace("–", "-")
        parts = txt.split("-")
        if len(parts) != 2:
            return 0
        low, high = float(parts[0]), float(parts[1])
        mid = (low + high) / 2
        return round(((high - mid) / mid) * 100, 2)
    except:
        return 0


# ----------------------------------------------
# Load Bhav Copy and compute average traded value
# ----------------------------------------------
def load_bhav_copy(files):
    frames = []
    for file in files:
        if Path(file).exists():
            try:
                df = pd.read_csv(file)
                df = df[["TckrSymb", "SctySrs", "TtlTrfVal"]]
                df.columns = ["SYMBOL", "SERIES", "TRADED_VALUE"]
                frames.append(df)
            except Exception as e:
                print("Error loading", file, e)

    if not frames:
        return pd.DataFrame(columns=["SYMBOL","TRADED_VALUE","SERIES"])

    merged = pd.concat(frames, ignore_index=True)
    result = merged.groupby("SYMBOL").agg({
        "TRADED_VALUE": "mean",
        "SERIES": "last"
    }).reset_index()
    return result


# ----------------------------------------------
# Load VAR values from DAT file
# ----------------------------------------------
def load_var_file(path):
    if not Path(path).exists():
        return pd.DataFrame(columns=["SYMBOL","VAR"])

    rows = []
    with open(path,"r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) > 4 and parts[0] == "20":
                try:
                    rows.append([parts[1], float(parts[4])])
                except:
                    pass  

    return pd.DataFrame(rows, columns=["SYMBOL","VAR"]).drop_duplicates()


# ----------------------------------------------
# Categorization Logic
# ----------------------------------------------
def assign_category(row):
    s = row["SERIES"]
    traded = row["TRADED_VALUE"]
    band = row["PRICE_BAND"]
    fno = row["is_fno"]
    var = row["VAR"]

    category = "Only Delivery"

    # Normal conditions
    if s in ["EQ","BE","BZ"] and traded > 5000000 and band > 5:
        category = "5x"
    elif s in ["EQ","BE","BZ"] and traded > 2000000 and band > 5:
        category = "3x"

    # F&O overrides
    if fno and var <= 20:
        category = "5x"
    elif fno and var <= 33.33 and category != "5x":
        category = "3x"

    return category


# =====================================================
# MAIN PROGRAM
# =====================================================

# --- Load security.txt safely (manual parser) ---
rows = []
with open("security.txt", "r", encoding="latin1") as f:
    for line in f:
        rows.append(line.strip().split("|"))

# Remove metadata row
rows = rows[1:]

# Extract needed columns manually
symbols, series_list, price_ranges = [], [], []

for row in rows:
    symbol = row[1] if len(row) > 1 else ""
    ser = row[2] if len(row) > 2 else ""
    prange = row[6] if len(row) > 6 else ""

    symbols.append(symbol.strip())
    series_list.append(ser.strip())
    price_ranges.append(prange.strip())

sec = pd.DataFrame({
    "SYMBOL": symbols,
    "SERIES": series_list,
    "PRICE_RANGE": price_ranges
})

# Compute price band %
sec["PRICE_BAND"] = sec["PRICE_RANGE"].apply(get_band_percent)


# Load Bhav copies
bhav_files = [
    "BhavCopy_NSE_CM (1).csv",
    "BhavCopy_NSE_CM (2).csv",
    "BhavCopy_NSE_CM (3).csv",
]
bhav_df = load_bhav_copy(bhav_files)


# Merge security + bhav
full = sec.merge(bhav_df, on="SYMBOL", how="left")

# Fix SERIES column conflicts after merge
if "SERIES_x" in full.columns:
    full["SERIES"] = full["SERIES_x"]
elif "SERIES_y" in full.columns:
    full["SERIES"] = full["SERIES_y"]

full["TRADED_VALUE"] = full["TRADED_VALUE"].fillna(0)


# Load VAR data
var_df = load_var_file("C_VAR1_06112025_6.DAT")
full = full.merge(var_df, on="SYMBOL", how="left")
full["VAR"] = full["VAR"].fillna(9999)


# Load F&O list
try:
    fno_list = set(pd.read_csv("FNO_Underlyings.csv")["SYMBOL"].str.strip())
except:
    fno_list = set()

full["is_fno"] = full["SYMBOL"].isin(fno_list)


# Assign final categories
full["category"] = full.apply(assign_category, axis=1)

# Save output
full.to_csv("securities_categorized.csv", index=False)

print("✔ Categorization completed successfully. Output saved as securities_categorized.csv")
