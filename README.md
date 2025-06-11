
# 🛠️ boot_cekBSU

Script otomatis untuk mengisi dan submit form pengecekan BSU (Bantuan Subsidi Upah) dari BPJS Ketenagakerjaan menggunakan data dari file Excel, lalu menyimpan hasilnya ke file CSV.

## 📌 Fitur
- Membaca data peserta dari Excel
- Mengisi form BSU di [https://bsu.bpjsketenagakerjaan.go.id/](https://bsu.bpjsketenagakerjaan.go.id/)
- Submit form dan ambil hasilnya
- Simpan hasil ke `hasil.csv`

## 📁 Struktur File
```
.
├── data.xlsx         # Data input peserta (wajib)
├── hasil.csv         # File hasil pengecekan
├── main.py           # Script utama
├── .env              # File environment (jika diperlukan)
└── README.md         # Dokumentasi ini
```

## 📥 Format Excel (`data.xlsx`)

| NIK         | Nama Lengkap | TanggalLahir | NamaIbu        | NoHP        | Email             |
|-------------|--------------|---------------|----------------|-------------|-------------------|
| 1234567890  | JOKO SANTOSO | 1990-05-21    | SRI LESTARI    | 08123456789 | joko@email.com    |

> Format `TanggalLahir` harus dalam `YYYY-MM-DD`

## ▶️ Cara Menjalankan

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

**Isi `requirements.txt`**:
```
selenium
pandas
python-dotenv
```

### 2. Jalankan script

```bash
python main.py
```

Script akan membaca file `data.xlsx`, mengisi form BSU satu per satu, lalu menyimpan hasilnya ke `hasil.csv`.

---

## ⚠️ Catatan

- Website BSU bisa saja berubah, pastikan ID form-nya masih sesuai
- Tidak bisa berjalan offline atau jika website down
- Rekomendasi gunakan `ChromeDriver` terbaru dan `Google Chrome` versi stabil

---

## 🧾 Lisensi

MIT License © 2025 [@hanungss](https://github.com/hanungss)
