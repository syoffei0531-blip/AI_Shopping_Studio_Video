import subprocess

from engines.asset_engine import AssetEngine


class VideoComposer:

    def __init__(self):
        self.asset = AssetEngine()

    def create_video(
        self,
        image_path,
        audio_path,
        subtitle_path,
        output_path,
    ):

        # ---------- 素材 ----------
        op = self.asset.get_op()
        ed = self.asset.get_ed()

        applause = self.asset.get_sfx("applause.mp3")
        amazing = self.asset.get_sfx("amazing.mp3")
        product_intro = self.asset.get_sfx("product_intro.mp3")

        print("========== ASSETS ==========")
        print("OP :", op)
        print("ED :", ed)
        print("拍手 :", applause)
        print("Amazing :", amazing)
        print("商品紹介 :", product_intro)

        # ---------- 動画生成 ----------
        command = [
            "ffmpeg",
            "-y",

            "-loop", "1",
            "-i", str(image_path),

            "-i", str(audio_path),

            "-vf",
            (
                "scale=1080:1920:force_original_aspect_ratio=decrease,"
                "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black"
            ),

            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",

            "-c:a", "aac",

            "-shortest",

            str(output_path)
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

        return output_path
