import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Analisis Bike Sharing dengan Streamlit")
st.write("Menjelajahi faktor-faktor yang mempengaruhi peminjaman sepeda.")

# Load dataset
df = pd.read_csv("https://raw.githubusercontent.com/Bumbii12/Proyek-visualisasi-data-Bike-Sharing/refs/heads/main/dashboard/all_data.csv")
df["dteday"] = pd.to_datetime(df["dteday"])

st.sidebar.image("https://www.svgrepo.com/show/70289/bike.svg")

# Menampilkan dataset
st.subheader("Dataset yang Digunakan")
st.dataframe(df.head())

# Pengaruh Cuaca terhadap Penyewaan Sepeda
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")

weather_avg_rentals = df.groupby("weathersit")["cnt"].mean().reset_index()
weather_avg_rentals = weather_avg_rentals.sort_values(by="cnt", ascending=False)

base_color = "#63b3ed"
highlight_color = "#1e4e8c"
colors = [highlight_color if i == 0 else base_color for i in range(len(weather_avg_rentals))]

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    data=weather_avg_rentals,
    x="weathersit",
    y="cnt",
    hue="weathersit",
    palette=colors,
    legend=False,
    ax=ax
)

max_height = weather_avg_rentals["cnt"].max()
plt.ylim(0, max_height * 1.2)

for p in ax.patches:
    ax.annotate(
        f"{int(p.get_height())}",
        (p.get_x() + p.get_width() / 2, p.get_height() + max_height * 0.05),
        ha="center",
        fontsize=12,
        fontweight="bold"
    )

plt.title("Pengaruh Cuaca terhadap Penyewaan Sepeda", fontsize=16, fontweight="bold", pad=10)
plt.xlabel("Kondisi Cuaca", fontsize=12, labelpad=8)
plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12, labelpad=8)
plt.xticks(rotation=5, fontsize=11)
plt.yticks(fontsize=11)
st.pyplot(fig)

# Rata-rata Peminjaman Sepeda per Musim
st.subheader("Rata-rata Peminjaman Sepeda per Musim")

season_labels = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
df["season"] = df["season"].replace(season_labels)
df_season = df.groupby("season")["cnt"].mean().reset_index()
df_season = df_season.sort_values(by="cnt", ascending=False)

base_color = "#63b3ed"
highlight_color = "#1e4e8c"
colors = [highlight_color if i == 0 else base_color for i in range(len(df_season))]

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    data=df_season,
    x="season",
    y="cnt",
    palette=colors,
    legend=False,
    ax=ax
)

max_height = df_season["cnt"].max()
plt.ylim(0, max_height * 1.2)

for p in ax.patches:
    ax.annotate(
        f"{int(p.get_height())}",
        (p.get_x() + p.get_width() / 2, p.get_height() + max_height * 0.05),
        ha="center",
        fontsize=12,
        fontweight="bold"
    )

plt.title("Pengaruh Musim terhadap Penyewaan Sepeda", fontsize=16, fontweight="bold", pad=10)
plt.xlabel("Musim", fontsize=12, labelpad=8)
plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12, labelpad=8)
plt.xticks(rotation=5, fontsize=11)
plt.yticks(fontsize=11)
st.pyplot(fig)

# Pengaruh Hari Libur terhadap Penyewaan Sepeda
st.subheader("Pengaruh Hari Libur terhadap Penyewaan Sepeda")

df_holiday = df.groupby("holiday")["cnt"].mean().reset_index()
holiday_labels = {0: "Hari Kerja", 1: "Hari Libur"}
df_holiday["holiday"] = df_holiday["holiday"].replace(holiday_labels)
df_holiday = df_holiday.sort_values(by="cnt", ascending=False)

base_color = "#63b3ed"
highlight_color = "#1e4e8c"
colors = [highlight_color if i == 0 else base_color for i in range(len(df_holiday))]

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    data=df_holiday,
    x="holiday",
    y="cnt",
    hue="holiday",
    palette=colors,
    legend=False,
    ax=ax
)

max_height = df_holiday["cnt"].max()
plt.ylim(0, max_height * 1.2)

for p in ax.patches:
    ax.annotate(
        f"{p.get_height():.2f}",
        (p.get_x() + p.get_width() / 2, p.get_height() + max_height * 0.05),
        ha="center",
        fontsize=12,
        fontweight="bold"
    )

plt.title("Pengaruh Hari Libur terhadap Penyewaan Sepeda", fontsize=16, fontweight="bold", pad=10)
plt.xlabel("Kategori Hari", fontsize=12, labelpad=8)
plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12, labelpad=8)
plt.xticks(rotation=5, fontsize=11)
plt.yticks(fontsize=11)
st.pyplot(fig)