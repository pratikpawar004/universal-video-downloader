from flask import Flask, request, jsonify, render_template, send_from_directory
import subprocess, os, re, sqlite3, threading

app = Flask(__name__)

YT_DLP = "yt-dlp.exe"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(BASE_DIR, "downloads", "videos")
MUSIC_DIR = os.path.join(BASE_DIR, "downloads", "music")
DB = os.path.join(BASE_DIR, "downloads.db")

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

# ------------------ DB ------------------

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        type TEXT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

init_db()

def save_history(name, type_):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO history (name, type) VALUES (?,?)", (name, type_))
    conn.commit()
    conn.close()

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/library")
def library():
    return render_template("library.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/tech")
def tech():
    return render_template("tech.html")

@app.route("/platforms")
def platforms():
    return render_template("platforms.html")

# ------------------ RECENT ------------------

@app.route("/recent")
def recent():
    videos, audios = [], []

    for folder in os.listdir(VIDEO_DIR):
        path = os.path.join(VIDEO_DIR, folder)
        if os.path.isdir(path):
            files = os.listdir(path)
            video = next((f for f in files if f.endswith(".mp4")), None)
            thumb = next((f for f in files if f.endswith(".jpg")), None)

            if video:
                videos.append({"name": folder, "video": video, "thumb": thumb})

    for folder in os.listdir(MUSIC_DIR):
        path = os.path.join(MUSIC_DIR, folder)
        if os.path.isdir(path):
            files = os.listdir(path)
            audio = next((f for f in files if f.endswith(".mp3")), None)
            thumb = next((f for f in files if f.endswith(".jpg")), None)

            if audio:
                audios.append({"name": folder, "audio": audio, "thumb": thumb})

    return jsonify({"videos": videos, "audios": audios})

# ------------------ FILE SERVE ------------------

@app.route("/video/<folder>/<file>")
def video(folder, file):
    return send_from_directory(os.path.join(VIDEO_DIR, folder), file)

@app.route("/thumb/<folder>/<file>")
def thumb(folder, file):
    return send_from_directory(os.path.join(VIDEO_DIR, folder), file)

@app.route("/audio/<folder>/<file>")
def audio(folder, file):
    return send_from_directory(os.path.join(MUSIC_DIR, folder), file)

@app.route("/audio-thumb/<folder>/<file>")
def audio_thumb(folder, file):
    return send_from_directory(os.path.join(MUSIC_DIR, folder), file)

# ------------------ DELETE ------------------

@app.route("/delete", methods=["POST"])
def delete():
    data = request.json
    type_ = data["type"]
    name = data["name"]

    path = os.path.join(VIDEO_DIR if type_=="video" else MUSIC_DIR, name)

    for f in os.listdir(path):
        os.remove(os.path.join(path, f))
    os.rmdir(path)

    return jsonify({"status": "deleted"})

# ------------------ DOWNLOAD QUEUE ------------------

queue = []
current_progress = {"progress": 0}

def run_download(data):
    global current_progress

    url = data["url"]
    quality = data.get("quality","720")
    format_type = data["format"]

    current_progress["progress"] = 0   # 🔥 RESET

    if format_type == "mp3":
        output = os.path.join(MUSIC_DIR, "%(title)s", "audio.%(ext)s")
        cmd = [
            YT_DLP, "--newline",
            "-x","--audio-format","mp3","--audio-quality","0",
            "--write-thumbnail","--convert-thumbnails","jpg",
            "-o", output, url
        ]
    else:
        output = os.path.join(VIDEO_DIR, "%(title)s", "video.%(ext)s")

        fmt = f"bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"

        cmd = [
            YT_DLP, "--newline",
            "-f", fmt,
            "--merge-output-format","mp4",
            "--write-thumbnail","--convert-thumbnails","jpg",
            "-o", output, url
        ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)

    for line in process.stdout:
        if "%" in line:
            try:
                p = line.split("%")[0].split()[-1]
                current_progress["progress"] = int(float(p))
            except:
                pass

    current_progress["progress"] = 100
    save_history(url, format_type)

def worker():
    while True:
        if queue:
            job = queue.pop(0)
            run_download(job)

threading.Thread(target=worker, daemon=True).start()

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    queue.append(data)
    return jsonify({"status": "added to queue"})

@app.route("/progress")
def progress():
    return jsonify(current_progress)

# ------------------

if __name__ == "__main__":
    app.run(debug=True)