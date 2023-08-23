from rest_framework import serializers
from cubeseed.filedescriptor.models import CourseCertificateFile

class CourseCertificateFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCertificateFile
        fields = ["id", "review_status", "reviewed_by", "reviewed_date", "farmer_profile", "certificate"]