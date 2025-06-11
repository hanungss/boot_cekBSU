import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from git import Repo
from dotenv import load_dotenv
import os

load_dotenv()

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

df = pd.read_excel("data.xlsx")

hasil = []

for index, row in df.iterrows():
    try:
        driver.get("https://bsu.bpjsketenagakerjaan.go.id/")
        time.sleep(3)

        # Isi form berdasarkan ID terbaru
        driver.find_element(By.ID, "nik-bsu").send_keys(str(row['NIK']))
        driver.find_element(By.ID, "nama-bsu").send_keys(str(row['Nama']))
        driver.find_element(By.ID, "tgl-lahir-bsu").send_keys(str(row['TanggalLahir']))
        driver.find_element(By.ID, "nama-ibu").send_keys(str(row['NamaIbu']))
        driver.find_element(By.ID, "nama-ibu-verif").send_keys(str(row['NamaIbu']))
        driver.find_element(By.ID, "hp").send_keys(str(row['NoHP']))
        driver.find_element(By.ID, "hp-verif").send_keys(str(row['NoHP']))
        driver.find_element(By.ID, "email").send_keys(str(row['Email']))
        driver.find_element(By.ID, "email-verif").send_keys(str(row['Email']))

        # Submit
        driver.find_element(By.ID, "btn-cek-bsu").click()
        time.sleep(5)

        # Ambil hasil dari notifikasi / hasil cek (jika ada)
        hasil_teks = driver.find_element(By.ID, "hasil").text
        hasil.append({
            "NIK": row['NIK'],
            "Nama": row['Nama'],
            "Hasil": hasil_teks
        })

    except Exception as e:
        print(f"Error baris {index}: {e}")
        hasil.append({
            "NIK": row['NIK'],
            "Nama": row['Nama'],
            "Hasil": "ERROR"
        })

# Simpan hasil ke CSV
pd.DataFrame(hasil).to_csv("hasil.csv", index=False)

# Push ke GitHub
repo = Repo(".")
repo.git.add("hasil.csv")
repo.index.commit("Update hasil cek BSU")
repo.remote(name="origin").push()
