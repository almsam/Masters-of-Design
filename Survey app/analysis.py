import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_FILE = r"c:\Users\samia\OneDrive\Desktop\Masters of Design\Survey app\responses.csv"
OUTPUT = "cohort_summary.png"

sns.set_theme(style="dark")

# Load data

print(BASE_DIR)
cohort = pd.read_csv(CSV_FILE)

cohort = cohort.loc[:, ~cohort.columns.str.contains("^Unnamed")]
cohort.columns = cohort.columns.str.strip()

# Figure

fig = plt.figure(figsize=(14, 14))

# Graph 1 : Boxplot + Scatter

ax = plt.subplot(2, 2, 1)

colors = ["magenta", "yellow", "coral", "yellowgreen", "turquoise"]

plot_df = cohort[
    [
        "Fine Arts",
        "Humanities",
        "Physical Sciences",
        "Life Sciences",
        "Mathematics"
    ]
].melt(var_name="Category", value_name="Value")

sns.boxplot(data=plot_df, x="Category", y="Value", palette=colors, width=0.5, showfliers=False)
sns.stripplot(data=plot_df, x="Category", y="Value", palette=colors, jitter=0.1, size=6, alpha=0.65 )
ax.set_ylim(0,5); ax.set_xlabel(""); ax.set_ylabel(""); ax.set_yticks([])
for label in ax.get_xticklabels():
    label.set_rotation(30); label.set_fontsize(15); label.set_fontweight("bold")

# Graph 2 : Execution Style

ax = plt.subplot(2,2,2)

ax.scatter(
    cohort["Q2x"],
    cohort["Q2y"],
    color="tomato",
    s=70,
    alpha=0.5
)

ax.scatter(cohort["Q2x"], cohort["Q2y"], s=70, color="tomato", alpha=0.5 )
ax.set_xlim(-11,11); ax.set_ylim(-11,11); ax.axhline(0,color="black"); ax.axvline(0,color="black")
ax.set_xticks([]); ax.set_yticks([])

ax.text(0,11,"Structured Thoughts", ha="center", va="center", fontsize=18, fontweight="bold")
ax.text(0,-11,"Freeform Thoughts", ha="center", va="center", fontsize=18, fontweight="bold")
ax.text(11,0,"Few Big Steps", rotation=90, ha="center", va="center", fontsize=18, fontweight="bold")
ax.text(-11,0,"Many Small Steps", rotation=90, ha="center", va="center", fontsize=18, fontweight="bold")

# Graph 3 : Thinking Style

ax = plt.subplot(2,2,3)
ax.scatter(cohort["Q3x"], cohort["Q3y"], s=70, color="lime", alpha=0.5 )
ax.set_xlim(-11,11); ax.set_ylim(-11,11); ax.axhline(0,color="black"); ax.axvline(0,color="black")
ax.set_xticks([]); ax.set_yticks([])
ax.text(0,11,"Human Feedback", ha="center", va="center", fontsize=18, fontweight="bold")
ax.text(0,-11,"Mechanical Testing", ha="center", va="center", fontsize=18, fontweight="bold")
ax.text(11,0,"Systems Thinking", rotation=90, ha="center", va="center", fontsize=18, fontweight="bold")
ax.text(-11,0,"Detailed Thinking", rotation=90, ha="center", va="center", fontsize=18, fontweight="bold")

# Graph 4 : Radar Overlay

ax = plt.subplot(2,2,4, polar=True)

labels = ["Fine\nArts", "\n\nHumanities", "Life\nSciences", "Physical\nSciences", "Mathematics" ]

columns = ["Fine Arts", "Humanities", "Life Sciences", "Physical Sciences", "Mathematics" ]

dot_colors = ["magenta", "yellow", "yellowgreen", "coral", "turquoise" ]

N = len(labels)

angles = np.linspace(0,2*np.pi,N,endpoint=False).tolist(); angles += angles[:1]
# angles += angles[:1]

ax.set_ylim(0,5)
for _, row in cohort.iterrows():
    values = [row["Fine Arts"], row["Humanities"], row["Life Sciences"], row["Physical Sciences"], row["Mathematics"] ]; values += values[:1]
    ax.plot(angles, values, color="dodgerblue", alpha=0.12, linewidth=1 ); ax.fill(angles, values, color="dodgerblue", alpha=0.015 )
    colors = ["magenta","yellow","yellowgreen","coral","turquoise"]
    columns = ["Fine Arts", "Humanities", "Life Sciences", "Physical Sciences", "Mathematics" ]
for angle, column, color in zip(angles[:-1], columns, dot_colors):
    ax.scatter(np.full(len(cohort), angle), cohort[column], color=color, s=18, alpha=0.75, zorder=10 )
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=12, fontweight="bold")

ax.tick_params(axis="x", pad=20)
ax.set_yticklabels([])

# Save

plt.tight_layout()
plt.savefig(OUTPUT, dpi=300)
plt.show()