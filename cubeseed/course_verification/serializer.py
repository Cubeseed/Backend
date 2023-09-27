from rest_framework import serializers
from .models import CourseVerification


class CourseVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseVerification
        fields = '__all__'