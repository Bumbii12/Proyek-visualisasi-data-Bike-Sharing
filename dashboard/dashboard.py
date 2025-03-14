import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Analisis Bike Sharing dengan Streamlit")
st.write("Menjelajahi faktor-faktor yang mempengaruhi peminjaman sepeda.")

df = pd.read_csv("https://raw.githubusercontent.com/Bumbii12/Proyek-visualisasi-data-Bike-Sharing/refs/heads/main/dashboard/all_data.csv")
df["dteday"] = pd.to_datetime(df["dteday"])

min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    st.image("https://www.svgrepo.com/show/70289/bike.svg")
    start_date, end_date = st.date_input(
        label="Pilih Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# **Filter dataset berdasarkan rentang tanggal yang dipilih**
filtered_df = df[(df["dteday"] >= pd.to_datetime(start_date)) & (df["dteday"] <= pd.to_datetime(end_date))]

st.subheader("Dataset yang Digunakan")
st.dataframe(filtered_df.head())  # Menampilkan dataset yang sudah difilter

st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")

weather_avg_rentals = filtered_df.groupby("weathersit")["cnt"].mean().reset_index()
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

st.subheader("Rata-rata Peminjaman Sepeda per Musim")

season_labels = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
filtered_df["season"] = filtered_df["season"].replace(season_labels)
df_season = filtered_df.groupby("season")["cnt"].mean().reset_index()
df_season = df_season.sort_values(by="cnt", ascending=False)

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

st.subheader("Pengaruh Hari Libur terhadap Penyewaan Sepeda")

df_holiday = filtered_df.groupby("holiday")["cnt"].mean().reset_index()
holiday_labels = {0: "Hari Kerja", 1: "Hari Libur"}
df_holiday["holiday"] = df_holiday["holiday"].replace(holiday_labels)
df_holiday = df_holiday.sort_values(by="cnt", ascending=False)

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

st.subheader("Distribusi Kategori Penyewaan Sepeda")

bins = [0, 100, 200, filtered_df["cnt"].max()]
labels = ["Rendah", "Sedang", "Tinggi"]
filtered_df["kategori_penyewaan"] = pd.cut(filtered_df["cnt"], bins=bins, labels=labels, include_lowest=True)

df_kategori = filtered_df["kategori_penyewaan"].value_counts().reset_index()
df_kategori.columns = ["Kategori", "Jumlah"]
df_kategori = df_kategori.sort_values(by="Jumlah", ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    data=df_kategori,
    x="Kategori",
    y="Jumlah",
    hue="Kategori",
    palette=colors,
    legend=False,
    ax=ax,
    order=df_kategori["Kategori"]  
)

max_height = df_kategori["Jumlah"].max()
plt.ylim(0, max_height * 1.2)

for p in ax.patches:
    ax.annotate(
        f"{p.get_height()}",
        (p.get_x() + p.get_width() / 2, p.get_height() + max_height * 0.05),
        ha="center",
        fontsize=12,
        fontweight="bold"
    )

plt.title("Distribusi Kategori Penyewaan Sepeda", fontsize=16, fontweight="bold", pad=10)
plt.xlabel("Kategori Penyewaan", fontsize=12, labelpad=8)
plt.ylabel("Jumlah Data", fontsize=12, labelpad=8)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
st.pyplot(fig)
