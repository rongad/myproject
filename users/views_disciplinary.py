from .models import DisciplinaryIncident
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import IncidentForm

class IncidentView(LoginRequiredMixin,ListView):
    model = DisciplinaryIncident
    template_name = "disciplinary/incident_list.html"
    context_object_name = "incidents"

    def get_queryset(self):
        return DisciplinaryIncident.objects.all()

class IncidentCreateView(CreateView):
    model = DisciplinaryIncident
    success_url = "http://127.0.0.1:8000/incidents"
    form_class = IncidentForm
    template_name = "disciplinary/create_incident.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class IncidentDeleteView(DeleteView):
    model = DisciplinaryIncident
    success_url = "http://127.0.0.1:8000/incidents"
    template_name = "disciplinary/delete_incident.html"

class IncidentUpdateView(UpdateView):
    model = DisciplinaryIncident
    success_url = "http://127.0.0.1:8000/incidents"
    form_class = IncidentForm    
    template_name = "disciplinary/create_incident.html"
