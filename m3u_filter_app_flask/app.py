from flask import Flask, render_template, request, send_file
import os

def extract_category_from_m3u(file_path, categories, output_file):
    extracted_entries = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as m3u_file:
            lines = m3u_file.readlines()
        for idx, line in enumerate(lines):
            if line.startswith("#EXTINF"):
                try:
                    category_info = line.split(",", 1)[1].strip()
                    if any(cat.lower() in category_info.lower() for cat in categories):
                        url = lines[idx + 1].strip() if idx + 1 < len(lines) else None
                        if url and url.startswith(("http", "rtmp", "rtsp")):
                            extracted_entries.append((line.strip(), url))
                except IndexError:
                    pass
        if extracted_entries:
            with open(output_file, 'w', encoding='utf-8') as output:
                output.write("#EXTM3U\n")
                for metadata, url in extracted_entries:
                    output.write(f"{metadata}\n{url}\n")
    except Exception as e:
        print(f"Error: {e}")

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["m3u_file"]
        categories = request.form.get("categories").split(",")
        if file and categories:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            output_file = os.path.join(RESULT_FOLDER, "filtered_" + file.filename)
            file.save(file_path)
            extract_category_from_m3u(file_path, categories, output_file)
            return send_file(output_file, as_attachment=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
