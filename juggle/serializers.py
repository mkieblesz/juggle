from rest_framework import serializers
from juggle.models import Job, JobApplication, Professional


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ["full_name"]


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["professional", "job", "date"]


class JobApplicationSerializer(serializers.ModelSerializer):
    professional = ProfessionalSerializer()

    class Meta:
        model = JobApplication
        fields = ["professional", "job", "date"]


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["title"]
