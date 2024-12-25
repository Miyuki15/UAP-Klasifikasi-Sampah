import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import logging
import shap

# Konfigurasi Streamlit
st.set_page_config(page_title="Prediksi Hujan Besok", layout="wide")

# Logging
logging.basicConfig(level=logging.INFO)

# Fungsi untuk memuat model
@st.cache_resource
def load_model(model_path):
    return joblib.load(model_path)

@st.cache_resource
def load_scaler(scaler_path):
    return joblib.load(scaler_path)

# Load model dan scaler
try:
    rf_model = load_model('random_forest_model.h5')
    xgb_model = load_model('xgboost_model.h5')
    scaler = load_scaler('scaler.pkl')  # Pastikan scaler disimpan selama praproses
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat model atau scaler: {e}")

# Judul aplikasi
st.title('Prediksi Hujan Besok')
st.markdown("Masukkan informasi cuaca untuk memprediksi apakah akan terjadi hujan esok hari.")

# Input manual dari pengguna
MinTemp = st.number_input('Suhu Minimum (°C)', value=10.0, step=0.1)
MaxTemp = st.number_input('Suhu Maksimum (°C)', value=25.0, step=0.1)
Rainfall = st.number_input('Curah Hujan (mm)', value=0.0, step=0.1)
WindGustSpeed = st.number_input('Kecepatan Angin Kencang (km/jam)', value=35.0, step=0.1)
Humidity9am = st.number_input('Kelembapan pada 9am (%)', value=75.0, step=0.1)
Humidity3pm = st.number_input('Kelembapan pada 3pm (%)', value=55.0, step=0.1)
Pressure9am = st.number_input('Tekanan Udara pada 9am (hPa)', value=1012.0, step=0.1)
Pressure3pm = st.number_input('Tekanan Udara pada 3pm (hPa)', value=1010.0, step=0.1)
Temp9am = st.number_input('Suhu pada 9am (°C)', value=20.0, step=0.1)
Temp3pm = st.number_input('Suhu pada 3pm (°C)', value=25.0, step=0.1)
WindGustDir = st.selectbox('Arah Angin Kencang', options=['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW'])
WindDir9am = st.selectbox('Arah Angin pada 9am', options=['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW'])
WindDir3pm = st.selectbox('Arah Angin pada 3pm', options=['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW'])
RainToday = st.selectbox('Hujan Hari Ini', options=['Yes', 'No'])

# Validasi input
if Rainfall < 0 or not (0 <= Humidity9am <= 100) or not (0 <= Humidity3pm <= 100):
    st.error("Pastikan nilai input logis: Curah Hujan tidak boleh negatif, dan Kelembapan harus antara 0-100%.")
else:
    # Encoding input kategorikal
    dir_mapping = {'N': 0, 'S': 1, 'E': 2, 'W': 3, 'NE': 4, 'NW': 5, 'SE': 6, 'SW': 7}
    WindGustDir = dir_mapping[WindGustDir]
    WindDir9am = dir_mapping[WindDir9am]
    WindDir3pm = dir_mapping[WindDir3pm]
    RainToday = 1 if RainToday == 'Yes' else 0

    # Membuat array input
    features = np.array([[MinTemp, MaxTemp, Rainfall, WindGustSpeed, Humidity9am, Humidity3pm,
                          Pressure9am, Pressure3pm, Temp9am, Temp3pm, WindGustDir, WindDir9am,
                          WindDir3pm, RainToday]])

    # Tambahkan placeholder jika jumlah fitur tidak sesuai
    num_missing_features = scaler.n_features_in_ - features.shape[1]
    if num_missing_features > 0:
        placeholders = np.zeros((features.shape[0], num_missing_features))
        features = np.hstack([features, placeholders])

    # Standardisasi data
    try:
        features_scaled = scaler.transform(features)
        st.write("Fitur berhasil distandardisasi.")
    except Exception as e:
        st.error(f"Kesalahan dalam standardisasi data: {e}")

    # Tombol prediksi
    if st.button('Prediksi Hujan esok hari'):
        # Random Forest
        rf_probabilities = rf_model.predict_proba(features_scaled)[0]
        rf_prediction = rf_model.predict(features_scaled)[0]
        rf_result = 'Akan Hujan Besok' if rf_prediction == 1 else 'Tidak Akan Hujan Besok'
        st.write(f"Prediksi (Random Forest): {rf_result}")

        # Visualisasi Probabilitas Random Forest
        st.subheader("Probabilitas Prediksi (Random Forest)")
        fig_rf, ax_rf = plt.subplots()
        classes_rf = ['Tidak Hujan', 'Hujan']
        ax_rf.bar(classes_rf, rf_probabilities, color=['blue', 'orange'])
        ax_rf.set_title("Probabilitas Prediksi")
        ax_rf.set_ylabel("Probabilitas")
        ax_rf.set_ylim([0, 1])
        for i, v in enumerate(rf_probabilities):
            ax_rf.text(i, v + 0.02, f"{v:.2f}", ha='center')
        st.pyplot(fig_rf)
        
        # SHAP Interpretasi untuk Random Forest
        try:
            st.subheader("SHAP untuk Random Forest")
            rf_explainer = shap.TreeExplainer(rf_model)
            rf_shap_values = rf_explainer.shap_values(features_scaled)
            shap.initjs()
            shap.waterfall_plot(shap.Explanation(
                values=rf_shap_values[0][0],
                base_values=rf_explainer.expected_value[0],
                feature_names=[
                    'MinTemp', 'MaxTemp', 'Rainfall', 'WindGustSpeed', 'Humidity9am',
                    'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Temp9am', 'Temp3pm',
                    'WindGustDir', 'WindDir9am', 'WindDir3pm', 'RainToday'
                ],
                data=features_scaled[0]
            ))
            st.pyplot(plt)
        except Exception as e:
            st.error(f"Kesalahan dalam interpretasi SHAP (Random Forest): {e}")

        # XGBoost
        try:
            st.subheader("Hasil Prediksi XGBoost")
            xgb_probabilities = xgb_model.predict_proba(features_scaled)[0]
            xgb_prediction = xgb_model.predict(features_scaled)[0]

            # Debugging jika hasil selalu sama
            st.write("Probabilitas (XGBoost):", xgb_probabilities)
            st.write("Prediksi (XGBoost):", xgb_prediction)

            # Validasi probabilitas
            if not (0 <= xgb_probabilities[0] <= 1 and 0 <= xgb_probabilities[1] <= 1):
                st.warning("Probabilitas XGBoost tidak valid. Periksa model atau input data.")

            xgb_result = 'Akan Hujan Besok' if xgb_prediction == 1 else 'Tidak Akan Hujan Besok'
            st.write(f"Prediksi (XGBoost): {xgb_result}")

            # Visualisasi Probabilitas XGBoost
            fig_xgb, ax_xgb = plt.subplots()
            classes_xgb = ['Tidak Hujan', 'Hujan']
            ax_xgb.bar(classes_xgb, xgb_probabilities, color=['green', 'red'])
            ax_xgb.set_title("Probabilitas Prediksi")
            ax_xgb.set_ylabel("Probabilitas")
            ax_xgb.set_ylim([0, 1])
            for i, v in enumerate(xgb_probabilities):
                ax_xgb.text(i, v + 0.02, f"{v:.2f}", ha='center')
            st.pyplot(fig_xgb)
        except Exception as e:
            st.error(f"Kesalahan prediksi XGBoost: {e}")

        # Debugging untuk memastikan input sesuai
        if st.checkbox("Debugging"):
            st.write("Input Data (Sebelum Standardisasi):", features)
            st.write("Input Data (Setelah Standardisasi):", features_scaled)

# Tentang aplikasi
st.sidebar.header("Tentang Aplikasi")
st.sidebar.write("""
Aplikasi ini bertujuan untuk memprediksi kemungkinan terjadinya hujan esok hari berdasarkan parameter cuaca yang dimasukkan pengguna.

Model yang digunakan:
- *Random Forest*: Dengan visualisasi interpretasi fitur menggunakan SHAP.
- *XGBoost*: Dengan visualisasi menggunakan Feature Importance dan Partial Dependence Plot (PDP).

### Cara Penggunaan
1. Masukkan parameter cuaca pada form input di halaman utama.
2. Klik tombol "Prediksi Hujan Esok Hari" untuk mendapatkan hasil prediksi.
3. Lihat visualisasi probabilitas untuk memahami hasil prediksi.

### Teknologi
Aplikasi ini dibangun menggunakan:
- *Scikit-learn*: Untuk implementasi model Random Forest.
- *XGBoost*: Untuk implementasi model XGBoost.
- *SHAP*: Untuk interpretasi model Random Forest.
- *Streamlit*: Untuk pengembangan antarmuka aplikasi web.

""")
