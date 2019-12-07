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
from productBacklog.models import ProductBacklog


# Create your views here.
def sendDeveloperEmail(request, project_pk, developer_pk):
    user = request.user
    user_name = user.username
    project = Project.objects.get(pk=project_pk)
    project_name = project.name
    developer = BackTrackUser.objects.get(pk=developer_pk)
    link = 'http://127.0.0.1:8000/project/' + str(project_pk) + '/developer/' + str(developer_pk)
    message = 'Hi, ' + user_name + ' sends you an invitation to join project ' + project_name + '. Open the following ' \
                                                                                                'link with your ' \
                                                                                                'account to join: ' + \
              link
    send_mail('BackTrack: Project Invitation', message, 'hku_tql@163.com',
              [developer.email], fail_silently=False)
    return HttpResponseRedirect(
        '/project/' + str(project_pk) + '/developer/invite')


def sendManagerEmail(request, project_pk, manager_pk):
    user = request.user
    user_name = user.username
    project = Project.objects.get(pk=project_pk)
    project_name = project.name
    manager = BackTrackUser.objects.get(pk=manager_pk)
    link = 'http://127.0.0.1:8000/project/' + str(project_pk) + '/manager/' + str(manager_pk)
    message = 'Hi, ' + user_name + ' sends you an invitation to join project ' + project_name + '. Open the following ' \
                                                                                                'link with your ' \
                                                                                                'account to join: ' + \
              link
    send_mail('BackTrack: Project Invitation', message, 'hku_tql@163.com',
              [manager.email], fail_silently=False)
    return HttpResponseRedirect('/project/' + str(project_pk) + '/manager/invite')


def developerJoin(request, project_pk, developer_pk):
    user = BackTrackUser.objects.get(pk=developer_pk)
    project = Project.objects.get(pk=project_pk)
    user.project = project
    user.save()
    return HttpResponseRedirect('/project')


def managerJoin(request, project_pk, manager_pk):
    user = BackTrackUser.objects.get(pk=manager_pk)
    project = Project.objects.get(pk=project_pk)
    project.manager = user
    project.save()
    return HttpResponseRedirect('/project')


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
            productBacklog = ProductBacklog(project=project)
            productBacklog.save()
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


class ManagerInvite(TemplateView):
    template_name = "project_manager_invite.html"

    def get_context_data(self, **kwargs):
        request = self.request
        user = request.user
        project_pk = self.kwargs['project_pk']
        project = Project.objects.get(pk=project_pk)
        manager_list = BackTrackUser.objects.filter(groups__name='Managers')
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
        context['manager_list'] = manager_list
        context['group'] = group
        return context


class DeveloperInvite(TemplateView):
    template_name = "project_developer_invite.html"

    def get_context_data(self, **kwargs):
        request = self.request
        user = request.user
        project_pk = self.kwargs['project_pk']
        project = Project.objects.get(pk=project_pk)
        developer_list = BackTrackUser.objects.filter(groups__name='Developers', project=None)
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
        context['developer_list'] = developer_list
        context['group'] = group
        return context


class DeveloperJoinConfirm(TemplateView):
    template_name = "project_developer_join.html"

    def get_context_data(self, **kwargs):
        request = self.request
        user = request.user
        project_pk = self.kwargs['project_pk']
        developer_pk = self.kwargs['developer_pk']
        is_self = False
        if developer_pk == user.pk:
            is_self = True
        is_not_involved = False
        if user.project is None:
            is_not_involved = True
        is_exist = False
        project = None
        if Project.objects.filter(pk=project_pk).count():
            project = Project.objects.get(pk=project_pk)
            is_exist = True
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
        context['is_exist'] = is_exist
        context['is_self'] = is_self
        context['is_not_involved'] = is_not_involved
        context['group'] = group
        return context


class ManagerJoinConfirm(TemplateView):
    template_name = "project_manager_join.html"

    def get_context_data(self, **kwargs):
        request = self.request
        user = request.user
        project_pk = self.kwargs['project_pk']
        developer_pk = self.kwargs['manager_pk']
        is_self = False
        if developer_pk == user.pk:
            is_self = True
        is_exist = False
        project = None
        is_available = False
        if Project.objects.filter(pk=project_pk).count():
            project = Project.objects.get(pk=project_pk)
            is_exist = True
            if project.manager is None:
                is_available = True
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
        context['is_exist'] = is_exist
        context['is_self'] = is_self
        context['is_available'] = is_available
        context['group'] = group
        return context
