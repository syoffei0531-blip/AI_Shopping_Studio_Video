from pathlib import Path


class AssetEngine:

    def __init__(self):

        # assetsフォルダ
        self.assets = Path(__file__).resolve().parents[2] / "assets"

        self.bgm = self.assets / "bgm"
        self.sfx = self.assets / "sfx"
        self.op = self.assets / "op"
        self.ed = self.assets / "ed"
        self.logo = self.assets / "logo"
        self.overlay = self.assets / "overlay"
        self.fonts = self.assets / "fonts"

    # -------------------
    # BGM
    # -------------------
    def get_bgm(self, filename):
        return self.bgm / filename

    # -------------------
    # 効果音
    # -------------------
    def get_sfx(self, filename):
        return self.sfx / filename

    # -------------------
    # OP
    # -------------------
    def get_op(self, filename="intro.mp4"):
        return self.op / filename

    # -------------------
    # ED
    # -------------------
    def get_ed(self, filename="outro.mp4"):
        return self.ed / filename

    # -------------------
    # ロゴ
    # -------------------
    def get_logo(self, filename):
        return self.logo / filename

    # -------------------
    # オーバーレイ
    # -------------------
    def get_overlay(self, filename):
        return self.overlay / filename

    # -------------------
    # フォント
    # -------------------
    def get_font(self, filename):
        return self.fonts / filename
