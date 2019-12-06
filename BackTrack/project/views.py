from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.views.generic import TemplateView, FormView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from .models import *
from .forms import *


# Create your views here.
class ProjectMain(TemplateView):
    template_name = "project_main.html"

    def get_context_data(self, **kwargs):
        request = self.request
        user = request.user
        if user.is_authenticated:
            if user.is_superuser:
                group = 'Super User'
                project_list = Project.objects.all()
            elif user.groups.filter(name='Owners').count():
                group = 'Owner'
                project_list = Project.objects.filter(owner__pk=user.pk)
            elif user.groups.filter(name='Managers').count():
                group = 'Manager'
                project_list = Project.objects.filter(manager__pk=user.pk)
            else:
                group = 'Developer'
                if user.project is not None:
                    project_list = [user.project]
                else:
                    project_list = None
        else:
            project_list = None
            group = None

        context = super().get_context_data(**kwargs)
        context['project_list'] = project_list
        context['group'] = group
        return context


class ProjectDetail(TemplateView):
    template_name = "project_detail.html"

    def get_context_data(self, **kwargs):
        project_pk = self.kwargs['project_pk']
        project = Project.objects.get(pk=project_pk)
        request = self.request
        user = request.user
        if user.is_authenticated:
            if user.is_superuser:
                group = 'Super User'
            elif user.groups.filter(name='Owners').count():
                group = 'Owner'
            elif user.groups.filter(name='Managers').count():
                group = 'Manager'
            else:
                group = 'Developer'
        else:
            group = None

        context = super().get_context_data(**kwargs)
        context['project'] = project
        context['group'] = group
        return context

class ProjectFinish(DeleteView):
    model = Project
    template_name = "project_finish.html"

    def get_success_url(self):
        request = self.request
        user = request.user
        owner_group = Group.objects.get(name='Owners')
        owner_group.user_set.remove(user)
        developer_group = Group.objects.get(name='Developers')
        developer_group.user_set.add(user)
        return '/project'

    def get_context_data(self, **kwargs):
        project_pk = self.kwargs['pk']

        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=project_pk)
        return context

class ProjectCreate(FormView):
    template_name = "project_creation.html"
    form_class = ProjectCreateForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            user = request.user
            project.owner = user
            project.save()
            owner_group = Group.objects.get(name='Owners')
            owner_group.user_set.add(user)
            developer_group = Group.objects.get(name='Developers')
            developer_group.user_set.remove(user)
            return HttpResponseRedirect('/project')

        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['form'] = ProjectCreateForm()
        return context