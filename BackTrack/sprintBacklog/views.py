from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, FormView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import *
from .forms import *


# Create your views here.
class SprintBacklogMain(TemplateView):
    template_name = "sprint_backlog_main.html"

    def get_context_data(self, **kwargs):
        project = self.kwargs['project_pk']
        sprintBacklog = SprintBacklog.objects.get(project__pk=project)
