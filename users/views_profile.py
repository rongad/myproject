from .models import Profile
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm
from django.http import HttpResponseRedirect

class ProfileView(LoginRequiredMixin,ListView):
    model = Profile
    template_name = "profile/list.html"
    context_object_name = "profiles"

    def get_queryset(self):
        return Profile.objects.all()
    
class ProfileCreateView(CreateView):
    model = Profile
    success_url = "http://127.0.0.1:8000/profiles"
    form_class = ProfileForm
    template_name = "profile/create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
class ProfileDeleteView(DeleteView):
    model = Profile
    success_url = "http://127.0.0.1:8000/profiles"
    template_name = "profile/delete.html"

class ProfileUpdateView(UpdateView):
    model = Profile
    success_url = "http://127.0.0.1:8000/profiles"
    form_class = ProfileForm    
    template_name = "profile/create.html"