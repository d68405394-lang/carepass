"""
Django管理コマンド: サンプルデータ投入
Renderの無料プランでも実行可能
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from billing_management.models import Client, Staff, ServiceLocation, CustomUser
from datetime import date


class Command(BaseCommand):
    help = 'マルチテナント対応のサンプルデータを投入'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("📊 サンプルデータ投入開始（マルチテナント対応）")
        self.stdout.write("=" * 60)
        
        # 既存のサンプルデータを削除
        self.stdout.write("\n🗑️  既存のサンプルデータを削除中...")
        try:
            Client.objects.filter(client_code__startswith='SAMPLE').delete()
        except Exception as e:
            self.stdout.write(f"   ⚠️  Client削除時にエラー: {e}")
        try:
            Staff.objects.filter(staff_code__startswith='SAMPLE').delete()
        except Exception as e:
            self.stdout.write(f"   ⚠️  Staff削除時にエラー: {e}")
        try:
            ServiceLocation.objects.filter(location_id__startswith='SAMPLE').delete()
        except Exception as e:
            self.stdout.write(f"   ⚠️  ServiceLocation削除時にエラー: {e}")
        try:
            CustomUser.objects.filter(username__startswith='sample_').delete()
        except Exception as e:
            self.stdout.write(f"   ⚠️  CustomUser削除時にエラー: {e}")
        
        # サンプル事業所を作成
        self.stdout.write("\n🏢 サンプル事業所を作成中...")
        locations_data = [
            {'code': 'SAMPLE01', 'name': 'サンプル事業所A（東京）'},
            {'code': 'SAMPLE02', 'name': 'サンプル事業所B（大阪）'},
            {'code': 'SAMPLE03', 'name': 'サンプル事業所C（名古屋）'},
        ]
        
        locations = {}
        for loc_data in locations_data:
            location, created = ServiceLocation.objects.get_or_create(
                location_id=loc_data['code'],
                defaults={
                    'location_name': loc_data['name'],
                }
            )
            locations[loc_data['code']] = location
            if created:
                self.stdout.write(f"   ✅ {loc_data['name']} を作成しました")
            else:
                self.stdout.write(f"   ℹ️  {loc_data['name']} は既に存在します")
        
        # サンプルユーザーを作成
        self.stdout.write("\n👤 サンプルユーザーを作成中...")
        
        # 1. スーパー管理者
        super_admin, created = CustomUser.objects.get_or_create(
            username='sample_superadmin',
            defaults={
                'email': 'superadmin@example.com',
                'role': 'super_admin',
                'location': None,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            super_admin.set_password('admin123')
            super_admin.save()
            self.stdout.write(f"   ✅ スーパー管理者: {super_admin.username} を作成しました")
            self.stdout.write(f"      パスワード: admin123")
        else:
            self.stdout.write(f"   ℹ️  スーパー管理者: {super_admin.username} は既に存在します")
        
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
                self.stdout.write(f"   ✅ 事業所管理者: {admin.username} ({admin.location.location_name}) を作成しました")
            else:
                self.stdout.write(f"   ℹ️  事業所管理者: {admin.username} は既に存在します")
            
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
                self.stdout.write(f"   ✅ スタッフ: {staff_user.username} ({staff_user.location.location_name}) を作成しました")
            else:
                self.stdout.write(f"   ℹ️  スタッフ: {staff_user.username} は既に存在します")
            
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
        self.stdout.write("\n👥 サンプル利用者を作成中...")
        clients_data = [
            {'code': 'SAMPLE001', 'name': '田中 太郎', 'location': locations['SAMPLE01'], 'birth_date': date(1990, 4, 15), 'recipient_number': '1234567890'},
            {'code': 'SAMPLE002', 'name': '佐藤 花子', 'location': locations['SAMPLE01'], 'birth_date': date(1985, 8, 22), 'recipient_number': '2345678901'},
            {'code': 'SAMPLE003', 'name': '鈴木 一郎', 'location': locations['SAMPLE02'], 'birth_date': date(1992, 2, 10), 'recipient_number': '3456789012'},
            {'code': 'SAMPLE004', 'name': '高橋 美咲', 'location': locations['SAMPLE02'], 'birth_date': date(1988, 11, 5), 'recipient_number': '4567890123'},
            {'code': 'SAMPLE005', 'name': '伊藤 健太', 'location': locations['SAMPLE03'], 'birth_date': date(1995, 6, 30), 'recipient_number': '5678901234'},
        ]
        
        for client_data in clients_data:
            client, created = Client.objects.get_or_create(
                client_code=client_data['code'],
                defaults={
                    'full_name': client_data['name'],
                    'location': client_data['location'],
                    'birth_date': client_data['birth_date'],
                    'recipient_number': client_data['recipient_number'],
                }
            )
            if created:
                self.stdout.write(f"   ✅ {client.full_name} ({client.location.location_name}) を作成しました")
            else:
                self.stdout.write(f"   ℹ️  {client.full_name} は既に存在します")
        
        # サンプル職員を作成
        self.stdout.write("\n👨‍💼 サンプル職員を作成中...")
        staff_data = [
            {'code': 'STAFF001', 'name': '山田 太郎', 'location': locations['SAMPLE01']},
            {'code': 'STAFF002', 'name': '山田 花子', 'location': locations['SAMPLE01']},
            {'code': 'STAFF003', 'name': '佐々木 次郎', 'location': locations['SAMPLE02']},
            {'code': 'STAFF004', 'name': '佐々木 三郎', 'location': locations['SAMPLE02']},
        ]
        
        for staff_info in staff_data:
            staff, created = Staff.objects.get_or_create(
                staff_code=staff_info['code'],
                defaults={
                    'full_name': staff_info['name'],
                    'location': staff_info['location'],
                }
            )
            if created:
                self.stdout.write(f"   ✅ {staff.full_name} ({staff.location.location_name}) を作成しました")
            else:
                self.stdout.write(f"   ℹ️  {staff.full_name} は既に存在します")
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("✅ サンプルデータの投入が完了しました！")
        self.stdout.write("=" * 60)
        
        self.stdout.write("\n📋 作成されたデータ:")
        self.stdout.write(f"   - 事業所: {ServiceLocation.objects.filter(location_id__startswith='SAMPLE').count()}箇所")
        self.stdout.write(f"   - ユーザー: {CustomUser.objects.filter(username__startswith='sample_').count()}名")
        self.stdout.write(f"   - 利用者: {Client.objects.filter(client_code__startswith='SAMPLE').count()}名")
        self.stdout.write(f"   - 職員: {Staff.objects.filter(staff_code__startswith='SAMPLE').count()}名")
        
        self.stdout.write("\n🔑 ログイン情報:")
        self.stdout.write("   スーパー管理者:")
        self.stdout.write("     - ユーザー名: sample_superadmin")
        self.stdout.write("     - パスワード: admin123")
        self.stdout.write("\n   事業所管理者:")
        self.stdout.write("     - sample_admin_tokyo / admin123")
        self.stdout.write("     - sample_admin_osaka / admin123")
        self.stdout.write("     - sample_admin_nagoya / admin123")
        self.stdout.write("\n   スタッフ:")
        self.stdout.write("     - sample_staff_tokyo1 / staff123")
        self.stdout.write("     - sample_staff_osaka1 / staff123")
        self.stdout.write("")
