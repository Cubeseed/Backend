from rest_framework import serializers
from .models import courseVerification


class CourseVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = courseVerification
        fields = '__all__'