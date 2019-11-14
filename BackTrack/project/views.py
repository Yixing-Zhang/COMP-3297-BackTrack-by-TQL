from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.views.generic import TemplateView, FormView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import *
from .forms import *


# Create your views here.
class ProjectMain(TemplateView):
    template_name = "project_main.html"

    def get_context_data(self, **kwargs):
        request = self.request
        user = request.user
        if request.user.is_authenticated:
            if request.user.is_superuser:
                project_list = Project.objects.all()
            elif request.user.groups.filter(name='Owner').exists():
                project_list = Project.objects.filter(owner__pk=user.pk)
            elif request.user.groups.filter(name='Manager').exists():
                project_list = Project.objects.filter(manager__pk=user.pk)
            else:
                if user.project is not None:
                    project_list = [user.project]
                else:
                    project_list = None
        else:
            project_list = None

        context = super().get_context_data(**kwargs)
        context['project_list'] = project_list
        return context


class ProjectDetail(TemplateView):
    template_name = "project_detail.html"

    def get_context_data(self, **kwargs):
        project_pk = self.kwargs['project_pk']
        project = Project.objects.get(pk=project_pk)

        context = super().get_context_data(**kwargs)
        context['project'] = project
        return context
