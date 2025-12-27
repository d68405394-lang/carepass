"""
サンプルデータ自動投入スクリプト
管理画面の使い方を学ぶためのサンプルデータを作成します
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from billing_management.models import Client, Staff
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
    
    # サンプル利用者を作成
    print("\n👥 サンプル利用者を作成中...")
    
    sample_clients = [
        {
            'client_code': 'SAMPLE001',
            'last_name': '田中',
            'first_name': '太郎',
            'date_of_birth': date(1990, 4, 15),
            'recipient_number': '1234567890',
            'is_active': True,
        },
        {
            'client_code': 'SAMPLE002',
            'last_name': '佐藤',
            'first_name': '花子',
            'date_of_birth': date(1985, 8, 22),
            'recipient_number': '2345678901',
            'is_active': True,
        },
        {
            'client_code': 'SAMPLE003',
            'last_name': '鈴木',
            'first_name': '一郎',
            'date_of_birth': date(1995, 12, 3),
            'recipient_number': '3456789012',
            'is_active': True,
        },
        {
            'client_code': 'SAMPLE004',
            'last_name': '高橋',
            'first_name': '美咲',
            'date_of_birth': date(1988, 6, 10),
            'recipient_number': '4567890123',
            'is_active': False,
        },
        {
            'client_code': 'SAMPLE005',
            'last_name': '伊藤',
            'first_name': '健太',
            'date_of_birth': date(1992, 3, 25),
            'recipient_number': '5678901234',
            'is_active': True,
        },
    ]
    
    for client_data in sample_clients:
        client, created = Client.objects.get_or_create(
            client_code=client_data['client_code'],
            defaults=client_data
        )
        if created:
            print(f"   ✅ {client.last_name} {client.first_name} さんを作成しました")
        else:
            print(f"   ℹ️  {client.last_name} {client.first_name} さんは既に存在します")
    
    # サンプルスタッフを作成
    print("\n👨‍💼 サンプルスタッフを作成中...")
    
    sample_staff = [
        {
            'staff_code': 'SAMPLE_STF001',
            'last_name': '山田',
            'first_name': '太郎',
            'position': '介護福祉士',
            'hourly_rate': 1500,
            'is_active': True,
        },
        {
            'staff_code': 'SAMPLE_STF002',
            'last_name': '中村',
            'first_name': '花子',
            'position': '社会福祉士',
            'hourly_rate': 1800,
            'is_active': True,
        },
        {
            'staff_code': 'SAMPLE_STF003',
            'last_name': '小林',
            'first_name': '健太',
            'position': 'サービス提供責任者',
            'hourly_rate': 2000,
            'is_active': True,
        },
    ]
    
    for staff_data in sample_staff:
        staff, created = Staff.objects.get_or_create(
            staff_code=staff_data['staff_code'],
            defaults=staff_data
        )
        if created:
            print(f"   ✅ {staff.last_name} {staff.first_name} さんを作成しました")
        else:
            print(f"   ℹ️  {staff.last_name} {staff.first_name} さんは既に存在します")
    
    # 統計情報を表示
    print("\n" + "=" * 60)
    print("📊 サンプルデータ投入完了！")
    print("=" * 60)
    print(f"\n✅ 利用者: {Client.objects.count()}名（うちサンプル: {len(sample_clients)}名）")
    print(f"✅ スタッフ: {Staff.objects.count()}名（うちサンプル: {len(sample_staff)}名）")
    
    print("\n" + "=" * 60)
    print("🎉 管理画面でサンプルデータを確認できます！")
    print("=" * 60)
    print("\n📋 次のステップ:")
    print("   1. 管理画面にログイン: /admin/")
    print("   2. 左メニューから「利用者管理」→「利用者」をクリック")
    print("   3. SAMPLEで始まる利用者が表示されます")
    print("   4. 利用者名をクリックすると詳細が表示されます")
    print("   5. 「保存」ボタンで変更を保存できます")
    print("\n💡 ヒント:")
    print("   - サンプルデータは自由に編集・削除できます")
    print("   - 「利用者を追加」ボタンで新しい利用者を追加できます")
    print("   - 同様にスタッフも管理できます")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    load_sample_data()
