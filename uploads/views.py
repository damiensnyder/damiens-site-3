from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Upload

class UploadView(CreateView):
    model = Upload
    fields = ['file']
    success_url = "/upload/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Upload.objects.all()
        return context
