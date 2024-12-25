# UAP-Prediksi Hujan


Nama  : bintang primadata putra (202110370311431)

## Overview Project

Project ini dimaksudkan untuk user yang ingin memprediksi hujan pada besok hari, dikarenakan untuk wilayah tropis sering terkendala akan cuaca yanng tifak menentu. project ini dibekali oleh 2 model mechine learning yaitu random forest dan juga XGBosst.

MODEL dan Dataset dapat diakses pada drive : https://drive.google.com/drive/folders/1l5aqcLU_xdMq9tg-MKTp8-T6neV8q28u?usp=drive_link


**RANDOM FOREST**

![image](https://github.com/user-attachments/assets/935fea14-a670-4263-bf92-7f3d5e6f288a)


**CGBOOST**
![image](https://github.com/user-attachments/assets/bcff51de-771e-4be3-94f1-f30e415907b7)



## overview dataset

**heatmap**
![image](https://github.com/user-attachments/assets/4c8180b8-6388-4705-9406-939b142c0bfa)


**distribusi target**
![image](https://github.com/user-attachments/assets/0874d5a9-9cad-4ac3-b636-8ebf6d7c2a85)

## latar belakang
Aplikasi ini bertujuan untuk memprediksi kemungkinan terjadinya hujan esok hari berdasarkan parameter cuaca yang dimasukkan pengguna. Cuaca adalah salah satu faktor yang sangat memengaruhi aktivitas manusia. Ketidakpastian kondisi cuaca, seperti kemungkinan terjadinya hujan, dapat berdampak pada sektor pertanian, transportasi, konstruksi, dan berbagai aspek kehidupan sehari-hari. Oleh karena itu, prediksi cuaca yang akurat menjadi kebutuhan yang sangat penting untuk membantu masyarakat dan sektor industri mengambil keputusan yang tepat.

Seiring dengan perkembangan teknologi, model pembelajaran mesin (machine learning) telah digunakan secara luas untuk memprediksi cuaca. Model ini memiliki kemampuan untuk menganalisis data historis cuaca dan memprediksi kemungkinan cuaca di masa depan dengan tingkat akurasi yang tinggi.

Aplikasi Prediksi Hujan Esok Hari ini dikembangkan untuk memanfaatkan kekuatan model pembelajaran mesin seperti Random Forest dan XGBoost dalam memprediksi kemungkinan terjadinya hujan. Dengan memberikan masukan berupa parameter cuaca seperti suhu, kelembapan, kecepatan angin, dan tekanan udara, aplikasi ini dapat memberikan hasil prediksi yang mudah dipahami serta disertai dengan visualisasi untuk interpretasi model.

Dengan adanya aplikasi ini, diharapkan masyarakat dapat mengambil keputusan yang lebih baik terkait aktivitas mereka, misalnya dalam perencanaan perjalanan, perlindungan properti, atau penjadwalan kegiatan luar ruangan. Aplikasi ini juga memberikan edukasi kepada pengguna tentang bagaimana faktor-faktor cuaca memengaruhi kemungkinan terjadinya hujan melalui interpretasi fitur menggunakan metode SHAP.

# Prediksi Hujan Esok Hari

Aplikasi web ini memprediksi kemungkinan hujan pada hari berikutnya berdasarkan parameter cuaca yang dimasukkan pengguna. Aplikasi ini dibangun menggunakan **Streamlit**, dengan dukungan model pembelajaran mesin seperti **Random Forest** dan **XGBoost**.

## Fitur Utama
1. **Input Parameter Cuaca:**
   - Suhu minimum dan maksimum.
   - Curah hujan.
   - Kecepatan angin kencang.
   - Kelembapan dan tekanan udara.
   - Arah angin dan kondisi hujan hari ini.

2. **Prediksi Hasil:**
   - Prediksi apakah akan hujan esok hari menggunakan Random Forest dan XGBoost.
   - Probabilitas hasil prediksi ditampilkan dalam bentuk grafik.

3. **Interpretasi Model:**
   - Visualisasi interpretasi fitur dengan **SHAP** untuk model Random Forest.
   - Debugging input data dan hasil prediksi untuk XGBoost.

## Teknologi yang Digunakan
- **Streamlit**: Untuk antarmuka pengguna.
- **Scikit-learn**: Implementasi model Random Forest.
- **XGBoost**: Implementasi model XGBoost.
- **SHAP**: Untuk interpretasi model.
- **Matplotlib**: Untuk visualisasi probabilitas prediksi.

## Cara Menggunakan Aplikasi
1. Jalankan aplikasi dengan perintah:
   ```bash
   streamlit run app.py

