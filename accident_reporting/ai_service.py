"""
事故・ヒヤリハット報告書のAI生成サービス

GoogleAI（Gemini）を使用して、職員が入力した事実情報から
法令準拠の報告書文章、原因分析、再発防止策を自動生成します。

【AI文章生成ルール】
・感情語・評価語は禁止
・推測は「〜と考えられる」に統一
・利用者責任への偏重禁止
・職員過失断定禁止
・再発防止策は「事業所としての対応」
"""
import os
import json
import google.generativeai as genai
from django.conf import settings


# GoogleAI APIキーの設定
GOOGLE_AI_API_KEY = os.environ.get('GOOGLE_AI_API_KEY', '')

if GOOGLE_AI_API_KEY:
    genai.configure(api_key=GOOGLE_AI_API_KEY)


# AI生成用のシステムプロンプト
SYSTEM_PROMPT = """あなたは介護・障害福祉事業所の事故報告書作成を支援する専門AIです。
以下のルールを厳守して、法令準拠かつ運営指導で指摘されない報告書を作成してください。

【絶対遵守ルール】
1. 感情語・評価語の禁止
   - NG例: 「残念ながら」「不幸にも」「幸い」「軽微な」「重大な」
   - OK例: 客観的事実のみを記載

2. 推測表現の統一
   - 推測が必要な場合は「〜と考えられる」に統一
   - NG例: 「〜だろう」「〜かもしれない」「〜と思われる」

3. 責任の偏重禁止
   - 利用者の責任に偏った記載をしない
   - 職員の過失を断定しない
   - 事実に基づいた客観的な記載に徹する

4. 再発防止策の主体
   - 「事業所として」の対応を記載
   - 個人の責任追及ではなく、組織的な改善策を提示

5. 時系列の明確化
   - 「誰が・いつ・どこで・何が・どう対応したか」を明確に

6. 行政報告要否の判断基準
   - 死亡事故
   - 医療機関への搬送を要した事故
   - 骨折等の重傷事故
   - 虐待が疑われる事故
   - 感染症の集団発生
   上記に該当する場合は「行政報告が必要」と判定"""


def generate_accident_report_content(report_data: dict) -> dict:
    """
    事故報告書の内容をAIで生成する
    
    Args:
        report_data: 事故報告書の入力データ
            - report_type: 区分（事故/ヒヤリハット）
            - occurred_at: 発生日時
            - location_detail: 発生場所
            - service_type: サービス種別
            - client_name: 利用者名
            - incident_description: 事実経過
            - client_state: 利用者の状態
            - damage_status: 被害の状況
            - initial_response: 初期対応
            - family_contact_log: 家族への連絡状況
            - medical_response: 医療機関への対応
    
    Returns:
        dict: AI生成結果
            - overview: 事故の状況
            - cause_analysis: 原因分析
            - prevention_plan: 再発防止策
            - is_government_report_needed: 行政報告要否
            - government_report_reason: 行政報告要否の判定理由
    """
    
    if not GOOGLE_AI_API_KEY:
        # APIキーが設定されていない場合はダミーの結果を返す
        return {
            'overview': '【AI生成機能を使用するには、GOOGLE_AI_API_KEY環境変数の設定が必要です】',
            'cause_analysis': '【AI生成機能を使用するには、GOOGLE_AI_API_KEY環境変数の設定が必要です】',
            'prevention_plan': '【AI生成機能を使用するには、GOOGLE_AI_API_KEY環境変数の設定が必要です】',
            'is_government_report_needed': False,
            'government_report_reason': '【AI生成機能を使用するには、GOOGLE_AI_API_KEY環境変数の設定が必要です】',
        }
    
    # ユーザープロンプトの構築
    user_prompt = f"""以下の事故・ヒヤリハット情報に基づいて、報告書の各項目を生成してください。

【入力情報】
■ 区分: {report_data.get('report_type', '不明')}
■ 発生日時: {report_data.get('occurred_at', '不明')}
■ 発生場所: {report_data.get('location_detail', '不明')}
■ サービス種別: {report_data.get('service_type', '不明')}
■ 利用者名: {report_data.get('client_name', '不明')}

■ 事実経過（職員入力）:
{report_data.get('incident_description', '情報なし')}

■ 利用者の状態:
{report_data.get('client_state', '情報なし')}

■ 被害の状況:
{report_data.get('damage_status', '情報なし')}

■ 初期対応:
{report_data.get('initial_response', '情報なし')}

■ 家族への連絡状況:
{report_data.get('family_contact_log', '情報なし')}

■ 医療機関への対応:
{report_data.get('medical_response', '情報なし')}

【出力形式】
以下のJSON形式で出力してください。各項目は日本語で記載し、法令準拠かつ客観的な表現を使用してください。

{{
    "overview": "事故の状況を時系列で客観的に記載（200-400字程度）",
    "cause_analysis": "原因分析を記載。推測は「〜と考えられる」を使用（150-300字程度）",
    "prevention_plan": "事業所としての再発防止策を具体的に記載（200-400字程度）",
    "is_government_report_needed": true または false,
    "government_report_reason": "行政報告要否の判定理由（100-200字程度）"
}}"""

    try:
        # Gemini モデルの初期化
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=SYSTEM_PROMPT
        )
        
        # AI生成の実行
        response = model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,  # 低めの温度で一貫性を確保
                max_output_tokens=2000,
            )
        )
        
        # レスポンスのパース
        response_text = response.text
        
        # JSONブロックの抽出（```json ... ``` で囲まれている場合に対応）
        if '```json' in response_text:
            json_start = response_text.find('```json') + 7
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        elif '```' in response_text:
            json_start = response_text.find('```') + 3
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        
        result = json.loads(response_text)
        
        return {
            'overview': result.get('overview', ''),
            'cause_analysis': result.get('cause_analysis', ''),
            'prevention_plan': result.get('prevention_plan', ''),
            'is_government_report_needed': result.get('is_government_report_needed', False),
            'government_report_reason': result.get('government_report_reason', ''),
        }
        
    except json.JSONDecodeError as e:
        return {
            'overview': f'AI生成結果のパースに失敗しました: {str(e)}',
            'cause_analysis': '',
            'prevention_plan': '',
            'is_government_report_needed': False,
            'government_report_reason': '',
        }
    except Exception as e:
        return {
            'overview': f'AI生成中にエラーが発生しました: {str(e)}',
            'cause_analysis': '',
            'prevention_plan': '',
            'is_government_report_needed': False,
            'government_report_reason': '',
        }
