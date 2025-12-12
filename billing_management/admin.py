from django.contrib import admin
from .models import ServiceLocation, Staff, StaffContract, WorkRecord, Client, ProgressAssessment, FTESufficientStatus, StaffPeerReview

# 管理画面にモデルを登録
admin.site.register(ServiceLocation)
admin.site.register(Staff)
admin.site.register(StaffContract)
admin.site.register(WorkRecord)
admin.site.register(Client)
admin.site.register(ProgressAssessment)
admin.site.register(FTESufficientStatus)
admin.site.register(StaffPeerReview)
