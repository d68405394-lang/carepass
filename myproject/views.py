from django.shortcuts import render

def home(request):
    """ランディングページ"""
    return render(request, 'index.html')

def progress(request):
    """進捗管理ページ"""
    return render(request, 'progress.html')

def ai_analysis(request):
    """AI分析ページ"""
    return render(request, 'ai_analysis.html')

def billing(request):
    """請求管理ページ"""
    return render(request, 'billing.html')

def guardian(request):
    """保護者ポータルページ"""
    return render(request, 'guardian.html')
