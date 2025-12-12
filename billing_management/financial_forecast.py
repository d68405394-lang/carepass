"""
経営・財務予測AI機能
既存の離脱リスク予測ロジックを応用して、事業所の収支予測を行う
"""
from django.db.models import Avg, Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Client, WorkRecord, ProgressAssessment, FTESufficientStatus


def calculate_financial_forecast(months_ahead=3):
    """
    数ヶ月先の収支を予測する
    
    Args:
        months_ahead: 予測する月数（デフォルト: 3ヶ月）
    
    Returns:
        dict: 財務予測データ
    """
    today = timezone.now().date()
    
    # 1. 利用者数の予測
    total_clients = Client.objects.count()
    
    # 離脱リスクの高い利用者数を取得
    from .views import ChurnPredictionView
    churn_view = ChurnPredictionView()
    churn_data = churn_view.get(None).data
    
    high_risk_count = churn_data.get('high_risk_count', 0)
    medium_risk_count = churn_data.get('medium_risk_count', 0)
    
    # 予測される利用者数（高リスク80%離脱、中リスク30%離脱と仮定）
    predicted_churn = int(high_risk_count * 0.8 + medium_risk_count * 0.3)
    predicted_clients = total_clients - predicted_churn
    
    # 2. 出席率の予測（過去30日の平均）
    thirty_days_ago = today - timedelta(days=30)
    recent_assessments = ProgressAssessment.objects.filter(
        assessment_date__gte=thirty_days_ago
    )
    
    if recent_assessments.exists():
        avg_progress_score = recent_assessments.aggregate(Avg('progress_score'))['progress_score__avg'] or 0
        # 進捗スコアが高いほど出席率も高いと仮定（相関係数0.7）
        predicted_attendance_rate = min(0.95, 0.6 + (float(avg_progress_score) / 5.0) * 0.35)
    else:
        predicted_attendance_rate = 0.85  # デフォルト値
    
    # 3. 加算取得状況の予測
    fte_statuses = FTESufficientStatus.objects.all()
    sufficient_locations = fte_statuses.filter(is_kasan_sufficient=True).count()
    total_locations = fte_statuses.count()
    
    if total_locations > 0:
        kasan_achievement_rate = sufficient_locations / total_locations
    else:
        kasan_achievement_rate = 0.0
    
    # 4. 収入予測（単価×利用者数×出席率×加算率）
    # 放課後等デイサービスの平均単価: 約10,000円/日
    base_unit_price = 10000
    
    # 加算による単価上昇（加算充足率に応じて0-20%増）
    kasan_multiplier = 1.0 + (kasan_achievement_rate * 0.2)
    
    # 月間営業日数（平均22日）
    working_days_per_month = 22
    
    # 月間予測収入
    monthly_revenue = (
        base_unit_price * 
        predicted_clients * 
        predicted_attendance_rate * 
        kasan_multiplier * 
        working_days_per_month
    )
    
    # 5. 支出予測（職員人件費）
    # 過去30日の勤務実績から平均人件費を算出
    recent_work_records = WorkRecord.objects.filter(
        work_date__gte=thirty_days_ago
    )
    
    if recent_work_records.exists():
        # duration_minutesフィールドを使用して合計時間を計算
        total_minutes = sum([record.duration_minutes for record in recent_work_records])
        total_hours = total_minutes / 60
        
        # 平均時給2,000円と仮定
        avg_hourly_wage = 2000
        monthly_labor_cost = (total_hours / 30) * 30 * avg_hourly_wage
    else:
        # デフォルト値（利用者10人につき職員1人、月給30万円）
        monthly_labor_cost = (predicted_clients / 10) * 300000
    
    # その他経費（家賃、光熱費等）を収入の30%と仮定
    other_expenses = monthly_revenue * 0.3
    
    # 月間予測支出
    monthly_expenses = monthly_labor_cost + other_expenses
    
    # 6. 利益予測
    monthly_profit = monthly_revenue - monthly_expenses
    profit_margin = (monthly_profit / monthly_revenue * 100) if monthly_revenue > 0 else 0
    
    # 7. キャッシュフロー予測（3ヶ月分）
    cash_flow_forecast = []
    for month in range(1, months_ahead + 1):
        # 月ごとに若干の変動を加える（±5%）
        import random
        variation = random.uniform(0.95, 1.05)
        
        cash_flow_forecast.append({
            'month': month,
            'revenue': int(monthly_revenue * variation),
            'expenses': int(monthly_expenses * variation),
            'profit': int(monthly_profit * variation),
        })
    
    # 8. リスク評価
    risk_level = 'low'
    risk_message = '財務状況は良好です。'
    
    if profit_margin < 5:
        risk_level = 'high'
        risk_message = '利益率が低く、経営が厳しい状況です。コスト削減や利用者獲得が急務です。'
    elif profit_margin < 15:
        risk_level = 'medium'
        risk_message = '利益率が低めです。効率化や加算取得の強化を検討してください。'
    elif predicted_churn > total_clients * 0.1:
        risk_level = 'medium'
        risk_message = '利用者離脱リスクが高いです。利用者満足度向上に注力してください。'
    
    # 9. 改善提案
    recommendations = []
    
    if kasan_achievement_rate < 0.8:
        recommendations.append({
            'title': '加算取得率の向上',
            'description': f'現在の加算充足率は{kasan_achievement_rate*100:.1f}%です。専門職の配置を強化することで、収入を{int((0.8 - kasan_achievement_rate) * monthly_revenue * 0.2):,}円増やせる可能性があります。',
            'impact': 'high',
        })
    
    if predicted_attendance_rate < 0.85:
        recommendations.append({
            'title': '出席率の向上',
            'description': f'現在の予測出席率は{predicted_attendance_rate*100:.1f}%です。利用者満足度を向上させることで、収入を{int((0.85 - predicted_attendance_rate) * monthly_revenue):,}円増やせる可能性があります。',
            'impact': 'high',
        })
    
    if predicted_churn > 0:
        recommendations.append({
            'title': '利用者離脱の防止',
            'description': f'{predicted_churn}名の利用者が離脱する可能性があります。早期に面談や支援計画の見直しを行うことで、{int(predicted_churn * base_unit_price * working_days_per_month * predicted_attendance_rate):,}円の収入減を防げます。',
            'impact': 'high',
        })
    
    if monthly_labor_cost / monthly_revenue > 0.5:
        recommendations.append({
            'title': '人件費率の最適化',
            'description': f'人件費率が{monthly_labor_cost / monthly_revenue * 100:.1f}%と高めです。業務効率化やシフト最適化を検討してください。',
            'impact': 'medium',
        })
    
    return {
        'forecast_date': today.isoformat(),
        'months_ahead': months_ahead,
        'current_metrics': {
            'total_clients': total_clients,
            'predicted_clients': predicted_clients,
            'predicted_churn': predicted_churn,
            'attendance_rate': round(predicted_attendance_rate * 100, 1),
            'kasan_achievement_rate': round(kasan_achievement_rate * 100, 1),
        },
        'monthly_forecast': {
            'revenue': int(monthly_revenue),
            'expenses': int(monthly_expenses),
            'profit': int(monthly_profit),
            'profit_margin': round(profit_margin, 1),
        },
        'cash_flow_forecast': cash_flow_forecast,
        'risk_assessment': {
            'level': risk_level,
            'message': risk_message,
        },
        'recommendations': recommendations,
    }
