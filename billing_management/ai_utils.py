"""
Google AI (Gemini) integration utilities for Care-pass system
"""
import os
import json
import google.generativeai as genai

def initialize_gemini():
    """Initialize Google Gemini API client"""
    api_key = os.environ.get('GOOGLE_AI_API_KEY') or os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_AI_API_KEY or GEMINI_API_KEY environment variable is not set")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def analyze_sentiment(assessment):
    """
    Analyze sentiment and quality of progress assessment comments
    
    Args:
        assessment: ProgressAssessment object
        
    Returns:
        dict: Analysis results with sentiment_score, record_quality_score, keywords, feedback
    """
    model = initialize_gemini()
    
    prompt = f"""
あなたは福祉事業所の専門家です。以下の職員による利用者の進捗記録を分析し、記録の質を評価してください。

【利用者情報】
- 氏名: {assessment.client.full_name}
- 評価日: {assessment.assessment_date}
- 成長スコア: {assessment.progress_score} / 5.0

【職員のコメント】
{assessment.specialist_comment}

以下の項目について分析し、JSON形式で回答してください：

1. sentiment_score: 感情スコア（-1.0〜1.0、ポジティブ=1.0、ネガティブ=-1.0、ニュートラル=0.0）
2. record_quality_score: 記録の質スコア（1〜5、5が最高）
   - 具体性: 具体的な行動や状況が記録されているか
   - 客観性: 主観的な表現ではなく、客観的な観察が記録されているか
   - 専門性: 専門的な視点や用語が適切に使用されているか
3. keywords: 重要なキーワード（最大5個、カンマ区切り）
4. feedback: 改善提案（具体的なフィードバック、100文字以内）

回答例：
{{
  "sentiment_score": 0.8,
  "record_quality_score": 4,
  "keywords": "コミュニケーション, 社会性, 集団活動, 成長, 積極性",
  "feedback": "具体的な場面の記述が優れています。今後は数値的な指標（回数、時間など）を追加すると、さらに客観性が向上します。"
}}

必ずJSON形式のみで回答してください。
"""
    
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.3,
            response_mime_type="application/json"
        )
    )
    
    result = json.loads(response.text)
    return result

def generate_progress_record(client, user_input, plan_context):
    """
    Generate professional progress record using AI
    
    Args:
        client: Client object
        user_input: Staff's brief input
        plan_context: Individual support plan context
        
    Returns:
        str: Generated progress record text
    """
    model = initialize_gemini()
    
    prompt = (
        f"あなたは福祉施設の専門職員です。以下の情報と目標に基づき、専門的な進捗記録を生成してください。\n"
        f"記録の形式は、具体的な行動、効果、専門的な視点を含んだ文章にしてください。\n"
        f"記録は200文字以内で、客観的かつ具体的に記述してください。\n\n"
        f"---個別支援計画情報---\n{plan_context}\n\n"
        f"---職員の断片的な入力---\n{user_input}\n\n"
        f"上記の情報に基づき、法定形式の進捗記録を生成してください。"
    )
    
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=500
        )
    )
    
    return response.text.strip()

def predict_churn_risk(client_data):
    """
    Predict dropout/churn risk for a client
    
    Args:
        client_data: dict with client information
        
    Returns:
        dict: Prediction results with risk_score and recommendations
    """
    model = initialize_gemini()
    
    prompt = f"""
あなたは福祉施設の専門家です。以下の利用者データを分析し、退所リスクを予測してください。

【利用者データ】
{json.dumps(client_data, ensure_ascii=False, indent=2)}

以下の項目について分析し、JSON形式で回答してください：

1. risk_score: 退所リスクスコア（0.0〜1.0、1.0が最高リスク）
2. risk_level: リスクレベル（"low", "medium", "high"）
3. risk_factors: リスク要因（配列、最大5個）
4. recommendations: 推奨対策（配列、最大3個）

回答例：
{{
  "risk_score": 0.65,
  "risk_level": "medium",
  "risk_factors": ["出席率の低下", "保護者との連絡頻度減少", "目標達成率の低下"],
  "recommendations": ["保護者面談の実施", "個別支援計画の見直し", "送迎サービスの提案"]
}}

必ずJSON形式のみで回答してください。
"""
    
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.3,
            response_mime_type="application/json"
        )
    )
    
    result = json.loads(response.text)
    return result
