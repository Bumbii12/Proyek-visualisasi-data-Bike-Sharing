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
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Bicycle_icon.svg/512px-Bicycle_icon.svg.png")
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

st.subheader("Rata-rata Peminjaman Sepeda Berdasarkan Kondisi Cuaca")

df_weather = df.groupby("weathersit")["cnt"].mean().reset_index()
weather_labels = {1: "Cerah", 2: "Mendung", 3: "Hujan Ringan"}
df_weather["weather_label"] = df_weather["weathersit"].map(weather_labels)
df_weather = df_weather.sort_values(by="cnt", ascending=True)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="weather_label", y="cnt", data=df_weather, palette="Reds", ax=ax)
st.pyplot(fig)

st.subheader("Dampak Kelembapan terhadap Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=df["hum"], y=df["cnt"], alpha=0.6, color="blue", ax=ax)
sns.regplot(x=df["hum"], y=df["cnt"], scatter=False, color="black", line_kws={"linestyle": "dashed"}, ax=ax)
st.pyplot(fig)

st.subheader("Dampak Kecepatan Angin terhadap Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=df["windspeed"], y=df["cnt"], alpha=0.6, color="red", ax=ax)
sns.regplot(x=df["windspeed"], y=df["cnt"], scatter=False, color="black", line_kws={"linestyle": "dashed"}, ax=ax)
st.pyplot(fig)
