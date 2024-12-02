# -*- coding: utf-8 -*-
"""submission_akhir_2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1l1dOx7XuIr38pcHvW9z5ipgJYYezFLAc

# Laporan Proyek Machine Learning - Aryaputra Maheswara

---

## Project Overview

---

Anime merupakan salah satu bentuk hiburan yang sangat populer di berbagai kalangan, baik anak-anak, remaja, maupun dewasa. Sebagai medium seni visual yang menggabungkan cerita mendalam, visual yang menawan, dan musik yang memikat, anime memiliki daya tarik yang kuat bagi para penggemarnya. Namun, seiring dengan pertumbuhan industri anime, jumlah judul yang tersedia di berbagai platform semakin meningkat, menciptakan tantangan bagi pengguna dalam menemukan anime yang sesuai dengan preferensi mereka.

Rekomendasi anime menjadi solusi untuk membantu pengguna menemukan anime yang relevan dengan minat mereka. Teknologi modern, seperti sistem rekomendasi berbasis kecerdasan buatan, memungkinkan pengalaman yang lebih personal dalam memilih anime. Salah satu metode yang dapat digunakan adalah content-based filtering, yang memanfaatkan data dari fitur atau karakteristik anime untuk menemukan kesamaan antara satu anime dengan yang lain.

#### Mengapa Proyek Ini Perlu Diselesaikan?
1. Pertumbuhan Industri Anime: Ukuran pasar global anime diperkirakan mencapai USD 31,23 miliar pada tahun 2023 dan diproyeksikan tumbuh dengan laju tahunan gabungan (CAGR) sebesar 9,8% dari tahun 2024 hingga 2030. Permintaan yang terus meningkat terhadap konten anime Jepang, distribusi berbasis internet, serta aplikasi game menjadi pendorong utama ekspansi pasar ini [Anime Market Size, Share, Growth And Trends Report, 2024](https://www.who.int/news-room/fact-sheets/detail/diabetes) [1].
2. Kepuasan Pengguna: Pengalaman pengguna sangat dipengaruhi oleh relevansi konten yang direkomendasikan. Studi menunjukkan bahwa algoritma berbasis konten dapat meningkatkan personalisasi dan kepuasan pengguna [2].
3. Efisiensi dalam Penemuan Konten: Tanpa sistem rekomendasi yang efisien, pengguna sering kali menghabiskan waktu yang lama untuk mencari anime yang mereka sukai, yang dapat menurunkan tingkat keterlibatan mereka [3].
4. Pemanfaatan Data yang Tersedia: Data deskriptif seperti genre, deskripsi, dan karakteristik anime lainnya dapat dimanfaatkan untuk menghasilkan rekomendasi yang akurat [4].

## Business Understanding

---

### Problem Statement

* Apa genre anime yang paling populer di seluruh kalangan?
* Anime apa yang paling populer dan disukai di dalam data tersebut?
* Apakah ada hubungan antar variabel pada dataset yang data diintepretasikan?
* Bagaimana cara membuat sistem rekomendasi anime?

### Goals

* Mengetahui genre anime yang paling populer serta mencari hubungan antar variabel yang berkaitan dengan anime
* Membuat sistem rekomendasi yang dapat merekomendasikan anime yang relevan
* Menggunakan algoritma cosine similarity untuk membuat sistem rekomendasi, lalu mengevaluasi menggunakan metriks precission untuk menjamin keakuratan sistem rekomendasi.

### Solution Approach

* Mengimplementasikan Exploratory Data Analysis (EDA) untuk analisis dan visualisasi data.
* Mengimplementasikan content-based filtering approach menggunakan algoritma cosine similarity.

## Data Loading
"""

import os
import zipfile

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack

import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('mode.chained_assignment', None)  # Disable warning

exists = os.path.exists('anime-recommendation-database-2020.zip')
if not exists:
    !kaggle datasets download hernan4444/anime-recommendation-database-2020
else:
    print('Dataset is downloaded!')

exists = os.path.exists('anime.csv')
if not exists:
    with zipfile.ZipFile('anime-recommendation-database-2020.zip', 'r') as zip_ref:
        zip_ref.extractall()
else:
    print('Data is extracted!')

anime = pd.read_csv('anime.csv')
anime_sinopsis = pd.read_csv('anime_with_synopsis.csv')

"""# Data Understanding

Dataset yang digunakan adalah data Anime yang tersedia pada website kaggle yang dapat di akses pada link [Berikut ini](https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset), dataset ini berisi data Anime yang di scarping pada website MyAnimeList di tahun 2020 dengan jumlah baris dan kolom sebanyak 17562 baris dan 35 kolom untuk anime.csv dan 16214 baris dan 5 kolom untuk anime_with_synopsis.csv.
"""

anime.shape

"""Dataset anime.csv berisi memiliki 35 variabel dengan keterangan sebagai berikut :

| Variabel | Keterangan |
|----------|------------|
| MAL_ID |  ID Anime yang tersimpan pada MyAnimeList (e.g. 1)|
| Name | Nama lengkap dari anime |
| Score | Rata-rata skor anime yang diberikan oleh user MyAnimeList. (e.g 8,78) |
| Genres | List dari genre yang ada pada 1 judul anime yang dipisahkan oleh koma (e.g Action, Comedy, Drama) |
| English name | Judul anime dalam bahasa inggris |
| Japanese name | Judul anime dalam bahasa Jepang |
| Type | Tipe anime (e.g TV, Movie, OVA) |
| Episodes | Jumlah episode |
| Aired | Tanggal Penayangan (e.g. Apr 3, 1998 to Apr 24, 1999) |
| Premiered | Musim tayang (e.g Spring 1998) |
| Produces | List dari produser anime |
| Licensors | List dari pemberi lisensi anime |
| Studios | List dari studio anime |
| Source | Sumber dari anime (e.g Manga) |
| Duration | Durasi anime per episode (e.g 24 min. per ep.) |
| Rating | Rating umur (e.g. R - 17+ (violence & profanity)) |
| Ranked | Posisi anime berdasarkan skor |
| Popularity | Posisi berdasarkan jumlah user yang menyimpan anime ke dalam list mereka |
| Members | Jumlah member komunitas yang ada pada grup anime ini |
| Favorites | Jumlah user yang menandai anime sebagai favorite |
| Watching | Jumlah user yang sedang menonton anime |
| Completed | Jumlah user yang telah menamatkan anime |
| On-Hold | Jumlah user yang menunda menonton anime |
| Dropped | Jumlah user yang tidak melanjutkan menonton anime |
| Plan to Watch | Jumlah user yang berencana menonton anime |
| Score-10 | Jumlah user yang memberikan skor 10 |
| Score-9 | Jumlah user yang memberikan skor 9 |
| Score-8 | Jumlah user yang memberikan skor 8 |
| Score-7 | Jumlah user yang memberikan skor 7 |
| Score-6 | Jumlah user yang memberikan skor 6 |
| Score-5 | Jumlah user yang memberikan skor 5 |
| Score-4 | Jumlah user yang memberikan skor 4 |
| Score-3 | Jumlah user yang memberikan skor 3 |
| Score-2 | Jumlah user yang memberikan skor 2 |
| Score-1 | Jumlah user yang memberikan skor 1 |
"""

anime_sinopsis.shape

"""Dataset anime_with_synopsis.csv berisi memiliki 5 variabel dengan keterangan sebagai berikut :

| Variabel | Keterangan |
|----------|------------|
| MAL_ID |  ID Anime yang tersimpan pada MyAnimeList (e.g. 1)|
| Name | Nama lengkap dari anime |
| Score | Rata-rata skor anime yang diberikan oleh user MyAnimeList. (e.g 8,78) |
| Genres | List dari genre yang ada pada 1 judul anime yang dipisahkan oleh koma (e.g Action, Comedy, Drama) |
| sypnopsis | Sinopsis dari anime |

## Exploratory Data Analysis
"""

anime.info()

anime.describe()

"""Data anime :
1. MAL_ID memiliki 17562 data, tetapi ID maksimal mencapai 48492, artinya terdapat beberapa ID yang tidak ada pada dataset ini
2. Nilai Popularity, Favorites, Watching, Completed, On-Hold, Dropped minimum adalah nol, artinya data tersebut adalah missing value, karena nilai minimum seharusnya adalah 1

---

### Cek value Unknown
"""

anime.isna().sum()

"""Tidak ada data bernilai NULL"""

# Check for "Unknown" values in each column and count them
unknown_count = anime.apply(lambda col: col.isin(['Unknown']).sum())

print(unknown_count)

"""Data tidak ada yang bernilai null, tetapi ada cukup banyak data yang bernilai Unknown

### Top 10 Popular Anime
"""

data_eda = anime[['MAL_ID','Name', 'Score', 'Type', 'Episodes', 'Rating', 'Genres', 'Ranked', 'Popularity', 'Favorites']]
data_popularity = data_eda[data_eda['Popularity'] >= 1]
data_popularity

# Filter top 10 anime berdasarkan popularitas (nilai Popularity terkecil)
top_10_popular_anime = data_popularity.sort_values(by='Popularity', ascending=True).head(10)

# Visualisasi top 10 anime paling populer
plt.figure(figsize=(10, 6))
sns.barplot(data=top_10_popular_anime, x='Name', y='Popularity', palette='coolwarm')
plt.title('Top 10 Anime Paling Populer Berdasarkan Popularitas', fontsize=14)
plt.xlabel('Nama Anime', fontsize=12)
plt.ylabel('Popularitas (Semakin Kecil Semakin Populer)', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.tight_layout()
plt.show()

top_10_popular_anime

"""Anime paling populer pada tahun 2020 adalah anime Death Note dengan jumlah favorites sebanyak 145.201"""

# Urutkan berdasarkan Favorites dan ambil Top 10
top_10_favorites_anime = data_popularity.sort_values(by='Favorites', ascending=False).head(10)

# Visualisasi Top 10 berdasarkan Favorites
plt.figure(figsize=(10, 6))
sns.barplot(data=top_10_favorites_anime, x='Name', y='Favorites', palette='coolwarm')
plt.title('Top 10 Anime Berdasarkan Favorites', fontsize=14)
plt.xlabel('Nama Anime', fontsize=12)
plt.ylabel('Favorites (Jumlah)', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.tight_layout()
plt.show()

# Tampilkan data Top 10 Favorites
top_10_favorites_anime

"""Anime yang paling disukai pada tahun 2020 adalah Fullmetal Alchemist: Brotherhood	dengan jumlah favorites sebanyak 183.914

**Insights yang Dapat Diperoleh**
* Korelasi Popularitas dengan Favorites:

    Anime dengan nilai Favorites tinggi kemungkinan besar memiliki nilai Popularity kecil (sangat populer).
* Identifikasi Anime Ikonik:

    Anime dengan Favorites tertinggi biasanya dianggap ikonik atau memiliki komunitas penggemar yang besar.

---

### Data Cleaning

### Memvisualisasikan data yang kosong pada setiap fitur

Memilih fitur yang akan digunakan oleh model recommender system nantinya
"""

data_anime = anime[['MAL_ID','Name', 'Score', 'Type', 'Episodes', 'Rating', 'Genres']].copy()
data_anime.info()

data_anime.isna().sum()

data_anime.duplicated().sum()

data_anime['MAL_ID'].nunique()

"""Seluruh data MAL_ID sudah unik dan tidak ada yang duplikat"""

unknown_count = data_anime.apply(lambda col: col.isin(['Unknown']).sum())

print(unknown_count)

# Visualization
plt.figure(figsize=(10, 6))
sns.barplot(x=unknown_count.index, y=unknown_count.values)
plt.title("Count of 'Unknown' Values per Column", fontsize=16)
plt.xlabel("Column", fontsize=14)
plt.ylabel("Count of 'Unknown'", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.show()

"""drop data yang bernilai unknown"""

# Drop rows with 'Unknown' values
data_anime_cleaned = data_anime.loc[~data_anime.isin(['Unknown']).any(axis=1)]

# Display the cleaned DataFrame
data_anime_cleaned = data_anime_cleaned.reset_index(drop=True)
data_anime_cleaned

unknown_count = data_anime_cleaned.apply(lambda col: col.isin(['Unknown']).sum())

print(unknown_count)

data_anime_cleaned.info()

data_anime_cleaned['Episodes'] = data_anime_cleaned['Episodes'].astype(int)
data_anime_cleaned['Score'] = data_anime_cleaned['Score'].astype(float)
data_anime_cleaned.info()

data_anime_cleaned.describe()

"""---

### Jumlah Rating
"""

# Menghitung jumlah anime berdasarkan rating nya
rating_counts = data_anime_cleaned['Rating'].value_counts()
print(rating_counts)

# Bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x=rating_counts.index, y=rating_counts.values, palette="viridis")
plt.title("Menghitung jumlah anime berdasarkan rating", fontsize=16)
plt.xlabel("Rating", fontsize=14)
plt.ylabel("Count", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.show()

"""Dari data diatas, Rating dengan jumlah tertinggi adalah PG-13 dengan jumlah sebanyak 5435

### Korelasi score dengan rating anime
"""

# Box plot to compare Scores by Rating
plt.figure(figsize=(10, 6))
sns.boxplot(data=data_anime_cleaned, x="Rating", y="Score")
plt.title("Score Distribution by Rating", fontsize=16)
plt.xlabel("Rating", fontsize=14)
plt.ylabel("Score", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.show()

"""Dari gambar diatas dapat disimpulkan :
* Score anime dengan rata - rata paling tinggi adalah anime dengan rating R-17+ dengan rata - rata 7.2, artinya anime dengan rating R lebih disukai
* Anime dengan score rata - rata yang paling kecil adalah anime dengan rating G - All Ages
* Anime dengan rating PG-13 memiliki penyebaran rating yang paling banyak, artinya anime dengan rating PG-13 memiliki perbedaan kualitas

### Analisis Genre
"""

genres = []
genre_anime = data_anime_cleaned['Genres'].unique()
for genre in genre_anime:
    array_genre = genre.split(',')
    [genres.append(x) for x in array_genre if x not in genres]
print('Jumlah Genre : ',len(genres))

# One-hot encoding genres
genres_split = data_anime_cleaned['Genres'].str.get_dummies(sep=', ')
genres_split['Type'] = data_anime_cleaned['Type']

# Grouping genres berdasarkan Type
genre_counts = genres_split.groupby('Type').sum().T

# Stacked bar chart
genre_counts.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title("Genres Distribution by Type", fontsize=16)
plt.xlabel("Genres", fontsize=14)
plt.ylabel("Count", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend(title="Type", fontsize=12)
plt.show()

from collections import Counter

# Memisahkan genre
genre_list = data_eda['Genres'].str.split(', ').explode()
genre_count = Counter(genre_list)

# Visualisasi
sns.barplot(x=list(genre_count.values()), y=list(genre_count.keys()), palette='muted')
plt.title('Frekuensi Genre Anime')
plt.xlabel('Frekuensi')
plt.ylabel('Genre')
plt.show()

# Pisahkan genre menjadi daftar individual
genres_popularity = data_eda.assign(Genres=data_eda['Genres'].str.split(', ')).explode('Genres')

# Hitung rata-rata popularitas untuk setiap genre
genre_popularity = genres_popularity.groupby('Genres').agg(
    avg_popularity=('Popularity', 'mean'),
    anime_count=('Popularity', 'count')
).sort_values(by='avg_popularity', ascending=True)

# Visualisasi genre dengan rata-rata popularitas terendah
plt.figure(figsize=(14, 8))
sns.barplot(
    x=genre_popularity['avg_popularity'],
    y=genre_popularity.index,
    palette='coolwarm'
)
plt.title('Genre Anime yang Paling Populer (Rata-rata Popularitas)', fontsize=16)
plt.xlabel('Rata-rata Popularitas (Semakin Kecil Semakin Baik)', fontsize=12)
plt.ylabel('Genre', fontsize=12)

# Tambahkan anotasi jumlah anime
for i, count in enumerate(genre_popularity['anime_count']):
    plt.text(
        genre_popularity['avg_popularity'].iloc[i] + 50,
        i,
        f"{count} anime",
        va='center',
        fontsize=10,
        color='black'
    )

plt.tight_layout()
plt.show()

"""Dari data diatas, dapat disimpulkan bahwa:
* Anime dengan genre komedi merupakan anime dengan jumlah yang paling banyak, yaitu 6029 anime
* Anime dengan genre harem memiliki rata - rata popularitas yang lebih tinggi meskipun memiliki jumlah anime yang lebih sedikit dari yang lainnya dengan jumlah sebanyak 399 anime
* Sedangkan anime dengan genre Kids memiliki rata - rata popularitas yang paling kecil

---

### Distribusi Anime Berdasarkan Tipe
"""

print('Kategori tipe anime : ',data_anime_cleaned['Type'].value_counts())

# Hitung jumlah anime berdasarkan tipe
anime_type_counts = data_anime_cleaned['Type'].value_counts()

# Visualisasi dengan barplot
plt.figure(figsize=(10, 6))
sns.barplot(x=anime_type_counts.index, y=anime_type_counts.values, palette='viridis')
plt.title('Distribusi Anime Berdasarkan Tipe', fontsize=14)
plt.xlabel('Tipe Anime', fontsize=12)
plt.ylabel('Jumlah Anime', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

"""Dari gambar diatas, dapat diketahui:
* Terdapat 6 tipe anime, yaitu TV, OVA, Movie, Special, ONA, Music
* Anime dengan tipe TV memiliki jumlah yang paling banyak, sebanyak 3761 anime

---

## Data Preparation

### Content Based Filtering

Untuk content-based filtering, kita akan fokus pada MAL_ID, Name, Score, Type, Episodes, Rating, Genres, dan sypnopsis

### Mengecek value kosong di data anime dengan sinopsis
"""

anime_sinopsis

anime_sinopsis.isna().sum()

# Menghitung value 'Unknown' di setiap kolom
unknown_counts_per_column = anime_sinopsis.isin(['Unknown']).sum()

# Visualize dengan a bar chart
plt.figure(figsize=(8, 6))
unknown_counts_per_column.plot(kind='bar', color='lightcoral')
plt.title("Count of 'Unknown' Values in Each Column")
plt.xlabel("Columns")
plt.ylabel("Count of 'Unknown' Values")
plt.xticks(rotation=45)
plt.show()

# Also, count the total 'Unknown' values in the entire DataFrame
total_unknown_count = unknown_counts_per_column.sum()
print(f"Total 'Unknown' values in the DataFrame: {total_unknown_count}")

"""Karena sinopsis tidak ada yang bernilai 'Unknown' maka di abaikan

### Drop Value Kosong pada data sinopsis
"""

anime_sinopsis_cleaned = anime_sinopsis.copy().dropna()

data_anime_cleaned_copy = data_anime_cleaned.copy()

"""### Merge data sinopsis ke dalam data anime general berdasarkan MAL_ID"""

# Merge ke dua dataframe dengan menggunakan 'MAL_ID'
merged_df = pd.merge(data_anime_cleaned_copy, anime_sinopsis_cleaned[['MAL_ID','sypnopsis']], on='MAL_ID', how='left')

merged_df[merged_df['sypnopsis'].isna()]

merged_df.fillna('', inplace=True)

merged_df.isna().sum()

data_anime_cleaned = merged_df

data_anime_cleaned.shape

"""---"""

# Inisialisasi TfidfVectorizer
tf = TfidfVectorizer()

"""Mentranformasikan data Genre dan sinopsis ke bentuk matrix dengan menggunakan tfidfVectorizer()"""

# TF-IDF untuk Genres
tfidf_matrix = tf.fit_transform(data_anime_cleaned["Genres"])

# Menyimpan feature name dari Genres
genres_features = tf.get_feature_names_out()

# TF-IDF untuk synopsis (fill missing value demgan empty strings)
tfidf_matrix2 = tf.fit_transform(data_anime_cleaned["sypnopsis"].fillna(''))

# Menyimpan feature name dari sypnopsis
synopsis_features = tf.get_feature_names_out()

# Combine feature name dari kedua fitur
combined_features = list(genres_features) + list(synopsis_features)

"""menggabungkan matriks genre dengan matriks sinopsis menjadi 1"""

# Combine ke dalam 1 matrix
final_features = hstack([tfidf_matrix, tfidf_matrix2])

# Membentuk tabel dari judul lagu beserta genrenya berdasarkan tfidf
pd.DataFrame(
    final_features.todense(),
    columns = combined_features,
    index = data_anime_cleaned['Name']
)

"""## Modelling

Menggunakan cosine similarity untuk mencari kemiripan anime
"""

# Cosine Similarity
cosine_sim = cosine_similarity(final_features)

"""Setelah itu, akan dibuat tabel berisi cosine similarity antar anime."""

# Membuat dataframe dari variabel cosine_sim dengan baris dan kolom berupa judul anime
cosine_sim_df = pd.DataFrame(cosine_sim, index = data_anime_cleaned["Name"], columns = data_anime_cleaned["Name"])
print('Shape:', cosine_sim_df.shape)

# Melihat similarity matrix pada setiap anime
cosine_sim_df.sample(10, axis = 1).sample(10, axis = 0)

"""Setelah dibentuk tabel cosine similarity, selanjutnya akan dibuat fungsi untuk menentukan rekomendasi musik berdasarkan content-based filtering.

---

### Pengujian Sistem Rekomendasi

deklarasi dataframe yang akan dijadikan output
"""

# Dataframe yang akan dijadikan output top - n recommendation
data_output = data_anime_cleaned[['MAL_ID','Name', 'Score', 'Type', 'Episodes', 'Rating', 'Genres', 'sypnopsis']].copy()

# Fungsi untuk mendapatkan rekomendasi top N berdasarkan judul anime

def get_top_n_recommendations_by_name(anime_name, n=10):
    # Mendapatkan index anime dari judul anime
    idx = data_anime_cleaned[data_anime_cleaned['Name'] == anime_name].index[0]

    # Mendapatkan similarity score dari judul anime
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sorting anime berdasarkan similarity score secara descending
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Mendapatkan top n anime, tanpa memasukkan judul yang di input
    sim_scores = sim_scores[1:n+1]

    # Mendapatkan index dari anime dan similarity score nya
    anime_indices = [i[0] for i in sim_scores]
    similarity_scores = [i[1] for i in sim_scores]

    # Mendapatkan full data anime berdasarkan data_output
    recommended_animes = data_output.iloc[anime_indices]

    # Menambahkan kolom nilai similarity score
    recommended_animes['similarity_score'] = similarity_scores

    return recommended_animes.reset_index().drop(columns='index')

# Inferensi top 10 reccomendation
anime_name_to_infer = "Darling in the FranXX"
top_recommendations = get_top_n_recommendations_by_name(anime_name=anime_name_to_infer, n=10)
print("Top 10 Recommendations with Full Anime Data:")
top_recommendations

"""## Evaluasi

Pada proyek ini, metrik evaluasi yang digunakan adalah precision. Precision mengukur seberapa akurat rekomendasi yang diberikan oleh sistem, yaitu proporsi dari item yang direkomendasikan yang benar-benar relevan. Dalam konteks sistem rekomendasi berbasis konten untuk anime, precision menunjukkan seberapa banyak anime yang direkomendasikan kepada pengguna yang sesuai dengan preferensi atau minat mereka.

---

Fungsi untuk evaluasi, jika similarity score diatas 0.5 maka akan dianggap relevan, kemudian di lakukan perhitungan dari total_item_relevan/total_item_yang_direkomendasikan untuk menghitung precission nya
"""

def evaluasi(top_recommendations, n=10):
    count = 0
    for score in top_recommendations['similarity_score']:
        if score > 0.5:
                count+=1
    precission = (count / n)
    # print(f'Precission : {precission} ({precission*100}%)')
    return precission

"""Melakukan evaluasi terhadap 5 judul anime kemudian di rata - rata untuk melihat hasil akhir nya"""

data_akhir = []

anime_names = ['Gintama', 'Naruto', 'Bleach', 'Log Horizon: Entaku Houkai', 'Majo no Tabitabi']

for judul in anime_names:
    top_recommendations = get_top_n_recommendations_by_name(anime_name=judul, n=10)
    precission = evaluasi(top_recommendations, 10)
    print("Top 10 Recommendations : ", judul)
    print('Precission : ', precission)
    # top_recommendations
    data_akhir.append(precission)

x = 0
for i in data_akhir:
    x+=i


print('Rata - rata  Precission dari 5 Judul: ', x/len(data_akhir))

"""Dari data diatas didapatkan rata - rata nilai precission adalah 0.86 yang bisa dibilang cukup bagus, namun nilai tersebut akan berubah-ubah tergantung dengan preferensi dari user.

## Kesimpulan

---

1. Genre komedi merupakan genre yang paling favorit di kalangan penggemar anime, dibuktikan dengan memiliki jumlah anime terbanyak yaitu 6029 anime, meskipun genre ini memiliki variasi popularitas yang lebih rendah dibandingkan genre lainnya.
2. Anime Fullmetal Alchemist: Brotherhood merupakan anime paling ikonik di kalangan penggemar, dibuktikan dengan memiliki nilai Favorites tertinggi, meskipun anime Death Note lebih populer di tahun 2020.

3. Terdapat beberapa variabel yang berkorelasi, yaitu sebagai berikut:

    * Variabel genre dan popularitas:

        * Genre harem berkorelasi positif yang cukup kuat terhadap popularitas. Meskipun memiliki jumlah anime yang lebih sedikit (399 anime), anime dengan genre ini memiliki rata-rata popularitas yang lebih tinggi, menunjukkan bahwa genre ini lebih disukai oleh kalangan tertentu.
        
        * Sebaliknya, genre kids berkorelasi negatif dengan popularitas karena anime dengan genre ini memiliki rata-rata popularitas yang lebih rendah dibandingkan genre lainnya.
    * Variabel rating dan skor:

        * Variabel rating berkorelasi positif yang kuat terhadap score anime. Anime dengan rating R-17+ memiliki rata-rata skor tertinggi (7.2), menunjukkan bahwa anime dengan rating ini lebih disukai dan mendapatkan lebih banyak apresiasi.
        * Sebaliknya, anime dengan rating G - All Ages berkorelasi negatif dengan skor, karena anime dengan rating ini memiliki rata-rata skor yang lebih rendah, menandakan bahwa anime untuk semua usia cenderung kurang disukai secara umum.
    * Variabel tipe anime dan jumlah anime:

        * Tipe anime TV berkorelasi positif dengan jumlah anime terbanyak (3761 anime), menandakan bahwa format serial televisi menjadi pilihan utama dalam produksi anime.

4. Sistem rekomendasi anime dapat diimplementasikan dengan menggunakan pendekatan Content-based filtering menggunakan cosine similarity untuk memberikan rekomendasi berdasarkan preferensi pengguna.

### Referensi

---

[1] Grand View Research, "Anime Market Size, Share & Trends Analysis Report By Type (T.V., Movie, Video, Internet Distribution), By Genre, By Demographics, By Region, And Segment Forecasts, 2024 - 2030," 2023. [Online]. Available: https://www.grandviewresearch.com/industry-analysis/anime-market.

[2] R. Burke, "Hybrid recommender systems: Survey and experiments," User Modeling and User-Adapted Interaction, vol. 12, no. 4, pp. 331–370, Nov. 2002, doi: 10.1023/A:1021240730564.

[3] M. Pazzani and D. Billsus, "Content-based recommendation systems," in The Adaptive Web: Methods and Strategies of Web Personalization, Berlin, Heidelberg: Springer, 2007, pp. 325–341, doi: 10.1007/978-3-540-72079-9_10.

[4] X. Su and T. M. Khoshgoftaar, "A survey of collaborative filtering techniques," Advances in Artificial Intelligence, vol. 2009, pp. 1–19, 2009, doi: 10.1155/2009/421425.
"""