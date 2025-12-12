import os
import django
from datetime import date
from django.core.exceptions import ValidationError

# Django環境のセットアップ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from billing_management.models import ServiceLocation, Staff, StaffContract, WorkRecord

def run_validation_tests():
    """兼務専従チェックの検証テストを実行する"""
    
    # 既存のテストデータをクリア（WorkRecordのみ）
    WorkRecord.objects.all().delete()
    
    # --- ステップ 1: テストデータの準備 ---
    print("--- ステップ 1: テストデータの準備 ---")
    
    # 1. ユーザー作成
    user_taro, _ = User.objects.get_or_create(username='taro_jo', defaults={'password': 'password123'})

    # 2. 事業所作成
    location, _ = ServiceLocation.objects.get_or_create(location_id='LOC01', defaults={'location_name': '本店'})

    # 3. 常勤職員作成
    staff_taro, _ = Staff.objects.get_or_create(
        staff_code='STF001',
        defaults={'full_name': '常勤 太郎', 'is_specialist': True, 'location': location}
    )
    # ユーザーとの紐付け（今回は不要だが、将来のために）
    # staff_taro.user = user_taro
    # staff_taro.save()

    # 4. 常勤契約を付与
    StaffContract.objects.get_or_create(
        staff=staff_taro,
        contract_start_date=date(2025, 1, 1),
        defaults={'contract_hours_week': 40, 'is_permanent': True}
    )

    print("テストデータ作成完了: 常勤職員(STF001)と常勤契約を登録しました。")
    
    # --- ステップ 2: 検証ケースの実行 ---
    print("\n--- ステップ 2: 検証ケースの実行 ---")
    
    # 1. 成功ケース：主たるサービス（Hodei）の勤務を登録
    try:
        record_hodei_day1 = WorkRecord.objects.create(
            staff=staff_taro,
            work_date=date(2025, 12, 10),
            service_type='Hodei',
            duration_minutes=480 # 8時間
        )
        print("\n[検証 1: 成功] Hodei 勤務の登録に成功しました。✅")
    except ValidationError as e:
        print(f"\n[検証 1: 失敗] 予期せぬエラー: {e} ❌")
        return # 失敗したら以降のテストは中断

    # 2. 成功ケース：主たるサービス登録後に、兼務サービス（Miniha）の勤務を登録
    try:
        record_miniha_day1 = WorkRecord.objects.create(
            staff=staff_taro,
            work_date=date(2025, 12, 10),
            service_type='Miniha',
            duration_minutes=60 # 1時間
        )
        print("\n[検証 2: 成功] Hodei登録後の Miniha 勤務の登録に成功しました。✅")
    except ValidationError as e:
        print(f"\n[検証 2: 失敗] 予期せぬエラー: {e} ❌")
        return # 失敗したら以降のテストは中断

    # 3. 失敗ケース：主たるサービス登録なしに、兼務サービス（Miniha）の勤務を登録
    try:
        record_miniha_day2 = WorkRecord(
            staff=staff_taro,
            work_date=date(2025, 12, 11),
            service_type='Miniha',
            duration_minutes=60
        )
        # save()を呼ぶことで、内部でclean()が実行される
        record_miniha_day2.save() 
        print("\n[検証 3: 失敗] エラーが発生しませんでした。ロジックに不備がある可能性があります。❌")
    except ValidationError as e:
        # ValidationErrorのメッセージを整形して表示
        message = e.message_dict.get('__all__', ['不明なエラー'])[0]
        print(f"\n[検証 3: 合格] 期待通り ValidationError が発生しました。システムが不正な入力をブロックしました。✅")
        print(f"エラーメッセージ: {message}")
    except Exception as e:
        print(f"\n[検証 3: 失敗] 予期せぬ例外が発生しました: {e} ❌")

if __name__ == '__main__':
    run_validation_tests()
