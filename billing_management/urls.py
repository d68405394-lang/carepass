from django.urls import path
from . import views

urlpatterns = [
    # 勤務実績の登録・一覧 (兼務専従チェックを強制実行)
    path('workrecords/', views.WorkRecordListCreate.as_view(), name='workrecord_list_create'),
    
    # 進捗・評価の登録・一覧 (画像/動画URLとAI分析結果の送受信を想定)
    path('progress/', views.ProgressAssessmentListCreate.as_view(), name='progress_assessment_list_create'),

    # 加算充足ステータスの登録・一覧 (経営ダッシュボード用)
    path('dashboard/fte/', views.FTESufficientStatusList.as_view(), name='fte_status_list'),

    # 職員相互評価の登録・一覧
    path('peerreview/', views.StaffPeerReviewListCreate.as_view(), name='peer_review_list_create'),
    path('evaluation/summary/', views.StaffEvaluationSummary.as_view(), name='staff_evaluation_summary'),
    
    # 国保連請求 CSV エクスポート API (弱みゼロ化の第一歩)
    path('export/kokuhoren_csv/', views.KokuhorenCsvExport.as_view(), name='kokuhoren_csv_export'),
    
    # 給与計算 CSV エクスポート API (運用負担のゼロ化)
    path('export/payroll_csv/', views.PayrollCsvExport.as_view(), name='payroll_csv_export'),
    
    # 会計 CSV エクスポート API (経理連携の自動化)
    path('export/accounting_csv/', views.AccountingCsvExport.as_view(), name='accounting_csv_export'),
    
    # 個別支援計画書 PDF エクスポート API (指導監査対応の自動化)
    path('export/support_plan_pdf/<int:client_id>/', views.SupportPlanPdfExport.as_view(), name='support_plan_pdf_export'),
    
    # 利用者一覧 API
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    
    # AI感情分析 API (強みの増強)
    path('analyze_sentiment/<int:assessment_id>/', views.SentimentAnalysisView.as_view(), name='sentiment_analysis'),
    
    # AI分析結果一覧 API
    path('analysis_results/', views.AnalysisResultListView.as_view(), name='analysis_results'),
    
    # 利用者離脱リスク予測 API (経営判断の集大成)
    path('churn_prediction/', views.ChurnPredictionView.as_view(), name='churn_prediction'),
    path('churn_prediction/<int:client_id>/', views.ClientChurnPredictionView.as_view(), name='client_churn_prediction'),
    
    # AI記録自動生成 API (究極の記録負担軽減)
    path('ai_record_generation/', views.AiRecordGeneration.as_view(), name='ai_record_generation'),
    
    # 電子サイン保存 API (ペーパーレス化の推進)
    path('save_signature/<int:client_id>/', views.SaveSignatureView.as_view(), name='save_signature'),
    
    # 経営・財務予測AI API (経営判断の高度化)
    path('financial_forecast/', views.FinancialForecastView.as_view(), name='financial_forecast'),
    
    # メール機能 API (保護者連絡の自動化)
    path('email/send/', views.SendEmailView.as_view(), name='send_email'),
    path('email/mark_read/<int:recipient_id>/', views.MarkAsReadView.as_view(), name='mark_as_read'),
    path('email/read_status/<int:message_id>/', views.ReadStatusView.as_view(), name='read_status'),
    path('email/unread/<int:client_id>/', views.UnreadMessagesView.as_view(), name='unread_messages'),
    path('email/history/', views.MessageHistoryView.as_view(), name='message_history'),
    
    # 保護者ポータル API (保護者向け情報公開)
    path('guardian/login/', views.GuardianLoginView.as_view(), name='guardian_login'),
    path('guardian/logout/', views.GuardianLogoutView.as_view(), name='guardian_logout'),
    path('guardian/dashboard/<int:client_id>/', views.GuardianDashboardView.as_view(), name='guardian_dashboard'),
    path('guardian/activities/<int:client_id>/', views.ActivityLogView.as_view(), name='activity_log'),
    
    # ゲーミフィケーション API (モチベーション向上)
    path('gamification/badges/<int:client_id>/', views.ClientBadgesView.as_view(), name='client_badges'),
    path('gamification/check_badges/<int:client_id>/', views.CheckBadgesView.as_view(), name='check_badges'),
    path('gamification/points/<int:client_id>/', views.ClientPointsView.as_view(), name='client_points'),
    path('gamification/award_points/<int:client_id>/', views.AwardPointsView.as_view(), name='award_points'),
    path('gamification/leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    
    # 事業所一覧 API (事故報告書用)
    path('service-locations/', views.ServiceLocationListView.as_view(), name='service_location_list'),
]
