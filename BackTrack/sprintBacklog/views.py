from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.views.generic import TemplateView, FormView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import *
from project.models import Project
from productBacklog.models import ProductBacklog, PBI
from .forms import *


# Create your views here.
def task_finish(request, project_pk, pbi_pk, task_pk):
    task = Task.objects.get(pk=task_pk)
    task.status = 'Finished'
    task.effortsDone = task.estimated
    task.save()
    return HttpResponseRedirect(
        '/project/' + str(project_pk) + '/sprintBacklog/pbi/' + str(pbi_pk) + '/task/' + str(task_pk))


def task_owner(request, project_pk, pbi_pk, task_pk):
    task = Task.objects.get(pk=task_pk)
    owner = request.user
    task.owner = owner
    task.status = 'In process'
    task.save()
    return HttpResponseRedirect(
        '/project/' + str(project_pk) + '/sprintBacklog/pbi/' + str(pbi_pk) + '/task/' + str(task_pk))


def start(request, project_pk, sprint_pk):
    sprintBacklog = SprintBacklog.objects.get(pk=sprint_pk)
    sprintBacklog.status = "In process"
    sprintBacklog.time = datetime.now()
    sprintBacklog.save()
    return HttpResponseRedirect('/project/' + str(project_pk) + '/sprintBacklog')


def active(request, project_pk, sprint_pk):
    project = Project.objects.get(pk=project_pk)
    sprintBacklog = SprintBacklog.objects.get(pk=sprint_pk)
    project.activeSprint = sprintBacklog
    project.sprintNumber += 1
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
            ready = True
            task = Task.objects.filter(pbi__pk=pbi.pk)
            for t in task:
                if t.status != "Finished":
                    if t.status == "In process":
                        pbi.status = "Unfinished"
                        ready = False
                        break
                    else:
                        pbi.status = "Unfinished"
                else:
                    ready = False
            if ready:
                pbi.status = "Ready"
            pbi.save()
    project.activeSprint = None
    project.save()
    return HttpResponseRedirect('/project/' + str(project_pk) + '/sprintBacklog')


def task_modify(request, project_pk, pbi_pk, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    pbi = PBI.objects.get(pk=pbi_pk)
    project = Project.objects.get(pk=project_pk)
    if request.method == "POST":
        form = TaskModifyForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('/project/' + str(project_pk) + '/sprintBacklog/pbi/' + str(pbi_pk) + '/task/' + str(task_pk), pk=pbi.pk)
    else:
        form = TaskModifyForm(instance=task)
    return render(request, 'task_modify.html', {'form': form, 'project': project, 'pbi': pbi, 'task': task})


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
            totalHoursDone = 0
            totalRemainingHours = 0
            for pbi in pbi_list:
                task = Task.objects.filter(pbi__pk=pbi.pk)
                hours = 0
                remainingHours = 0
                hoursDone = 0
                for t in task:
                    remainingHours += (t.estimated - t.effortsDone)
                    hours += t.estimated
                    hoursDone += t.effortsDone
                pbi.taskHours = hours
                pbi.remainingTaskHours = remainingHours
                pbi.taskHoursDone = hoursDone
                totalHours += hours
                totalRemainingHours += remainingHours
                totalHoursDone += hoursDone
                tasks.append(task)
            context['totalHours'] = totalHours
            context['totalRemainingHours'] = totalRemainingHours
            context['totalHoursDone'] = totalHoursDone
            rows = zip(pbi_list, tasks)
            context['rows'] = rows
        return context


class SprintFinishConfirm(TemplateView):
    template_name = "sprint_finish_confirm.html"

    def get_context_data(self, **kwargs):
        project = self.kwargs['project_pk']

        context = super().get_context_data(**kwargs)
        context["project"] = Project.objects.get(pk=project)
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
            if pbi.status == 'Ready' or pbi.status == "Unfinished":
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
            sprintBacklog.sprintNumber = project.sprintNumber + 1
            sprintBacklog.status = "Ready"
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


class TaskMain(TemplateView):
    template_name = "task_main.html"

    def get_context_data(self, **kwargs):
        project_pk = self.kwargs['project_pk']
        pbi_pk = self.kwargs['pbi_pk']
        task_pk = self.kwargs['task_pk']
        project = Project.objects.get(pk=project_pk)
        pbi = PBI.objects.get(pk=pbi_pk)
        task = Task.objects.get(pk=task_pk)

        context = super().get_context_data(**kwargs)
        context['project'] = project
        context['pbi'] = pbi
        context['task'] = task
        return context


class TaskOwnerConfirm(TemplateView):
    template_name = "task_owner_confirm.html"

    def get_context_data(self, **kwargs):
        project_pk = self.kwargs['project_pk']
        pbi_pk = self.kwargs['pbi_pk']
        task_pk = self.kwargs['task_pk']
        project = Project.objects.get(pk=project_pk)
        pbi = PBI.objects.get(pk=pbi_pk)
        task = Task.objects.get(pk=task_pk)

        context = super().get_context_data(**kwargs)
        context['project'] = project
        context['pbi'] = pbi
        context['task'] = task
        return context


class TaskFinishConfirm(TemplateView):
    template_name = "task_finish_confirm.html"

    def get_context_data(self, **kwargs):
        project_pk = self.kwargs['project_pk']
        pbi_pk = self.kwargs['pbi_pk']
        task_pk = self.kwargs['task_pk']
        project = Project.objects.get(pk=project_pk)
        pbi = PBI.objects.get(pk=pbi_pk)
        task = Task.objects.get(pk=task_pk)

        context = super().get_context_data(**kwargs)
        context['project'] = project
        context['pbi'] = pbi
        context['task'] = task
        return context


class TaskAdd(FormView):
    template_name = "task_add.html"
    form_class = TaskAddForm

    def post(self, request, *args, **kwargs):
        project_pk = self.kwargs['project_pk']
        form = self.form_class(request.POST)
        pbi_pk = self.kwargs['pbi_pk']
        pbi = PBI.objects.get(pk=pbi_pk)
        if form.is_valid():
            task = form.save(commit=False)
            task.status = "Ready"
            task.pbi = pbi
            task.save()
            return HttpResponseRedirect('/project/' + str(project_pk) + '/sprintBacklog')

        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        project_pk = self.kwargs['project_pk']
        project = Project.objects.get(pk=project_pk)
        pbi_pk = self.kwargs['pbi_pk']
        pbi = PBI.objects.get(pk=pbi_pk)

        context = super().get_context_data(**kwargs)
        context['project'] = project
        context['pbi'] = pbi
        context['form'] = TaskAddForm()
        return context


class TaskDelete(DeleteView):
    model = Task
    template_name = "task_delete.html"

    def get_success_url(self):
        project = self.kwargs['project_pk']
        return reverse_lazy("sprint_backlog_main", kwargs={'project_pk': project})

    def get_context_data(self, **kwargs):
        pbi_pk = self.kwargs['pbi_pk']
        project_pk = self.kwargs['project_pk']
        task_pk = self.kwargs['pk']

        context = super().get_context_data(**kwargs)
        context['task'] = Task.objects.get(pk=task_pk)
        context['pbi'] = PBI.objects.get(pk=pbi_pk)
        context['project'] = Project.objects.get(pk=project_pk)
        return context
