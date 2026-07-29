import subprocess

from moviepy import VideoFileClip, ImageClip, concatenate_videoclips

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

        temp_product = "/tmp/product_scene.mp4"
        
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

        probe = subprocess.run(
            [
                "ffmpeg",
                "-i",
                temp_product
            ],
            capture_output=True,
            text=True
        )

        print(probe.stderr)

        # -----------------------------
        # OP + 商品 + ED を結合
        # -----------------------------

        intro = VideoFileClip(str(op))
        
        studio = ImageClip(str(self.asset.get_studio()))
        studio = studio.with_duration(5)

        product = VideoFileClip(str(temp_product))
        outro = VideoFileClip(str(ed))
        
        final = concatenate_videoclips(
            [
                intro,
                studio,
                product,
                outro
            ],
            method="compose"
        )

        final.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            fps=30
        )

        intro.close()
        studio.close()
        product.close()
        outro.close()
        final.close()
        
        return output_path
