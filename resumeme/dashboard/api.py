from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Resume, Template, JobApplication
from .serializers import ResumeSerializer, TemplateSerializer, JobApplicationSerializer

class ResumeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ResumeSerializer

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def generate_pdf(self, request, pk=None):
        resume = self.get_object()
        # Generate PDF logic here
        return Response({'pdf_url': 'url_to_pdf'})