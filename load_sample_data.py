"""
サンプルデータ自動投入スクリプト
管理画面の使い方を学ぶためのサンプルデータを作成します
マルチテナント対応: CustomUserモデルとロールベースのユーザーを作成
"""

import os
import sys
import django

# PYTHONPATHを設定
sys.path.insert(0, '/home/ubuntu')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from billing_management.models import Client, Staff, ServiceLocation, CustomUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from datetime import date

def load_sample_data():
    """サンプルデータを投入"""
    
    print("=" * 60)
    print("📊 サンプルデータ投入開始（マルチテナント対応）")
    print("=" * 60)
    
    # 既存のサンプルデータを削除
    print("\n🗑️  既存のサンプルデータを削除中...")
    Client.objects.filter(client_code__startswith='SAMPLE').delete()
    Staff.objects.filter(staff_code__startswith='SAMPLE').delete()
    ServiceLocation.objects.filter(location_id__startswith='SAMPLE').delete()
    CustomUser.objects.filter(username__startswith='sample').delete()
    
    # サンプル事業所を作成
    print("\n🏢 サンプル事業所を作成中...")
    
    locations_data = [
        {'location_id': 'SAMPLE01', 'location_name': 'サンプル事業所A（東京）'},
        {'location_id': 'SAMPLE02', 'location_name': 'サンプル事業所B（大阪）'},
        {'location_id': 'SAMPLE03', 'location_name': 'サンプル事業所C（名古屋）'},
    ]
    
    locations = {}
    for loc_data in locations_data:
        location, created = ServiceLocation.objects.get_or_create(
            location_id=loc_data['location_id'],
            defaults={'location_name': loc_data['location_name']}
        )
        locations[loc_data['location_id']] = location
        if created:
            print(f"   ✅ {location.location_name} を作成しました")
        else:
            print(f"   ℹ️  {location.location_name} は既に存在します")
    
    # CustomUserを作成（ロールベース）
    print("\n👤 サンプルユーザーを作成中...")
    
    # 1. スーパー管理者（全事業所を管理）
    super_admin, created = CustomUser.objects.get_or_create(
        username='sample_superadmin',
        defaults={
            'email': 'superadmin@example.com',
            'role': 'super_admin',
            'location': None,  # 全事業所にアクセス可能
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        super_admin.set_password('admin123')
        super_admin.save()
        print(f"   ✅ スーパー管理者: {super_admin.username} を作成しました")
        print(f"      パスワード: admin123")
    else:
        print(f"   ℹ️  スーパー管理者: {super_admin.username} は既に存在します")
    
    # 全てのパーミッションを付与
    all_permissions = Permission.objects.all()
    super_admin.user_permissions.set(all_permissions)
    super_admin.save()
    
    # 2. 事業所管理者（各事業所に1名ずつ）
    location_admins_data = [
        {'username': 'sample_admin_tokyo', 'email': 'admin.tokyo@example.com', 'location': locations['SAMPLE01']},
        {'username': 'sample_admin_osaka', 'email': 'admin.osaka@example.com', 'location': locations['SAMPLE02']},
        {'username': 'sample_admin_nagoya', 'email': 'admin.nagoya@example.com', 'location': locations['SAMPLE03']},
    ]
    
    for admin_data in location_admins_data:
        admin, created = CustomUser.objects.get_or_create(
            username=admin_data['username'],
            defaults={
                'email': admin_data['email'],
                'role': 'location_admin',
                'location': admin_data['location'],
                'is_staff': True,
                'is_superuser': False,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            print(f"   ✅ 事業所管理者: {admin.username} ({admin.location.location_name}) を作成しました")
        else:
            print(f"   ℹ️  事業所管理者: {admin.username} は既に存在します")
        
        # billing_managementアプリの全てのパーミッションを付与
        app_permissions = Permission.objects.filter(content_type__app_label='billing_management')
        admin.user_permissions.set(app_permissions)
        admin.save()
    
    # 3. スタッフユーザー（各事業所に2名ずつ）
    staff_users_data = [
        {'username': 'sample_staff_tokyo1', 'email': 'staff1.tokyo@example.com', 'location': locations['SAMPLE01']},
        {'username': 'sample_staff_tokyo2', 'email': 'staff2.tokyo@example.com', 'location': locations['SAMPLE01']},
        {'username': 'sample_staff_osaka1', 'email': 'staff1.osaka@example.com', 'location': locations['SAMPLE02']},
        {'username': 'sample_staff_osaka2', 'email': 'staff2.osaka@example.com', 'location': locations['SAMPLE02']},
    ]
    
    for staff_data in staff_users_data:
        staff_user, created = CustomUser.objects.get_or_create(
            username=staff_data['username'],
            defaults={
                'email': staff_data['email'],
                'role': 'staff',
                'location': staff_data['location'],
                'is_staff': True,
                'is_superuser': False,
            }
        )
        if created:
            staff_user.set_password('staff123')
            staff_user.save()
            print(f"   ✅ スタッフ: {staff_user.username} ({staff_user.location.location_name}) を作成しました")
        else:
            print(f"   ℹ️  スタッフ: {staff_user.username} は既に存在します")
        
        # billing_managementアプリの読み取りと追加パーミッションを付与
        view_permissions = Permission.objects.filter(
            content_type__app_label='billing_management',
            codename__startswith='view_'
        )
        add_permissions = Permission.objects.filter(
            content_type__app_label='billing_management',
            codename__startswith='add_'
        )
        change_permissions = Permission.objects.filter(
            content_type__app_label='billing_management',
            codename__startswith='change_'
        )
        staff_user.user_permissions.set(list(view_permissions) + list(add_permissions) + list(change_permissions))
        staff_user.save()
    
    # サンプル利用者を作成（各事業所に割り当て）
    print("\n👥 サンプル利用者を作成中...")
    
    sample_clients = [
        # 東京事業所の利用者
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
            'location': locations['SAMPLE01'],
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
            'location': locations['SAMPLE01'],
        },
        # 大阪事業所の利用者
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
            'location': locations['SAMPLE02'],
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
            'location': locations['SAMPLE02'],
        },
        # 名古屋事業所の利用者
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
            'location': locations['SAMPLE03'],
        },
    ]
    
    for client_data in sample_clients:
        client, created = Client.objects.get_or_create(
            client_code=client_data['client_code'],
            defaults=client_data
        )
        if created:
            print(f"   ✅ {client.full_name} さん ({client.location.location_name}) を作成しました")
        else:
            print(f"   ℹ️  {client.full_name} さんは既に存在します")
    
    # サンプルスタッフを作成
    print("\n👨‍💼 サンプルスタッフを作成中...")
    
    sample_staff = [
        {
            'staff_code': 'SAMPLE_STF001',
            'full_name': '山田 太郎',
            'is_specialist': True,
            'location': locations['SAMPLE01'],
        },
        {
            'staff_code': 'SAMPLE_STF002',
            'full_name': '中村 花子',
            'is_specialist': True,
            'location': locations['SAMPLE01'],
        },
        {
            'staff_code': 'SAMPLE_STF003',
            'full_name': '小林 健太',
            'is_specialist': False,
            'location': locations['SAMPLE02'],
        },
        {
            'staff_code': 'SAMPLE_STF004',
            'full_name': '渡辺 美咲',
            'is_specialist': True,
            'location': locations['SAMPLE03'],
        },
    ]
    
    for staff_data in sample_staff:
        staff, created = Staff.objects.get_or_create(
            staff_code=staff_data['staff_code'],
            defaults=staff_data
        )
        if created:
            print(f"   ✅ {staff.full_name} さん ({staff.location.location_name}) を作成しました")
        else:
            print(f"   ℹ️  {staff.full_name} さんは既に存在します")
    
    # 統計情報を表示
    print("\n" + "=" * 60)
    print("📊 サンプルデータ投入完了！")
    print("=" * 60)
    print(f"\n✅ 事業所: {ServiceLocation.objects.count()}箇所（うちサンプル: {len(locations_data)}箇所）")
    print(f"✅ ユーザー: {CustomUser.objects.count()}名")
    print(f"   - スーパー管理者: 1名")
    print(f"   - 事業所管理者: {len(location_admins_data)}名")
    print(f"   - スタッフ: {len(staff_users_data)}名")
    print(f"✅ 利用者: {Client.objects.count()}名（うちサンプル: {len(sample_clients)}名）")
    print(f"✅ スタッフ: {Staff.objects.count()}名（うちサンプル: {len(sample_staff)}名）")
    
    print("\n" + "=" * 60)
    print("🎉 管理画面でサンプルデータを確認できます！")
    print("=" * 60)
    print("\n📋 ログイン情報:")
    print("\n1️⃣  スーパー管理者（全事業所にアクセス可能）:")
    print("   ユーザー名: sample_superadmin")
    print("   パスワード: admin123")
    print("\n2️⃣  事業所管理者（自分の事業所のみ）:")
    print("   東京: sample_admin_tokyo / admin123")
    print("   大阪: sample_admin_osaka / admin123")
    print("   名古屋: sample_admin_nagoya / admin123")
    print("\n3️⃣  スタッフ（自分の事業所のみ）:")
    print("   東京: sample_staff_tokyo1 / staff123")
    print("   大阪: sample_staff_osaka1 / staff123")
    
    print("\n💡 ヒント:")
    print("   - 各ユーザーでログインして、表示されるデータが異なることを確認してください")
    print("   - スーパー管理者は全事業所のデータを見ることができます")
    print("   - 事業所管理者とスタッフは自分の事業所のデータのみ見ることができます")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    load_sample_data()
