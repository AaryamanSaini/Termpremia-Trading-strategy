import pandas as pd

# load the csv
df = pd.read_csv("ACMPREMIA.csv")

# look at the first few rows and column names
print(df.head())
print(df.columns)

import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("ACMPREMIA.csv")
df["DATE"] = pd.to_datetime(df["DATE"])
df = df.sort_values("DATE").reset_index(drop=True)

# Rename yield column for convenience
df["yield10"] = df["10year yield"]

# Daily change in yield
df["dy"] = df["yield10"].diff()

# Strategy positions:
# buy means short yields
# sell means long yields
df["position"] = 0
df.loc[df["buy"] == 1, "position"] = -1
df.loc[df["sell"] == 1, "position"] = 1

df["position"] = df["position"].replace(0, method="ffill").fillna(0)

# PNL in basis points
df["pnl_bps"] = df["position"] * df["dy"] * 10000

# Cumulative PNL
df["cum_pnl"] = df["pnl_bps"].cumsum()

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df["DATE"], df["cum_pnl"])

# Title and labels
plt.title("Term Premium Strategy PNL (bps)")
plt.xlabel("Date")
plt.ylabel("Cumulative PNL (bps)")
plt.grid(True)

# Calculate net bps
net_bps = df["cum_pnl"].iloc[-1]

# Add annotation box on chart
plt.text(
    0.02,            # x position (2 percent from left)
    0.95,            # y position (95 percent up)
    f"Net bps: {net_bps:.2f}",
    transform=plt.gca().transAxes,  # makes text relative to chart
    fontsize=12,
    bbox=dict(facecolor="white", alpha=0.8)
)

plt.show()
# Optional: save output
df.to_csv("strategy_output.csv", index=False)

net_bps = df["cum_pnl"].iloc[-1]
print("Net bps change from start to end:", net_bps)
print("Script finished running.")
print("Net bps:", df["cum_pnl"].iloc[-1])
