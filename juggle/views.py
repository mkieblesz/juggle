from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if JobApplication.objects.filter(serializer.job, date=date.today()).count() >= 5:
            return Response({"message": "You can't apply for this job today"}, status=400)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=200, headers=headers)
