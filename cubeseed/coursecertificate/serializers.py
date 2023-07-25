from rest_framework import serializers
from cubeseed.coursecertificate.models import CourseCertificate
from cubeseed.userprofile.serializers import UserProfileSerializer


class CourseCertificateSerializer(serializers.ModelSerializer):
    reviewed_by = UserProfileSerializer()
    user = UserProfileSerializer()

    class Meta:
        model = CourseCertificate
        fields = [
            "name",
            "review_status",
            "reviewed_by",
            "reviewed_date",
            "user"
        ]
        read_only_fields = ["reviewed_by", "user"]
