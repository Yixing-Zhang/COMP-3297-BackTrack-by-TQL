from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, FormView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import *
from project.models import Project
from productBacklog.models import ProductBacklog, PBI
from .forms import *


# Create your views here.
class SprintBacklogMain(UpdateView):
    template_name = "sprintbacklog_main.html"
    form_class = BasicForm

    def get_success_url(self):
        project = self.kwargs['project_pk']
        url = '/project/' + str(project) + "/sprintBacklog"
        return url

    def get_object(self, queryset=None):
        project = self.kwargs['project_pk']
        return Project.objects.get(pk=project)

    def form_valid(self, form):
        project = form.save(commit=False)
        project.activeSprint = None
        project.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        project = self.kwargs['project_pk']
        sprintBacklog = Project.objects.get(pk=project).activeSprint

        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=project)
        if sprintBacklog is not None:
            pbi_list = PBI.objects.filter(sprintBacklog__pk=sprintBacklog.pk).order_by('priority')
            tasks = []
            totalHours = 0
            for pbi in pbi_list:
                task = Task.objects.filter(pbi__pk=pbi.pk)
                hours = 0
                for t in task:
                    hours += t.estimated
                pbi.taskHours = hours
                totalHours += hours
                tasks.append(task)
            context['totalHours'] = totalHours
            rows = zip(pbi_list, tasks)
            context['rows'] = rows
        return context
