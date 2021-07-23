from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from juggle.models import Business, Job, JobApplication, Professional
from juggle.serializers import JobApplicationSerializer, JobSerializer


class EntitySearch(APIView):
    def get(self, request, format=None):
        query = request.data.get("query", None)
        entities = [
            {"type": "professional", "full_name": p.full_name}
            for p in Professional.objects.all()
            if not query or query in p.full_name
        ] + [
            {"type": "business", "company_name": b.company_name}
            for b in Business.objects.all()
            if not query or query in b.company_name
        ]
        return Response(entities)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
