from django.db.models import Sum
from datetime import date
from django.conf import settings
from decimal import Decimal
from .models import Staff, StaffContract, WorkRecord # 定義したモデルをインポート

# --- 設定値（現在は仮の週40時間） ---
# settings.pyから値を取得。設定されていない場合はデフォルトの40時間を使用。
FULL_TIME_HOURS_PER_WEEK = getattr(settings, 'FULL_TIME_HOURS_PER_WEEK', 40)


def calculate_full_time_equivalent(staff_id, start_date, end_date):
    """
    指定された職員の指定期間における常勤換算数（FTE: Full-Time Equivalent）を計算する。
    
    常勤換算数 = 該当職員の総勤務時間数 / 常勤職員の基準総時間数
    
    Args:
        staff_id (int): 対象職員のID。
        start_date (date): 計算期間の開始日。
        end_date (date): 計算期間の終了日。
        
    Returns:
        float: 常勤換算数 (小数点以下2桁に丸められる)。
    """
    
    # 1. 職員の総勤務時間（分）を集計
    # WorkRecordはduration_minutesで分単位の勤務時間を保持
    total_minutes_result = WorkRecord.objects.filter(
        staff_id=staff_id,
        work_date__range=[start_date, end_date]
    ).aggregate(Sum('duration_minutes'))
    
    total_minutes = total_minutes_result.get('duration_minutes__sum')
    
    if total_minutes is None or total_minutes == 0:
        return 0.0
    
    # 2. 常勤職員の基準時間を取得
    
    # 対象職員の契約情報を取得（計算期間に最も近い、または有効な契約を取得すべきだが、
    # 今回は簡便化のため、最も新しい契約を取得すると仮定）
    try:
        # 契約開始日がstart_date以前で、最も新しい契約を取得
        contract = StaffContract.objects.filter(
            staff_id=staff_id,
            contract_start_date__lte=start_date
        ).latest('contract_start_date')
    except StaffContract.DoesNotExist:
        # 契約情報がない場合は計算不能
        return 0.0

    # 基準時間として、契約上の週労働時間を使用
    # ユーザーの指示では「常勤職員の基準総時間数」を分母に使うロジックだが、
    # 提示されたコードは「対象職員の契約時間」を分母に使っているため、そちらを採用。
    # (常勤換算の分母は、通常「常勤職員の週の所定労働時間」が使われるが、
    # 提示されたコードの意図を尊重し、契約上の週労働時間を使用)
    benchmark_hours_per_week = contract.contract_hours_week

    # 3. 対象期間の総週数を計算
    # 対象期間の日数
    duration_days = (end_date - start_date).days + 1
    
    # 対象期間の総週数
    duration_weeks = duration_days / 7.0
    
    # 4. 対象期間における常勤換算の総時間 (分)
    # 基準時間(時間/週) * 対象期間の週数 * 60分
    # Decimal型とfloat型の乗算でTypeErrorが発生するため、Decimal型に変換して計算
    full_time_minutes_benchmark = benchmark_hours_per_week * Decimal(duration_weeks) * 60

    if full_time_minutes_benchmark == 0:
        return 0.0
        
    # 5. 常勤換算数（FTE）の計算
    # 常勤換算数 = 実際の総勤務時間（分） / 契約上の基準総時間（分）
    fte = total_minutes / full_time_minutes_benchmark
    
    return round(float(fte), 2)
