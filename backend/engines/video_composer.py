from pathlib import Path

from engines.asset_engine import AssetEngine


class VideoComposer:

    def __init__(self):

        self.asset = AssetEngine()

    def create_video(
        self,
        image_path,
        audio_path,
        output_path,
    ):

        op = self.asset.get_op()
        ed = self.asset.get_ed()

        applause = self.asset.get_sfx("applause.mp3")
        amazing = self.asset.get_sfx("amazing.mp3")
        product_intro = self.asset.get_sfx("product_intro.mp3")

        print("OP :", op)
        print("ED :", ed)
        print("拍手 :", applause)
        print("Amazing :", amazing)
        print("商品紹介 :", product_intro)

        return output_path
