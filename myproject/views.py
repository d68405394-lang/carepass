from django.shortcuts import render, redirect
from django.contrib import messages
from billing_management.models import Client, ProgressAssessment, Staff, WorkRecord
from datetime import date

def home(request):
    """ランディングページ"""
    return render(request, 'index.html')

def progress(request):
    """進捗管理ページ"""
    # 利用者とその進捗評価データを取得
    clients = Client.objects.all()
    assessments = ProgressAssessment.objects.select_related('client', 'staff').order_by('-assessment_date')
    
    context = {
        'clients': clients,
        'assessments': assessments,
    }
    return render(request, 'progress.html', context)

def ai_analysis(request):
    """AI分析ページ"""
    # 進捗評価データを取得（AI分析用）
    assessments = ProgressAssessment.objects.select_related('client', 'staff').order_by('-assessment_date')[:10]
    
    context = {
        'assessments': assessments,
    }
    return render(request, 'ai_analysis.html', context)

def billing(request):
    """請求管理ページ"""
    # 勤務実績データを取得
    work_records = WorkRecord.objects.select_related('staff').order_by('-work_date')
    
    # 職員ごとの勤務時間集計
    from collections import defaultdict
    staff_summary = defaultdict(lambda: {'total_minutes': 0, 'records': []})
    
    for record in work_records:
        staff = record.staff
        staff_key = staff.staff_code if staff else 'N/A'
        
        staff_summary[staff_key]['staff_name'] = staff.full_name if staff else 'N/A'
        staff_summary[staff_key]['total_minutes'] += record.duration_minutes
        staff_summary[staff_key]['records'].append(record)
    
    context = {
        'work_records': work_records,
        'staff_summary': dict(staff_summary),
    }
    return render(request, 'billing.html', context)

def guardian(request):
    """保護者ポータルページ"""
    # 利用者と進捗評価データを取得
    clients = Client.objects.all()
    assessments = ProgressAssessment.objects.select_related('client', 'staff').order_by('-assessment_date')
    
    context = {
        'clients': clients,
        'client_reports': assessments,
    }
    return render(request, 'guardian.html', context)

def progress_input(request):
    """進捗記録入力フォーム"""
    if request.method == 'POST':
        # フォームデータを取得
        client_id = request.POST.get('client_id')
        staff_id = request.POST.get('staff_id')
        assessment_date = request.POST.get('assessment_date')
        progress_score = request.POST.get('progress_score')
        specialist_comment = request.POST.get('specialist_comment')
        
        # データを保存
        try:
            client = Client.objects.get(id=client_id)
            staff = Staff.objects.get(id=staff_id) if staff_id else None
            
            ProgressAssessment.objects.create(
                client=client,
                staff=staff,
                assessment_date=assessment_date,
                progress_score=progress_score,
                specialist_comment=specialist_comment
            )
            messages.success(request, '✅ 進捗記録を保存しました')
            return redirect('progress_input')
        except Exception as e:
            messages.error(request, f'❌ エラーが発生しました: {str(e)}')
    
    # フォーム表示用のデータ
    clients = Client.objects.all()
    staff_list = Staff.objects.all()
    today = date.today()
    
    context = {
        'clients': clients,
        'staff_list': staff_list,
        'today': today,
    }
    return render(request, 'progress_input.html', context)

def work_record_input(request):
    """勤務時間記録入力フォーム"""
    if request.method == 'POST':
        # フォームデータを取得
        staff_id = request.POST.get('staff_id')
        work_date = request.POST.get('work_date')
        service_type = request.POST.get('service_type')
        duration_minutes = request.POST.get('duration_minutes')
        
        # データを保存
        try:
            staff = Staff.objects.get(id=staff_id)
            
            WorkRecord.objects.create(
                staff=staff,
                work_date=work_date,
                service_type=service_type,
                duration_minutes=duration_minutes
            )
            messages.success(request, '✅ 勤務記録を保存しました')
            return redirect('work_record_input')
        except Exception as e:
            messages.error(request, f'❌ エラーが発生しました: {str(e)}')
    
    # フォーム表示用のデータ
    staff_list = Staff.objects.all()
    today = date.today()
    
    context = {
        'staff_list': staff_list,
        'today': today,
    }
    return render(request, 'work_record_input.html', context)
