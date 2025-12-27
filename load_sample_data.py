"""
サンプルデータ自動投入スクリプト
管理画面の使い方を学ぶためのサンプルデータを作成します
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from billing_management.models import Client, Staff, ServiceLocation
from datetime import date

def load_sample_data():
    """サンプルデータを投入"""
    
    print("=" * 60)
    print("📊 サンプルデータ投入開始")
    print("=" * 60)
    
    # 既存のサンプルデータを削除
    print("\n🗑️  既存のサンプルデータを削除中...")
    Client.objects.filter(client_code__startswith='SAMPLE').delete()
    Staff.objects.filter(staff_code__startswith='SAMPLE').delete()
    ServiceLocation.objects.filter(location_id__startswith='SAMPLE').delete()
    
    # サンプル事業所を作成（Staffモデルに必要）
    print("\n🏢 サンプル事業所を作成中...")
    sample_location, created = ServiceLocation.objects.get_or_create(
        location_id='SAMPLE_LOC01',
        defaults={
            'location_name': 'サンプル事業所'
        }
    )
    if created:
        print(f"   ✅ {sample_location.location_name} を作成しました")
    else:
        print(f"   ℹ️  {sample_location.location_name} は既に存在します")
    
    # サンプル利用者を作成
    print("\n👥 サンプル利用者を作成中...")
    
    sample_clients = [
        {
            'client_code': 'SAMPLE001',
            'full_name': '田中 太郎',
            'birth_date': date(1990, 4, 15),
            'recipient_number': '1234567890',
            'guardian_name': '田中 一郎',
            'guardian_email': 'tanaka@example.com',
            'long_term_goal': '日常生活動作の自立を目指す',
            'short_term_goal': '歩行訓練を継続する',
            'support_content': '理学療法士による歩行訓練、作業療法士による日常生活動作訓練',
        },
        {
            'client_code': 'SAMPLE002',
            'full_name': '佐藤 花子',
            'birth_date': date(1985, 8, 22),
            'recipient_number': '2345678901',
            'guardian_name': '佐藤 次郎',
            'guardian_email': 'sato@example.com',
            'long_term_goal': 'コミュニケーション能力の向上',
            'short_term_goal': '言語療法を週2回実施',
            'support_content': '言語聴覚士による言語訓練、グループ活動への参加',
        },
        {
            'client_code': 'SAMPLE003',
            'full_name': '鈴木 一郎',
            'birth_date': date(1995, 12, 3),
            'recipient_number': '3456789012',
            'guardian_name': '鈴木 三郎',
            'guardian_email': 'suzuki@example.com',
            'long_term_goal': '就労に向けた準備',
            'short_term_goal': '作業訓練を通じて集中力を高める',
            'support_content': '作業訓練、職業相談、ソーシャルスキルトレーニング',
        },
        {
            'client_code': 'SAMPLE004',
            'full_name': '高橋 美咲',
            'birth_date': date(1988, 6, 10),
            'recipient_number': '4567890123',
            'guardian_name': '高橋 四郎',
            'guardian_email': 'takahashi@example.com',
            'long_term_goal': '身体機能の維持・向上',
            'short_term_goal': 'リハビリテーションを継続',
            'support_content': '理学療法、作業療法、レクリエーション活動',
        },
        {
            'client_code': 'SAMPLE005',
            'full_name': '伊藤 健太',
            'birth_date': date(1992, 3, 25),
            'recipient_number': '5678901234',
            'guardian_name': '伊藤 五郎',
            'guardian_email': 'ito@example.com',
            'long_term_goal': '社会参加の促進',
            'short_term_goal': '外出訓練を月2回実施',
            'support_content': '外出訓練、公共交通機関の利用訓練、買い物訓練',
        },
    ]
    
    for client_data in sample_clients:
        client, created = Client.objects.get_or_create(
            client_code=client_data['client_code'],
            defaults=client_data
        )
        if created:
            print(f"   ✅ {client.full_name} さんを作成しました")
        else:
            print(f"   ℹ️  {client.full_name} さんは既に存在します")
    
    # サンプルスタッフを作成
    print("\n👨‍💼 サンプルスタッフを作成中...")
    
    sample_staff = [
        {
            'staff_code': 'SAMPLE_STF001',
            'full_name': '山田 太郎',
            'is_specialist': True,
            'location': sample_location,
        },
        {
            'staff_code': 'SAMPLE_STF002',
            'full_name': '中村 花子',
            'is_specialist': True,
            'location': sample_location,
        },
        {
            'staff_code': 'SAMPLE_STF003',
            'full_name': '小林 健太',
            'is_specialist': False,
            'location': sample_location,
        },
    ]
    
    for staff_data in sample_staff:
        staff, created = Staff.objects.get_or_create(
            staff_code=staff_data['staff_code'],
            defaults=staff_data
        )
        if created:
            print(f"   ✅ {staff.full_name} さんを作成しました")
        else:
            print(f"   ℹ️  {staff.full_name} さんは既に存在します")
    
    # 統計情報を表示
    print("\n" + "=" * 60)
    print("📊 サンプルデータ投入完了！")
    print("=" * 60)
    print(f"\n✅ 事業所: {ServiceLocation.objects.count()}箇所（うちサンプル: 1箇所）")
    print(f"✅ 利用者: {Client.objects.count()}名（うちサンプル: {len(sample_clients)}名）")
    print(f"✅ スタッフ: {Staff.objects.count()}名（うちサンプル: {len(sample_staff)}名）")
    
    print("\n" + "=" * 60)
    print("🎉 管理画面でサンプルデータを確認できます！")
    print("=" * 60)
    print("\n📋 次のステップ:")
    print("   1. 管理画面にログイン: /admin/")
    print("   2. 左メニューから「Billing Management」→「利用者」をクリック")
    print("   3. SAMPLEで始まる利用者が表示されます")
    print("   4. 利用者名をクリックすると詳細が表示されます")
    print("   5. 「保存」ボタンで変更を保存できます")
    print("\n💡 ヒント:")
    print("   - サンプルデータは自由に編集・削除できます")
    print("   - 「利用者を追加」ボタンで新しい利用者を追加できます")
    print("   - 同様にスタッフ、事業所も管理できます")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    load_sample_data()
