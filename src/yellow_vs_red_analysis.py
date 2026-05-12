import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from adjustText import adjust_text
import os

df = pd.read_csv("data/referee_summary.csv")

df = df[df["matches"] >= 5].copy()

x_col = "yellow_cards_per_match"
y_col = "red_cards_per_match"

avg_x = df[x_col].mean()
avg_y = df[y_col].mean()

# Bölge renkleri
def get_zone(row):

    if row[x_col] >= avg_x and row[y_col] >= avg_y:
        return "#EF476F"

    elif row[x_col] < avg_x and row[y_col] >= avg_y:
        return "#9D4EDD"

    elif row[x_col] >= avg_x and row[y_col] < avg_y:
        return "#F8961E"

    else:
        return "#06D6A0"

df["color"] = df.apply(get_zone, axis=1)

fig, ax = plt.subplots(figsize=(16, 10), dpi=160)

fig.patch.set_facecolor("#F7F8FA")
ax.set_facecolor("#FBFBFC")

# Limitler
x_min = df[x_col].min() - 0.2
x_max = df[x_col].max() + 0.2

y_min = df[y_col].min() - 0.05
y_max = df[y_col].max() + 0.08

# Quadrant background
alpha_bg = 0.035

# Sol alt
ax.fill_between(
    [x_min, avg_x],
    y_min,
    avg_y,
    color="#06D6A0",
    alpha=alpha_bg,
    zorder=0
)

# Sol üst
ax.fill_between(
    [x_min, avg_x],
    avg_y,
    y_max,
    color="#9D4EDD",
    alpha=alpha_bg,
    zorder=0
)

# Sağ alt
ax.fill_between(
    [avg_x, x_max],
    y_min,
    avg_y,
    color="#F8961E",
    alpha=alpha_bg,
    zorder=0
)

# Sağ üst
ax.fill_between(
    [avg_x, x_max],
    avg_y,
    y_max,
    color="#EF476F",
    alpha=alpha_bg,
    zorder=0
)

# Ortalama çizgileri
ax.axvline(
    avg_x,
    color="#94A3B8",
    linestyle="--",
    linewidth=1
)

ax.axhline(
    avg_y,
    color="#94A3B8",
    linestyle="--",
    linewidth=1
)

sizes = df["matches"] * 25

# İkincil bubble
ax.scatter(
    df[x_col],
    df[y_col],
    s=sizes * 1.35,
    c=df["color"],
    alpha=0.10,
    linewidth=0,
    zorder=2
)

# Ana bubble
scatter = ax.scatter(
    df[x_col],
    df[y_col],
    s=sizes,
    c=df["color"],
    alpha=0.60,
    edgecolors="white",
    linewidth=2.4,
    zorder=3
)

# Label'lar
texts = []

for _, row in df.iterrows():

    txt = ax.text(
        row[x_col],
        row[y_col],
        row["referee_name"],
        fontsize=7.6,
        fontweight="bold",
        color="#0B2447",
        zorder=4
    )

    txt.set_path_effects([
        pe.withStroke(linewidth=3, foreground="white")
    ])

    texts.append(txt)

adjust_text(
    texts,
    ax=ax,
    expand_points=(1.4, 1.6),
    expand_text=(1.2, 1.4),
    arrowprops=dict(
        arrowstyle="-",
        color="#6C757D",
        alpha=0.35,
        lw=0.7
    )
)

# Başlık
fig.text(
    0.5,
    0.94,
    "SÜPER LİG HAKEMLERİ:\nSARI KART vs KIRMIZI KART PROFİLİ",
    fontsize=24,
    fontweight="heavy",
    color="#0B2447",
    ha="center",
    linespacing=0.85
)

fig.text(
    0.5,
    0.905,
    "X: Maç başına sarı kart | Y: Maç başına kırmızı kart | Bubble size: Yönettiği maç sayısı",
    fontsize=11,
    color="#5C677D",
    ha="center"
)

# Quadrant text
ax.text(
    x_min + 0.05,
    y_max - 0.02,
    "AZ SARI - ÇOK KIRMIZI",
    fontsize=10,
    fontweight="bold",
    color="#7B2CBF"
)

ax.text(
    x_max - 0.05,
    y_max - 0.02,
    "ÇOK SARI - ÇOK KIRMIZI",
    fontsize=10,
    fontweight="bold",
    color="#D90429",
    ha="right"
)

ax.text(
    x_min + 0.05,
    y_min + 0.02,
    "AZ SARI - AZ KIRMIZI",
    fontsize=10,
    fontweight="bold",
    color="#008F5A"
)

ax.text(
    x_max - 0.05,
    y_min + 0.02,
    "ÇOK SARI - AZ KIRMIZI",
    fontsize=10,
    fontweight="bold",
    color="#E67700",
    ha="right"
)

# Axis
ax.set_xlabel(
    "SARI KART / MAÇ",
    fontsize=13,
    fontweight="bold",
    color="#0B2447"
)

ax.set_ylabel(
    "KIRMIZI KART / MAÇ",
    fontsize=13,
    fontweight="bold",
    color="#0B2447"
)

ax.tick_params(axis="both", labelsize=10, colors="#0B2447")

ax.grid(True, alpha=0.08)

for spine in ax.spines.values():
    spine.set_color("#D0D7DE")

# Alt bilgi
fig.text(
    0.06,
    0.035,
    "Analiz: Melih Şişkular",
    fontsize=9.5,
    color="#5C677D"
)

fig.text(
    0.94,
    0.035,
    "Sezon: 2025/26",
    fontsize=9.5,
    color="#5C677D",
    ha="right",
    style="italic"
)

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

plt.subplots_adjust(
    left=0.08,
    right=0.96,
    top=0.85,
    bottom=0.12
)

os.makedirs("../outputs", exist_ok=True)

plt.savefig(
    "outputs/yellow_vs_red_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()