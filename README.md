# 🚀 Universal Video Downloader (Flask + yt-dlp)

A powerful **local video & audio downloader** built using **Flask, yt-dlp, FFmpeg, and SQLite**, featuring real-time progress tracking and multi-download queue.

---

## 🔥 Features

* 🎥 Download videos (MP4) in multiple qualities (1080p, 720p, 360p)
* 🎧 Extract audio (MP3) with thumbnail
* 📊 Real-time progress bar
* 📦 Multi-download queue system
* 🖼 Thumbnail download
* 📂 Organized folders (per video/audio)
* 🗑 Delete from UI
* 📚 Library view
* 💾 SQLite database (history)

---

## 🛠 Tech Stack

* **Backend:** Flask (Python)
* **Downloader:** yt-dlp
* **Media Processing:** FFmpeg
* **Database:** SQLite
* **Frontend:** HTML + CSS + JS

---

## 📁 Project Structure

```id="x3c9oz"
project/
│
├── app.py
├── downloads/
│   ├── videos/
│   └── music/
├── templates/
│   ├── index.html
│   └── library.html
├── downloads.db
├── yt-dlp.exe
└── ffmpeg.exe   ← IMPORTANT
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone repo

```id="j9j1xq"
https://github.com/pratikpawar004/universal-video-downloader.git
cd universal-video-downloader
```

### 2️⃣ Install Python dependencies

```id="6v7k8o"
pip install flask
```

---

## 🔥 3️⃣ Install yt-dlp & FFmpeg (IMPORTANT)

### ✅ yt-dlp

Download:
👉 https://github.com/yt-dlp/yt-dlp/releases

Place:

```id="u3h2w0"
yt-dlp.exe → project root folder
```

---

### ✅ FFmpeg (REQUIRED for audio/video merge)

Download:
👉 https://www.gyan.dev/ffmpeg/builds/

Extract and copy:

```id="psg7lt"
ffmpeg.exe → project root folder
```

---

### ⚠️ Why FFmpeg is needed?

* yt-dlp downloads:

  * video stream
  * audio stream (separate)

👉 FFmpeg merges them into a single MP4

Without FFmpeg:

* ❌ video without audio
* ❌ conversion errors

---

## ▶️ Run the app

```id="vsyf3a"
python app.py
```

Open:

```id="p6q8rf"
http://127.0.0.1:5000
```

---

## 🧠 How It Works

* URL → `/download`
* Added to queue
* Worker runs yt-dlp
* Progress tracked live
* FFmpeg merges streams
* Files saved in folders
* History saved in SQLite

---

## 📊 Database (SQLite)

Table: `history`

| Column | Description    |
| ------ | -------------- |
| id     | Auto increment |
| name   | URL            |
| type   | mp3 / mp4      |
| time   | Timestamp      |

---

## ⚠️ Notes

* Local app only (127.0.0.1)
* Sharing links won’t work externally
* Internet required
* FFmpeg must be present

---

## 🚀 Future Improvements

* 🔐 Login system
* 🌐 Cloud deploy
* 📈 Analytics
* ❌ Cancel download
* 📊 Multi-progress UI

---

## Author

Pratik Pawar

---

## ⭐ Support

If you like this project → ⭐ the repo
