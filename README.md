# 🎨 Air Canvas Premium – Yapay Zeka Destekli Sanal Çizim Uygulaması

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge\&logo=python\&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg?style=for-the-badge\&logo=opencv\&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange.svg?style=for-the-badge\&logo=google\&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-red.svg?style=for-the-badge)

---

## 📌 Proje Hakkında

**Air Canvas Premium**, Computer Vision, OpenCV ve Google MediaPipe kullanılarak geliştirilmiş
yapay zeka destekli bir sanal çizim uygulamasıdır.

Bu uygulama sayesinde ekrana dokunmadan, sadece el hareketleri ile
havada çizim yapabilirsiniz.

Bu proje klasik air drawing projelerinden farklı olarak:

✔ Güvenli menü alanları
✔ Hitbox destekli seçim sistemi
✔ Dinamik fırça kalınlığı
✔ Katmanlı arayüz sistemi
✔ Gerçek zamanlı el takibi
✔ Şekil çizim motoru

özellikleri ile geliştirilmiştir.

---

## ✨ Özellikler

### 🛡 Safe Zone (Güvenli Bölge)

Menü alanına geldiğinizde çizim durur.
Yanlışlıkla arayüz boyanmaz.

### 🎯 Aim Assist (Hitbox Sistemi)

Butonlara tam basmanız gerekmez.
Ekstra seçim alanı sayesinde daha akıcı kontrol sağlar.

### 📐 Dinamik Fırça Kalınlığı

Başparmak ve işaret parmağı mesafesine göre fırça kalınlığı değişir.

Aralık:

5px → 50px

### 🎨 Katmanlı Arayüz Sistemi

* UI her zaman üstte
* Canvas altta
* Yarı saydam paneller
* Modern tasarım

### 🔳 Shape Preview Motoru

* Dikdörtgen
* Çember
* Canlı önizleme
* Sonradan yerleştirme

Profesyonel çizim deneyimi sağlar.

---

## 🕹 Gesture Kontrolleri

| Hareket          | Mod      | Açıklama      |
| ---------------- | -------- | ------------- |
| ☝ İşaret Parmağı | Çizim    | Serbest çizim |
| ✌ İki Parmak     | Hover    | Menü seçimi   |
| 🤏 Üç Parmak     | Kalınlık | Fırça boyutu  |
| 🛑 Temizle       | Reset    | Tuvali sil    |

---

## 📦 Gereksinimler

* Python 3.10 veya 3.11 önerilir
* Kamera gerekli

---

## ⚙ Kurulum

### 1. Repoyu indir

```bash
git clone https://github.com/ardairmk55/air_canvas
cd air_canvas
```

### 2. Sanal ortam oluştur

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Kütüphaneleri yükle

```bash
pip install -r requirements.txt
```

Eğer requirements.txt yoksa:

```bash
pip install opencv-python mediapipe numpy
```

---

## ▶ Çalıştırma

```bash
python air_canvas.py
```

Çıkmak için:

```
Q
```

---

## 📂 Proje Yapısı

```
air_canvas/
│
├── air_canvas.py
├── requirements.txt
├── README.md
├── .gitignore
└── demo/
    └── demo.gif
```

---

## 🧠 Kullanılan Teknolojiler

* OpenCV
* MediaPipe
* NumPy
* Computer Vision
* Hand Tracking
* Gesture Recognition
* UI Layer System
* Hitbox Algorithm

---

## 📷 Demo

/demo/demo.gif

---

## 👨‍💻 Geliştirici

Arda Irmak
Gümüşhane Üniversitesi
Bilgisayar Programcılığı

GitHub:
https://github.com/ardairmk55

---

## 📄 Lisans

MIT License

Serbestçe kullanabilir, değiştirebilir ve paylaşabilirsiniz.
