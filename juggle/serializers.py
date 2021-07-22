from rest_framework import serializers
from juggle.models import Job, JobApplication, Professional


class EntitySerializer(serializers.BaseSerializer):
    pass


class ProfessionalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professional


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job


class JobApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JobApplication
