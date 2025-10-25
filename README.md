---

# 🧠 RSA QR Capstone (Full Local Version)

Aplikasi Flask untuk **penandatanganan dan verifikasi file digital** berbasis **RSA** dengan tambahan **QR Code**.
Dirancang untuk penggunaan **lokal** maupun **hosting di Render**, dengan login multi-role (`admin`, `client`, `mitra`) dan dashboard terpisah.

---

## 🇮🇩 Deskripsi (Bahasa Indonesia)

### ⚙️ Fitur Utama

* 🔐 **Generate Key RSA** — membuat kunci publik dan privat.
* 🖋️ **Digital Signing** — menandatangani file menggunakan private key.
* ✅ **Verification System** — memverifikasi keaslian file digital.
* 🧾 **QR Code Generation** — menampilkan QR Code hasil verifikasi.
* 👥 **Login Multi-Role** — tiga role berbeda: `admin`, `client`, dan `mitra`.
* 📂 **Auto-Save Outputs** — hasil proses otomatis tersimpan di `outputs/`.
* ⚡ **Folder Otomatis** — `keys/`, `uploads/`, dan `outputs/` dibuat otomatis.

---

### 🧩 Struktur Proyek

```
RSA_QR_Capstone/
├── app.py                 # Aplikasi Flask utama
├── sign_file.py           # Script tanda tangan manual
├── requirements.txt       # Dependensi Python
├── image/                 # Logo dan background
├── webpage/               # Template HTML
├── keys/                  # RSA key pairs (generate otomatis)
├── uploads/               # File upload sementara
└── outputs/               # Hasil sign dan verifikasi
```

---

### 💻 Cara Menjalankan di Lokal

1. Clone repositori:

   ```bash
   git clone https://github.com/username/RSA_QR_Capstone.git
   cd RSA_QR_Capstone
   ```
2. Buat virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Instal dependensi:

   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi:

   ```bash
   python app.py
   ```
5. Buka browser:
   👉 `http://127.0.0.1:5000`

---

### 🔑 Akun Default

| Role   | Username | Password  |
| ------ | -------- | --------- |
| Admin  | admin    | admin123  |
| Client | client   | client123 |
| Mitra  | mitra    | mitra123  |

> Kamu dapat mengubah password di `app.py` atau menggunakan environment variable.

---

### 🚀 Deploy ke Render

1. Upload semua file ke GitHub.
2. Masuk ke [Render.com](https://render.com) → **New → Web Service**
3. Isi Start Command:

   ```
   gunicorn app:app
   ```
4. Tambahkan Environment Variables:

   ```
   FLASK_SECRET_KEY = something_secure
   ADMIN_PASS = admin123
   CLIENT_PASS = client123
   MITRA_PASS = mitra123
   FLASK_DEBUG = 0
   ```
5. Klik **Deploy**, lalu buka URL publik yang diberikan oleh Render.

---

### 🧠 Teknologi yang Digunakan

* **Flask** – framework utama
* **Flask-Login** – autentikasi multi-user
* **PyCryptodome** – RSA, SHA-256, enkripsi
* **qrcode** – pembuatan QR Code
* **Gunicorn** – server production
* **Werkzeug** – utilitas Flask

---

### 🪪 Lisensi

Proyek ini bersifat **open-source (MIT License)**.
Silakan digunakan dan dikembangkan untuk keperluan akademik, riset, atau pengembangan sistem keamanan digital.

---

## 🇬🇧 Description (English Version)

### ⚙️ Key Features

* 🔐 **RSA Key Generation** — create public and private key pairs.
* 🖋️ **Digital Signing** — digitally sign files with the private key.
* ✅ **Verification System** — verify file authenticity.
* 🧾 **QR Code Generation** — display a QR Code for verification results.
* 👥 **Multi-Role Login** — three separate roles: `admin`, `client`, and `mitra`.
* 📂 **Auto-Save Outputs** — processed results automatically stored in `outputs/`.
* ⚡ **Automatic Folder Setup** — creates `keys/`, `uploads/`, and `outputs/` if missing.

---

### 🧩 Project Structure

```
RSA_QR_Capstone/
├── app.py                 # Main Flask Application
├── sign_file.py           # Manual signing tool
├── requirements.txt       # Dependencies
├── image/                 # Assets (logo, backgrounds)
├── webpage/               # HTML templates
├── keys/                  # RSA key pairs (auto-generated)
├── uploads/               # Temporary uploaded files
└── outputs/               # Sign and verification results
```

---

### 💻 Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/username/RSA_QR_Capstone.git
   cd RSA_QR_Capstone
   ```
2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:

   ```bash
   python app.py
   ```
5. Open browser at:
   👉 `http://127.0.0.1:5000`

---

### 🔑 Default Accounts

| Role   | Username | Password  |
| ------ | -------- | --------- |
| Admin  | admin    | admin123  |
| Client | client   | client123 |
| Mitra  | mitra    | mitra123  |

---

### 🚀 Deploy on Render

1. Push your project to GitHub.
2. Go to [Render.com](https://render.com) → **New → Web Service**.
3. Set **Start Command**:

   ```
   gunicorn app:app
   ```
4. Add **Environment Variables**:

   ```
   FLASK_SECRET_KEY = something_secure
   ADMIN_PASS = admin123
   CLIENT_PASS = client123
   MITRA_PASS = mitra123
   FLASK_DEBUG = 0
   ```
5. Click **Deploy** and access your public Render URL.

---

### 🧠 Tech Stack

* **Flask** – backend framework
* **Flask-Login** – user authentication
* **PyCryptodome** – RSA encryption and SHA-256 hashing
* **qrcode** – QR generation
* **Gunicorn** – production WSGI server
* **Werkzeug** – Flask utilities

---

### 🪪 License

Licensed under the **MIT License**.
You are free to use, modify, and distribute this project for academic or development purposes.

---

> ✨ *Developed by Ammar Siraj Ananda, Sallaa Fikriyatul 'Arifah, Muhammad Fadhli Rahmansyah — RSA QR Capstone Project (2025)*

---
