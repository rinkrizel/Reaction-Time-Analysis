from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1) Create synthetic data
rng = np.random.default_rng(0)

n_subjects = 20
trials_per_subject = 200
conditions = ["easy", "hard"]

rows = []
for s in range(n_subjects):
    for t in range(trials_per_subject):
        cond = rng.choice(conditions, p=[0.5, 0.5])

        # baseline RT: hard is slower
        base = 520 if cond == "easy" else 650
        rt = rng.normal(loc=base, scale=120)

        # inject some outliers
        if rng.random() < 0.01:
            rt = rng.uniform(50, 120)      # too fast
        if rng.random() < 0.01:
            rt = rng.uniform(3200, 6000)   # too slow

        # accuracy: hard slightly worse
        p_correct = 0.92 if cond == "easy" else 0.85
        correct = 1 if rng.random() < p_correct else 0

        rows.append((s, t, cond, float(rt), correct))

df = pd.DataFrame(rows, columns=["subject","trial","condition","rt_ms","correct"])
df.to_csv(Path("data", "synthetic_rt.csv", index=False))

df.head()


# 2) Basic cleaning
df_clean = df.copy()
df_clean = df_clean[(df_clean["rt_ms"] >= 150) & (df_clean["rt_ms"] <= 3000)]

print("Before:", len(df), "After:", len(df_clean))

# 3) Plot distribution before vs after
plt.figure()
plt.hist(df["rt_ms"], bins=60, alpha=0.6, label="before")
plt.hist(df_clean["rt_ms"], bins=60, alpha=0.6, label="after")
plt.xlabel("Reaction time (ms)")
plt.ylabel("Count")
plt.title("RT distribution (before vs after cleaning)")
plt.legend()
plt.tight_layout()
plt.savefig(Path("figures", "rt_distribution_before_after.png"))
plt.show()

# 4) Summary stats by condition
summary = (
    df_clean.groupby("condition")
    .agg(mean_rt=("rt_ms","mean"),
         median_rt=("rt_ms","median"),
         accuracy=("correct","mean"),
         n=("rt_ms","size"))
    .reset_index()
)
print(summary)

# 5) Speed–accuracy tradeoff by subject
by_subj = (
    df_clean.groupby(["subject","condition"])
    .agg(mean_rt=("rt_ms","mean"),
         accuracy=("correct","mean"))
    .reset_index()
)

# Figure plotting
plt.figure()
for cond in conditions:
    sub = by_subj[by_subj["condition"] == cond]
    plt.scatter(sub["mean_rt"], sub["accuracy"], label=cond, alpha=0.8)
    plt.savefig(Path("figures", "rt_by_condition.png"))

plt.xlabel("Mean RT (ms)")
plt.ylabel("Accuracy")
plt.title("Speed–accuracy tradeoff (per subject)")
plt.legend()
plt.tight_layout()
plt.savefig(Path("figures", "speed_accuracy.png"))
plt.show()
