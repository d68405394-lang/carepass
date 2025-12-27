from django.shortcuts import render
from billing_management.models import Client, ProgressAssessment, Staff, WorkRecord

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
    
    # 利用者ごとに最新の評価をグループ化
    from collections import defaultdict
    client_reports = defaultdict(list)
    
    for assessment in assessments:
        client_reports[assessment.client.client_code].append(assessment)
    
    context = {
        'clients': clients,
        'client_reports': dict(client_reports),
    }
    return render(request, 'guardian.html', context)
