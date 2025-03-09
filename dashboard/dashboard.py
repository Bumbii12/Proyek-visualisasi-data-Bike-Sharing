import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Analisis Bike Sharing dengan Streamlit")
st.write("Menjelajahi faktor-faktor yang mempengaruhi peminjaman sepeda.")

# Load dataset
df = pd.read_csv("all_data.csv")

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

df_filtered = df[(df["dteday"] >= pd.to_datetime(start_date)) & 
                 (df["dteday"] <= pd.to_datetime(end_date))]

st.subheader("Data Peminjaman Sepeda yang Difilter")
st.dataframe(df_filtered.head())

st.subheader("Rata-rata Peminjaman Sepeda per Musim")

df_season = df.groupby("season")["cnt"].mean().reset_index()
season_labels = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
df_season["season_label"] = df_season["season"].map(season_labels)
df_season = df_season.sort_values(by="cnt", ascending=True)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season_label", y="cnt", data=df_season, palette="Blues", ax=ax)
plt.title("Rata-rata Peminjaman Sepeda per Musim", fontsize=14, fontweight="bold")
st.pyplot(fig)

st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")

weather_labels = {
    1: "Cerah/Sedikit Berawan",
    2: "Mendung",
    3: "Hujan Ringan/Salju",
    4: "Cuaca Ekstrem"
}

df["weathersit"] = df["weathersit"].replace(weather_labels)
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
    legend=False
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

st.subheader("Pengaruh Hari Libur terhadap Penyewaan Sepeda")

df_holiday = df.groupby("holiday")["cnt"].mean().reset_index()
holiday_labels = {0: "Hari Kerja", 1: "Hari Libur"}
df_holiday["holiday_label"] = df_holiday["holiday"].map(holiday_labels)
df_holiday = df_holiday.sort_values(by="cnt", ascending=True)

colors = ["#63b3ed", "#2b6cb0"]

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    x="holiday_label",
    y="cnt",
    data=df_holiday,
    hue="holiday_label",
    palette=colors,
    legend=False
)

plt.ylim(0, df_holiday["cnt"].max() * 1.2)

for i, row in enumerate(df_holiday.itertuples()):
    plt.text(i, row.cnt * 1.05, f"{row.cnt:.2f}", ha="center", fontsize=12, fontweight="bold")

plt.title("Pengaruh Hari Libur terhadap Penyewaan Sepeda", fontsize=14, fontweight="bold")
plt.xlabel("Kategori Hari", fontsize=12)
plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
st.pyplot(fig)
