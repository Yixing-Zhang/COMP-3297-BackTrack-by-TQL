from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, FormView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import *
from project.models import Project
from productBacklog.models import ProductBacklog, PBI
from .forms import *


# Create your views here.
def active(request, project_pk, sprint_pk):
    project = Project.objects.get(pk=project_pk)
    sprintBacklog = SprintBacklog.objects.get(pk=sprint_pk)
    project.activeSprint = sprintBacklog
    project.save()
    return HttpResponseRedirect('/project/' + str(project_pk) + '/sprintBacklog')


def add(request, project_pk, pbi_pk):
    pbi = PBI.objects.get(pk=pbi_pk)
    project = Project.objects.get(pk=project_pk)
    sprintBacklog = project.activeSprint
    pbi.sprintBacklog = sprintBacklog
    pbi.status = 'In process'
    pbi.save()
    return HttpResponseRedirect('/project/' + str(project_pk) + '/sprintBacklog/pbi/add')


def remove(request, project_pk, pbi_pk):
    pbi = PBI.objects.get(pk=pbi_pk)
    pbi.sprintBacklog = None
    pbi.status = 'Ready'
    pbi.save()
    return HttpResponseRedirect('/project/' + str(project_pk) + '/sprintBacklog')


def finish(request, project_pk):
    project = Project.objects.get(pk=project_pk)
    sprintBacklog = project.activeSprint
    if sprintBacklog is not None:
        sprintBacklog.status = 'Finished'
        sprintBacklog.save()
        pbi_list = PBI.objects.filter(sprintBacklog__pk=sprintBacklog.pk)
        for pbi in pbi_list:
            pbi.status = 'Finished'
            task = Task.objects.filter(pbi__pk=pbi.pk)
            for t in task:
                t.status = 'Finished'
                t.save()
            pbi.save()
    project.activeSprint = None
    project.save()
    return HttpResponseRedirect('/project/' + str(project_pk) + '/sprintBacklog')


class SprintBacklogMain(TemplateView):
    template_name = "sprintbacklog_main.html"

    def get_context_data(self, **kwargs):
        project = self.kwargs['project_pk']
        sprintBacklog = Project.objects.get(pk=project).activeSprint

        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=project)
        if sprintBacklog is not None:
            pbi_list = PBI.objects.filter(sprintBacklog__pk=sprintBacklog.pk).order_by('priority')
            tasks = []
            totalHours = 0
            totalRemainingHours = 0
            for pbi in pbi_list:
                task = Task.objects.filter(pbi__pk=pbi.pk)
                hours = 0
                remainingHours = 0
                for t in task:
                    if t.status == 'In process':
                        remainingHours += t.estimated
                    hours += t.estimated
                pbi.taskHours = hours
                pbi.remainingTaskHours = remainingHours
                totalHours += hours
                totalRemainingHours += remainingHours
                tasks.append(task)
            context['totalHours'] = totalHours
            context['totalRemainingHours'] = totalRemainingHours
            rows = zip(pbi_list, tasks)
            context['rows'] = rows
        return context


class SprintPBIMain(TemplateView):
    template_name = "sprint_pbi_main.html"

    def get_context_data(self, **kwargs):
        project = self.kwargs['project_pk']
        pbi = self.kwargs['pbi_pk']

        context = super().get_context_data(**kwargs)
        context['delete'] = str(pbi) + '/delete'
        context['modify'] = str(pbi) + '/modify'
        context['back'] = '/project/' + str(project) + '/productBacklog'
        context["project"] = Project.objects.get(pk=project)
        context['pbi'] = PBI.objects.get(pk=pbi)
        return context


class SprintPBIAdd(TemplateView):
    template_name = 'sprint_pbi_add.html'

    def get_context_data(self, **kwargs):
        project = self.kwargs['project_pk']
        productBacklog = ProductBacklog.objects.get(project__pk=project)

        context = super().get_context_data(**kwargs)
        context["project"] = Project.objects.get(pk=project)
        context['pbi_list'] = PBI.objects.filter(productBacklog__pk=productBacklog.pk).order_by('priority')
        cumulative = 0
        for pbi in context['pbi_list']:
            if pbi.status == 'Ready':
                cumulative += pbi.estimated
                pbi.cumulative = cumulative
        return context


class SprintBacklogAdd(FormView):
    template_name = "sprintbacklog_add.html"
    form_class = SprintForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        project_pk = self.kwargs['project_pk']
        project = Project.objects.get(pk=project_pk)
        if form.is_valid():
            sprintBacklog = form.save(commit=False)
            sprintBacklog.status = "In process"
            sprintBacklog.project = project
            sprintBacklog.save()
            return HttpResponseRedirect('/project/' + str(project_pk) + '/sprintBacklog/' + str(sprintBacklog.pk))

        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        project = self.kwargs['project_pk']

        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=project)
        context['form'] = SprintForm()
        return context
