import os
import django
from datetime import date, timedelta

# Django環境のセットアップ
# manage.pyと同じ階層で実行されることを想定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from billing_management.models import ServiceLocation, Staff, StaffContract, WorkRecord
from billing_management.utils import calculate_full_time_equivalent

def create_test_data():
    """常勤換算ロジック検証用のテストデータをデータベースに投入する"""
    print("--- テストデータ作成開始 ---")

    # 1. 事業所マスタ
    location, created = ServiceLocation.objects.get_or_create(
        location_id="LOC001",
        defaults={'location_name': "本社"}
    )
    print(f"事業所: {location.location_name} ({'新規作成' if created else '既存'})")

    # 2. 職員マスタ
    staff_full, _ = Staff.objects.get_or_create(
        staff_code="S001",
        defaults={'full_name': "常勤 太郎", 'location': location}
    )
    staff_part, _ = Staff.objects.get_or_create(
        staff_code="S002",
        defaults={'full_name': "非常勤 花子", 'location': location}
    )
    staff_half, _ = Staff.objects.get_or_create(
        staff_code="S003",
        defaults={'full_name': "半減 次郎", 'location': location}
    )
    print("職員3名作成完了")

    # 3. 職員契約テーブル
    # 常勤: 週40時間
    StaffContract.objects.get_or_create(
        staff=staff_full,
        contract_start_date=date(2025, 1, 1),
        defaults={'contract_hours_week': 40.00, 'is_permanent': True}
    )
    # 非常勤: 週20時間
    StaffContract.objects.get_or_create(
        staff=staff_part,
        contract_start_date=date(2025, 1, 1),
        defaults={'contract_hours_week': 20.00, 'is_permanent': False}
    )
    # 半減（契約は40時間だが、勤務は20時間相当で検証）
    StaffContract.objects.get_or_create(
        staff=staff_half,
        contract_start_date=date(2025, 1, 1),
        defaults={'contract_hours_week': 40.00, 'is_permanent': True}
    )
    print("職員契約3件作成完了")

    # 4. 勤務実績テーブル (計算期間: 2025-12-01 (月) 〜 2025-12-07 (日) の1週間)
    start_date = date(2025, 12, 1)
    
    # 勤務時間（分）
    FULL_TIME_DAILY_MINUTES = 8 * 60  # 480分 (常勤の1日8時間)
    PART_TIME_DAILY_MINUTES = 4 * 60  # 240分 (非常勤/半減の1日4時間)
    
    # 常勤 太郎: 40時間/週 (480分 x 5日 = 2400分)
    for i in range(5): # 月曜から金曜
        WorkRecord.objects.get_or_create(
            staff=staff_full,
            work_date=start_date + timedelta(days=i),
            defaults={'duration_minutes': FULL_TIME_DAILY_MINUTES}
        )
    # 土日（0分）
    for i in range(5, 7):
        WorkRecord.objects.get_or_create(
            staff=staff_full,
            work_date=start_date + timedelta(days=i),
            defaults={'duration_minutes': 0}
        )

    # 非常勤 花子: 20時間/週 (240分 x 5日 = 1200分)
    for i in range(5): # 月曜から金曜
        WorkRecord.objects.get_or_create(
            staff=staff_part,
            work_date=start_date + timedelta(days=i),
            defaults={'duration_minutes': PART_TIME_DAILY_MINUTES}
        )
    # 土日（0分）
    for i in range(5, 7):
        WorkRecord.objects.get_or_create(
            staff=staff_part,
            work_date=start_date + timedelta(days=i),
            defaults={'duration_minutes': 0}
        )

    # 半減 次郎: 20時間/週 (240分 x 5日 = 1200分)
    for i in range(5): # 月曜から金曜
        WorkRecord.objects.get_or_create(
            staff=staff_half,
            work_date=start_date + timedelta(days=i),
            defaults={'duration_minutes': PART_TIME_DAILY_MINUTES}
        )
    # 土日（0分）
    for i in range(5, 7):
        WorkRecord.objects.get_or_create(
            staff=staff_half,
            work_date=start_date + timedelta(days=i),
            defaults={'duration_minutes': 0}
        )
    print("勤務実績作成完了")
    print("--- テストデータ作成終了 ---")
    
    return staff_full, staff_part, staff_half, start_date, start_date + timedelta(days=6)

def validate_fte_logic(staff_full, staff_part, staff_half, start_date, end_date):
    """常勤換算ロジックを検証する"""
    print("\n--- 常勤換算ロジック検証開始 ---")
    
    test_cases = [
        {
            'staff': staff_full,
            'expected_fte': 1.00,
            'description': "常勤職員 (契約40h/週, 勤務40h/週)"
        },
        {
            'staff': staff_part,
            'expected_fte': 1.00,
            'description': "非常勤職員 (契約20h/週, 勤務20h/週)"
        },
        {
            'staff': staff_half,
            'expected_fte': 0.50,
            'description': "非常勤（半減） (契約40h/週, 勤務20h/週)"
        },
    ]
    
    all_passed = True
    for case in test_cases:
        staff = case['staff']
        expected = case['expected_fte']
        description = case['description']
        
        fte = calculate_full_time_equivalent(staff.id, start_date, end_date)
        
        status = "✅ PASS" if fte == expected else f"❌ FAIL (期待値: {expected}, 実際: {fte})"
        
        print(f"[{status}] {staff.full_name} ({description}) -> FTE: {fte}")
        
        if fte != expected:
            all_passed = False

    print("\n--- 検証結果 ---")
    if all_passed:
        print("🎉 すべての常勤換算ロジックテストに合格しました。")
    else:
        print("⚠️ 一部の常勤換算ロジックテストが失敗しました。")
        
    return all_passed

if __name__ == '__main__':
    # 既存のデータをクリア（今回はシンプルにするためスキップ）
    # WorkRecord.objects.all().delete()
    # StaffContract.objects.all().delete()
    # Staff.objects.all().delete()
    # ServiceLocation.objects.all().delete()
    
    staff_full, staff_part, staff_half, start_date, end_date = create_test_data()
    validate_fte_logic(staff_full, staff_part, staff_half, start_date, end_date)
