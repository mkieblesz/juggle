from rest_framework import serializers
from juggle.models import Job, JobApplication, Professional


class ProfessionalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professional


class JobApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JobApplication


class JobSerializer(serializers.HyperlinkedModelSerializer):
    job_application = JobApplicationSerializer(many=True, read_only=True)

    class Meta:
        model = Job
