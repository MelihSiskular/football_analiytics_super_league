import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import os

# csv dosyamızı buradan okuyacağız.
df = pd.read_csv("data/referee_summary.csv")

# Minimum maç filtresi
df = df[df["matches"] >= 5].copy()

# Sertlik endeksi -> Bu değerleri kendim verdim !
df["strictness_score"] = (
    df["yellow_cards_per_match"] * 1
    + df["red_cards_per_match"] * 4
    + df["penalties_per_match"] * 2
)

df = df.sort_values("strictness_score", ascending=True)

# Renk
colors = []
for value in df["strictness_score"]:
    if value >= df["strictness_score"].quantile(0.75):
        colors.append("#EF476F")
    elif value >= df["strictness_score"].median():
        colors.append("#F8961E")
    else:
        colors.append("#06D6A0")

fig, ax = plt.subplots(figsize=(13, 9), dpi=160)

fig.patch.set_facecolor("#F7F8FA")
ax.set_facecolor("#FBFBFC")

bars = ax.barh(
    df["referee_name"],
    df["strictness_score"],
    color=colors,
    edgecolor="white",
    linewidth=2,
    alpha=0.9
)

# Değer etiketleri
for bar in bars:
    width = bar.get_width()

    txt = ax.text(
        width + 0.05,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.2f}",
        va="center",
        ha="left",
        fontsize=8.5,
        fontweight="bold",
        color="#0B2447"
    )

    txt.set_path_effects([
        pe.withStroke(linewidth=3, foreground="white")
    ])

# Ortalama çizgisi
avg = df["strictness_score"].mean()

ax.axvline(
    avg,
    color="#94A3B8",
    linestyle="--",
    linewidth=1.2
)

ax.text(
    avg + 0.05,
    len(df) - 1,
    f"Ortalama: {avg:.2f}",
    fontsize=9,
    fontweight="bold",
    color="#2454D6",
    va="center"
)

# Başlık
fig.text(
    0.5,
    0.94,
    "SÜPER LİG HAKEM SERTLİK ENDEKSİ",
    fontsize=24,
    fontweight="heavy",
    color="#0B2447",
    ha="center"
)

fig.text(
    0.5,
    0.905,
    "Endeks = Sarı Kart/Maç + 4×Kırmızı Kart/Maç + 2×Penaltı/Maç",
    fontsize=11,
    color="#5C677D",
    ha="center"
)

ax.set_xlabel("SERTLİK ENDEKSİ", fontsize=12, fontweight="bold", color="#0B2447")
ax.set_ylabel("")

ax.tick_params(axis="x", labelsize=10, colors="#0B2447")
ax.tick_params(axis="y", labelsize=9, colors="#0B2447")

ax.grid(axis="x", alpha=0.10)
ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_color("#D0D7DE")

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

plt.subplots_adjust(left=0.26, right=0.94, top=0.84, bottom=0.10)

os.makedirs("../outputs", exist_ok=True)
plt.savefig("outputs/referee_strictness_index.png", dpi=300, bbox_inches="tight")
plt.show()