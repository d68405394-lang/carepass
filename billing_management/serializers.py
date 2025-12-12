from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import WorkRecord

class WorkRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkRecord
        fields = '__all__'

    def validate(self, data):
        """
        WorkRecordモデルのclean()メソッド（兼務専従チェックロジック）を
        API経由でのデータ保存時にも強制的に実行する。
        """
        # インスタンスが既に存在する場合は、既存のインスタンスを更新
        instance = WorkRecord(**data)
        if self.instance:
            instance.pk = self.instance.pk
        
        try:
            instance.clean()
        except ValidationError as e:
            # DjangoのValidationErrorをDRFのValidationErrorに変換
            raise serializers.ValidationError(e.message_dict)
            
        return data

from .models import ProgressAssessment

class ProgressAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressAssessment
        # 画像・動画URLとAI分析結果のフックを含める
        fields = ['client', 'staff', 'assessment_date', 'progress_score', 
                  'specialist_comment', 'media_url', 'analysis_result_json',
                  'nlp_keyword_tags', 'sentiment_score']
from .models import FTESufficientStatus

class FTESufficientStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FTESufficientStatus
        fields = '__all__'
from .models import StaffPeerReview

class StaffPeerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPeerReview
        fields = ['reviewer', 'reviewed_staff', 'cooperation_score', 'review_comment']
