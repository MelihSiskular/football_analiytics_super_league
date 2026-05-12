import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text
import matplotlib.patheffects as pe
import os

# Hakemler hakkındaki özet verimizi okuyalım.
df = pd.read_csv("../data/referee_summary.csv")
df = df[df["matches"] >= 5].copy()

#sarı kart ve penaltı arası ilişkiden bahsedeceğiz.
x_col = "yellow_cards_per_match"
y_col = "penalties_per_match"

avg_x = df[x_col].mean()
avg_y = df[y_col].mean()

# x - y koordinatını 4'e bölelim
def get_zone(row):
    if row[x_col] >= avg_x and row[y_col] >= avg_y:
        return "high_high"
    elif row[x_col] < avg_x and row[y_col] >= avg_y:
        return "low_cards_high_pen"
    elif row[x_col] >= avg_x and row[y_col] < avg_y:
        return "high_cards_low_pen"
    else:
        return "low_low"

df["zone"] = df.apply(get_zone, axis=1)

zone_colors = {
    "high_high": "#EF476F",
    "low_cards_high_pen": "#9D4EDD",
    "high_cards_low_pen": "#F8961E",
    "low_low": "#06D6A0"
}

df["color"] = df["zone"].map(zone_colors)

fig, ax = plt.subplots(figsize=(16, 10), dpi=160)

fig.patch.set_facecolor("#F7F8FA")
ax.set_facecolor("#FBFBFC")

# Arka plan quadrant alanları
x_min = df[x_col].min() - 0.20
x_max = df[x_col].max() + 0.20
y_min = df[y_col].min() - 0.07
y_max = df[y_col].max() + 0.12

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
ax.axvline(avg_x, color="#94A3B8", linestyle="--", linewidth=1, alpha=0.7)
ax.axhline(avg_y, color="#94A3B8", linestyle="--", linewidth=1, alpha=0.7)

# Bubble chart
sizes = df["matches"] * 25

ax.scatter(
    df[x_col],
    df[y_col],
    s=sizes,
    c=df["color"],
    edgecolors="white",
    alpha=0.58,
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
        fontsize=7.8,
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
    "SÜPER LİG HAKEM PROFİLLERİ:\nKART VE PENALTI EĞİLİMLERİ",
    fontsize=24,
    fontweight="heavy",
    color="#0B2447",
    ha="center",
    linespacing=0.85
)

# Subtitle
fig.text(
    0.06,
    0.905,
    "X: Maç başına sarı kart  |  Y: Maç başına penaltı  |  Bubble size: Yönettiği maç sayısı",
    fontsize=11,
    color="#5C677D"
)

# Eksenler
ax.set_xlabel("SARI KARTLAR / MAÇ", fontsize=13, fontweight="bold", color="#0B2447", labelpad=14)
ax.set_ylabel("PENALTILAR / MAÇ", fontsize=13, fontweight="bold", color="#0B2447", labelpad=14)

ax.tick_params(axis="both", labelsize=10, colors="#0B2447")

# Grid
ax.grid(True, linestyle="-", linewidth=0.6, alpha=0.08, color="#6C757D")
ax.set_axisbelow(True)

# Kenarlık
for spine in ax.spines.values():
    spine.set_color("#D0D7DE")
    spine.set_linewidth(1)

# Ortalama notları
ax.text(
    avg_x - 0.03,
    df[y_col].max() + 0.03,
    f"Ortalama\nSarı Kart / Maç\n{avg_x:.2f}",
    fontsize=7.8,
    fontweight="bold",
    color="#2454D6",
    ha="right",
    va="bottom"
)

ax.text(
    df[x_col].max() + 0.18,
    avg_y + 0.03,
    f"Ortalama\nPenaltı / Maç\n{avg_y:.2f}",
    fontsize=7.8,
    fontweight="bold",
    color="#2454D6",
    ha="right",
    va="bottom"
)

# Quadrant açıklamaları - ayırdığımız 4 bölge için ayrı ayrı !
ax.text(
    df[x_col].min() - 0.18,
    df[y_col].max() - 0.10,
    "AZ KART - ÇOK PENALTI\nKart göstermeyen ancak\nPenaltı kararı fazla olan hakemler",
    fontsize=9,
    color="#7B2CBF",
    fontweight="bold",
    ha="left",
    va="top",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="none", alpha=0.65)
)

ax.text(
    df[x_col].max() + 0.18,
    df[y_col].max() - 0.10,
    "ÇOK KART - ÇOK PENALTI\nOyuna müdahalesi yüksek,\nKart ve penaltı kararı fazla olan hakemler",
    fontsize=9,
    color="#D90429",
    fontweight="bold",
    ha="right",
    va="top",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="none", alpha=0.65)
)

ax.text(
    df[x_col].min() -0.18,
    df[y_col].min() +0.1,
    "AZ KART - AZ PENALTI\nOyunun akmasına izin veren\nMüdahalesi düşük hakemler",
    fontsize=9,
    color="#008F5A",
    fontweight="bold",
    ha="left",
    va="bottom",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="none", alpha=0.65)
)

ax.text(
    df[x_col].max() + 0.18,
    df[y_col].min() + 0.1,
    "ÇOK KART - AZ PENALTI\nKart gösterme eğilimi yüksek\nPenaltı kararı düşük olan hakemler",
    fontsize=7.8,
    color="#E67700",
    fontweight="bold",
    ha="right",
    va="bottom",
    bbox=dict(boxstyle="round,pad=0.45", facecolor="white", edgecolor="none", alpha=0.75)
)

ax.scatter(
    df[x_col],
    df[y_col],
    s=sizes * 1.35,
    c=df["color"],
    alpha=0.10,
    linewidth=0,
    zorder=2
)

# Bubble size legend
legend_sizes = [5, 10, 15, 20]
legend_handles = [
    plt.scatter([], [], s=s * 25, color="#94A3B8", alpha=0.55, edgecolors="white", linewidth=1)
    for s in legend_sizes
]

legend = ax.legend(
    legend_handles,
    [str(s) if s < 20 else "20+" for s in legend_sizes],
    title="YÖNETTİĞİ MAÇ SAYISI",
    scatterpoints=1,
    frameon=True,
    labelspacing=1,
    borderpad=0.8,
    loc="upper right",
    bbox_to_anchor=(0.99, 1.17),
    ncol=4
)

legend.get_frame().set_facecolor("white")
legend.get_frame().set_edgecolor("#DEE2E6")
legend.get_title().set_fontweight("bold")
legend.get_title().set_color("#0B2447")

for text in legend.get_texts():
    text.set_color("#0B2447")

# Alt bilgi
fig.text(
    0.06,
    0.035,
    "Veri: SofaScore   |   Analiz: Melih Şişkular",
    fontsize=9.5,
    color="#5C677D"
)

fig.text(
    0.94,
    0.035,
    "Sezon: 2025/26 (33 Hafta - 297 Maç)",
    fontsize=9.5,
    color="#5C677D",
    ha="right",
    style="italic"
)

plt.subplots_adjust(left=0.08, right=0.96, top=0.85, bottom=0.12)

os.makedirs("../outputs", exist_ok=True)
ax.set_ylim(df[y_col].min() - 0.07, df[y_col].max() + 0.12)
ax.set_xlim(df[x_col].min() - 0.20, df[x_col].max() + 0.20)

plt.savefig("outputs/referee_bubble_chart_light.png", dpi=300, bbox_inches="tight")
plt.show()