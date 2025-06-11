import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from git import Repo
from dotenv import load_dotenv
import os

load_dotenv()

# Setup browser
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Load data dari Excel
df = pd.read_excel("data.xlsx")

# Hasil akan disimpan ke sini
hasil = []

# Loop tiap baris dan isi form
for index, row in df.iterrows():
    try:
        driver.get("https://bsu.bpjsketenagakerjaan.go.id/")

        # Tunggu sebentar agar page selesai load
        time.sleep(2)

        # Input NIK
        input_nik = driver.find_element(By.ID, "nik")
        input_nik.clear()
        input_nik.send_keys(str(row['NIK']))

        # Input Nama Lengkap
        input_nama = driver.find_element(By.ID, "nama")
        input_nama.clear()
        input_nama.send_keys(str(row['Nama']))

        # Submit
        submit = driver.find_element(By.ID, "btnCek")
        submit.click()

        time.sleep(3)  # Tunggu hasil muncul

        # Ambil hasil
        result = driver.find_element(By.ID, "hasil").text
        print(f"{row['NIK']} - {result}")
        hasil.append({"NIK": row['NIK'], "Nama": row['Nama'], "Hasil": result})

    except Exception as e:
        print(f"Error pada baris {index}: {e}")
        hasil.append({"NIK": row['NIK'], "Nama": row['Nama'], "Hasil": "ERROR"})

# Simpan hasil
hasil_df = pd.DataFrame(hasil)
hasil_df.to_csv("hasil.csv", index=False)

# Git commit & push
repo = Repo(".")
repo.git.add("hasil.csv")
repo.index.commit("Update hasil cek BSU otomatis")
origin = repo.remote(name="origin")
origin.push()
