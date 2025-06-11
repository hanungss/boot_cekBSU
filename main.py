import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Inisialisasi driver (tanpa membuka jendela browser)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Hapus baris ini jika ingin melihat browsernya
driver = webdriver.Chrome(options=chrome_options)

# Baca data dari Excel dan bersihkan header
df = pd.read_excel("data.xlsx", engine="openpyxl")
df.columns = df.columns.str.strip().str.upper()  # Standarisasi header

# List penampung hasil
hasil_list = []

# Loop data peserta
for index, row in df.iterrows():
    driver.get("https://bsu.bpjsketenagakerjaan.go.id/")
    time.sleep(2)

    # Isi form
    driver.find_element(By.ID, "nik-bsu").send_keys(str(row["NIK"]))
    driver.find_element(By.ID, "nama-bsu").send_keys(row["NAMA"].upper())
    tanggal_lahir = pd.to_datetime(row["TANGGALLAHIR"], errors="coerce").strftime("%Y-%m-%d")
    driver.execute_script("document.getElementById('tgl-lahir-bsu').value = arguments[0];", tanggal_lahir)
    driver.find_element(By.ID, "nama-ibu").send_keys(row["NAMAIBU"].upper())
    driver.find_element(By.ID, "nama-ibu-verif").send_keys(row["NAMAIBU"].upper())
    driver.find_element(By.ID, "hp").send_keys(str(row["NOHP"]))
    driver.find_element(By.ID, "hp-verif").send_keys(str(row["NOHP"]))
    driver.find_element(By.ID, "email").send_keys(row["EMAIL"].lower())
    driver.find_element(By.ID, "email-verif").send_keys(row["EMAIL"].lower())

    # Submit form aman
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btn-cek-bsu"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
    time.sleep(1)
    try:
        submit_button.click()
    except:
        driver.execute_script("arguments[0].click();", submit_button)

    time.sleep(3)

    # Ambil hasil
    soup = BeautifulSoup(driver.page_source, "html.parser")
    hasil_elem = soup.select_one("div.respon-bsu h3")
    hasil_text = hasil_elem.get_text(strip=True) if hasil_elem else "Tidak ada hasil ditemukan."

    # Tampilkan di terminal
    print(f"Hasil untuk {row['NIK']} - {row['NAMA']}")
    print(hasil_text)
    print("=" * 30)

    # Tambahkan ke list hasil
    hasil_list.append({
        "NIK": row["NIK"],
        "NAMA": row["NAMA"],
        "HASIL": hasil_text
    })

# Selesai dan simpan ke Excel
hasil_df = pd.DataFrame(hasil_list)
hasil_df.to_excel("hasil_bsu.xlsx", index=False)
print("✅ Semua hasil disimpan ke 'hasil_bsu.xlsx'")

driver.quit()
