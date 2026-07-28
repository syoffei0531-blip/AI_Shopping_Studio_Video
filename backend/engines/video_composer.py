import subprocess

from engines.asset_engine import AssetEngine
from pathlib import Path

class VideoComposer:

    def __init__(self):
        print("★★★★★ VIDEO_COMPOSER VERSION B ★★★★★")
        self.asset = AssetEngine()

    def create_video(
        self,
        image_path,
        audio_path,
        subtitle_path,
        output_path,
    ):

        temp_product = "/tmp/product.mp4"
        
        # ---------- 素材 ----------
        op = self.asset.get_op()
        ed = self.asset.get_ed()

        applause = self.asset.get_sfx("applause.mp3")
        amazing = self.asset.get_sfx("amazing.mp3")
        product_intro = self.asset.get_sfx("product_intro.mp3")

        print("========== ASSETS ==========")
        print("Assets Root:", self.asset.assets)
        print("OP:", op)
        print("ED:", ed)
        print("Current Dir:", Path.cwd())
        print("OP :", op)
        print("ED :", ed)
        print("拍手 :", applause)
        print("Amazing :", amazing)
        print("商品紹介 :", product_intro)

        # ---------- 動画生成 ----------
        subtitle_filter = subtitle_path.replace("\\", "/")
        
        command = [
            "ffmpeg",
            "-y",

            "-loop", "1",
            "-framerate", "30",
            "-i", str(image_path),

            "-i", str(audio_path),

            "-map", "0:v:0",
            "-map", "1:a:0",

            "-vf",
            (
                "scale=1080:1920:force_original_aspect_ratio=decrease,"
                "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,"
                f"subtitles='{subtitle_filter}'"
            ),

            "-c:v", "libx264",
            "-preset", "medium",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
    
            "-shortest",

            temp_product
        ]

        print("========== FFMPEG ==========")
        print(" ".join(command))

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        print(result.stdout)
        print(result.stderr)

        if result.returncode != 0:
            raise Exception(result.stderr)

        print("PRODUCT CREATED")

        subprocess.run([
            "ffmpeg",
            "-i",
            temp_product
        ])
    try:
        probe = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                temp_product
            ],
            capture_output=True,
            text=True
        )
    except Exception as e:
        
        print("FFPROBE ERROR:", e)
        print("PRODUCT DURATION =", probe.stdout)

        # -----------------------------
        # OP + 商品 + ED を結合
        # -----------------------------

        concat_file = "/tmp/concat.txt"

        with open(concat_file, "w", encoding="utf-8") as f:
            f.write(f"file '{op}'\n")
            f.write(f"file '{temp_product}'\n")
            f.write(f"file '{ed}'\n")

        concat_command = [
            "ffmpeg",
            "-y",

            "-fflags", "+genpts",

            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,

            "-vsync", "vfr",

            "-c:v", "libx264",
            "-preset", "medium",
            "-pix_fmt", "yuv420p",

            "-c:a", "aac",

            "-movflags", "+faststart",

            str(output_path)
        ]

        print("========== CONCAT ==========")
        print("CONCAT MODE = ENCODE")
        print(" ".join(concat_command))

        concat_result = subprocess.run(
            concat_command,
            capture_output=True,
            text=True
        )
        
        print("CONCAT FINISHED")
        print(concat_result.stdout)
        print(concat_result.stderr)

        if concat_result.returncode != 0:
            raise Exception(concat_result.stderr)

        return output_path
