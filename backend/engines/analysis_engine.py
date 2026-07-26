# ============================================
# backend/engines/analysis_engine.py
# Part 1
# ============================================

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


logger = logging.getLogger(__name__)


class AnalysisEngine:
    """
    AI Shopping Studio
    Product Analysis Engine

    Responsibilities
    ----------------
    - 商品情報を受け取る
    - AIへ分析依頼
    - JSONへ変換
    - 後続Engineへ渡す
    """

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5.5"
        )

    # --------------------------------------------------

    def analyze(
        self,
        product: Dict[str, Any],
        reviews: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        logger.info("Analysis Start")

        prompt = self._build_prompt(
            product=product,
            reviews=reviews,
        )

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.4,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": self._system_prompt(),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        result = json.loads(content)

        logger.info("Analysis Complete")

        return result

    # --------------------------------------------------

    def _system_prompt(self) -> str:

        return """
あなたはAI Shopping Studio専属の商品アナリストです。

以下を厳守してください。

・誇張禁止
・公平
・メーカーを過度に持ち上げない
・レビューを参考にする
・メリットだけでなくデメリットも書く
・レビューが少ない場合は推測しない

必ずJSONのみ返してください。
"""

    # --------------------------------------------------

    def _build_prompt(
        self,
        product: Dict[str, Any],
        reviews: List[Dict[str, Any]],
    ) -> str:

        return f"""
商品情報

{json.dumps(product, ensure_ascii=False, indent=2)}

レビュー

{json.dumps(reviews, ensure_ascii=False, indent=2)}

以下JSON形式で回答してください。

{{
  "summary":"",
  "pros":[],
  "cons":[],
  "recommended_for":[],
  "not_recommended_for":[],
  "ratings":{{
      "price":0,
      "quality":0,
      "design":0,
      "performance":0,
      "overall":0
  }},
  "final_comment":""
}}
"""

# --------------------------------------------------

    def validate_result(
        self,
        result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        AIの返却JSONを安全な形式へ補正
        """

        defaults = {
            "summary": "",
            "pros": [],
            "cons": [],
            "recommended_for": [],
            "not_recommended_for": [],
            "ratings": {
                "price": 0,
                "quality": 0,
                "design": 0,
                "performance": 0,
                "overall": 0,
            },
            "final_comment": "",
        }

        if not isinstance(result, dict):
            logger.warning("AI returned invalid result.")
            return defaults

        for key, value in defaults.items():
            if key not in result:
                result[key] = value

        if not isinstance(result["ratings"], dict):
            result["ratings"] = defaults["ratings"]

        for key in defaults["ratings"]:
            result["ratings"].setdefault(key, 0)

        return result

    # --------------------------------------------------

    def analyze_safe(
        self,
        product: Dict[str, Any],
        reviews: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        外部からはこちらを使用することを推奨
        """

        try:

            result = self.analyze(
                product=product,
                reviews=reviews,
            )

            return self.validate_result(result)

        except Exception as e:

            logger.exception(e)

            return {
                "summary": "分析できませんでした。",
                "pros": [],
                "cons": [],
                "recommended_for": [],
                "not_recommended_for": [],
                "ratings": {
                    "price": 0,
                    "quality": 0,
                    "design": 0,
                    "performance": 0,
                    "overall": 0,
                },
                "final_comment": "AI分析に失敗しました。"
            }


analysis_engine = AnalysisEngine()
