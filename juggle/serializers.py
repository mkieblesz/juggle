from rest_framework import serializers
from juggle.models import Job, JobApplication, Professional


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ["full_name"]


class JobApplicationSerializer(serializers.ModelSerializer):
    professional = ProfessionalSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = ["professional", "job", "date"]


class JobSerializer(serializers.ModelSerializer):
    job_application = JobApplicationSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = ["title"]
