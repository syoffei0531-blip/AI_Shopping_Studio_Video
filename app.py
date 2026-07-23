from flask import Flask, request, send_file, Response
import subprocess
import os
import requests
import json

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Japan Hidden Stories</title>
    </head>
    <body>
        <h1>Japan Hidden Stories</h1>

        <p>
            AI platform for automatically publishing educational videos
            about Japanese culture to TikTok.
        </p>

        <p><a href="/privacy">Privacy Policy</a></p>
        <p><a href="/terms">Terms of Service</a></p>

        <p>Contact: syoffei0531@gmail.com</p>
    </body>
    </html>
    """
def home():
    return """
    <h1>Japan Hidden Stories</h1>

    <p>AI platform for automatically publishing educational videos about Japanese culture.</p>

    <p><a href="/privacy">Privacy Policy</a></p>

    <p><a href="/terms">Terms of Service</a></p>

    <p>Contact: syoffei0531@gmail.com</p>
    """

@app.route("/tiktokd4nUffblE8bbcZnU3otgBCAB")
def tiktok_verify():
    return Response(
        "tiktok-developers-site-verification=d4nUffblE8bbcZnU3otgBCAByFcyTvaQ",
        mimetype="text/plain"
    )
from flask import Response

@app.route("/tiktokzzL3jSgljn7HlUWykqiO3sGmR5MKhD7q.txt")
def tiktok_verify_new():
    return Response(
        "tiktok-developers-site-verification=zzL3jSgljn7HlUWykqiO3sGmR5MKhD7q",
        mimetype="text/plain"
    )

@app.route("/privacy")
def privacy():
    return """
    <h1>Privacy Policy</h1>
    <p>This application only uses TikTok APIs to publish videos authorized by the user.</p>
    <p>No personal information is sold or shared with third parties.</p>
    <p>Contact: syoffei0531@gmail.com</p>
    """

@app.route("/terms")
def terms():
    return """
    <h1>Terms of Service</h1>
    <p>This application is used to automatically publish educational videos about Japanese culture.</p>
    <p>Users are responsible for the content they publish.</p>
    """


@app.route("/create-video", methods=["POST"])
def create_video():

    try:

        os.makedirs("/tmp/video", exist_ok=True)

        # -----------------------
        # n8nからファイル受信
        # -----------------------

        product_image = request.files["product_image"]
        audio = request.files["audio"]

        title = request.form.get("title")
        description = request.form.get("description")
        speech = request.form.get("speech")

        print("========== AI Shopping Studio ==========")
        print("FILES :", list(request.files.keys()))
        print("FORM  :", list(request.form.keys()))
        print("TITLE :", title)
        print("========================================")

        os.makedirs("/tmp/video", exist_ok=True)

        image_path = "/tmp/video/product.jpg"
        audio_path = "/tmp/video/audio.mp3"

        product_image.save(image_path)
        audio.save(audio_path)

        print("========== AI Shopping Studio ==========")
        print("Image :", image_path)
        print("Audio :", audio_path)
        print("========================================")

        # ここから動画生成開始
        
       
    except Exception as e:
        import traceback

        print("========== ERROR ==========")
        print(traceback.format_exc())
        print("===========================")

        return {
            "error": str(e),
            "traceback": traceback.format_exc()
            }, 500
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
