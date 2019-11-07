from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, FormView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import *
from project.models import Project
from .forms import *


# Create your views here.
class ProductBacklogMain(TemplateView):
    template_name = "productbacklog_main.html"

    def get_context_data(self, **kwargs):
        project = self.kwargs['project_pk']
        productBacklog = ProductBacklog.objects.get(project__pk=project)

        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=project)
        context['pbi_list'] = PBI.objects.filter(productBacklog__pk=productBacklog.pk).order_by('priority')
        remaining_estimated = 0
        finished_estimated = 0
        for pbi in context['pbi_list']:
            if pbi.status != "Finished":
                remaining_estimated += pbi.estimated
                pbi.cumulative = remaining_estimated
            else:
                finished_estimated += pbi.estimated
                pbi.cumulative = finished_estimated
        total_estimated = remaining_estimated + finished_estimated
        context['total_estimated'] = total_estimated
        context['finished_estimated'] = finished_estimated
        context['remaining_estimated'] = remaining_estimated
        return context


class PBIMain(TemplateView):
    template_name = "pbi_main.html"

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


class PBIAdd(FormView):
    template_name = "pbi_add.html"
    form_class = PBIAddForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        project = self.kwargs['project_pk']
        productBacklog = ProductBacklog.objects.get(project__pk=project)
        if form.is_valid():
            pbi = form.save(commit=False)
            pbi.status = "Ready"
            pbi.productBacklog = productBacklog
            pbi.save()
            return HttpResponseRedirect('/project/' + str(project) + '/productBacklog')

        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        project = self.kwargs['project_pk']

        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=project)
        context['form'] = PBIAddForm()
        return context


class PBIDelete(DeleteView):
    model = PBI
    template_name = "pbi_delete.html"

    def get_success_url(self):
        project = self.kwargs['project_pk']
        return reverse_lazy("product_backlog_main", kwargs={'project_pk': project})

    def get_context_data(self, **kwargs):
        pbi = self.kwargs['pk']
        project = self.kwargs['project_pk']

        context = super().get_context_data(**kwargs)
        context['pbi_main'] = '/project/' + str(project) + '/productBacklog/pbi/' + str(pbi)
        context['pbi'] = PBI.objects.get(pk=pbi)
        context['project'] = Project.objects.get(pk=project)
        return context


def pbi_modify(request, project_pk, pbi_pk):
    pbi = get_object_or_404(PBI, pk=pbi_pk)
    project = Project.objects.get(pk=project_pk)
    pbi_main = '/project/' + str(project_pk) + '/productBacklog/pbi/' + str(pbi_pk)
    if request.method == "POST":
        form = PBIModifyForm(request.POST, instance=pbi)
        if form.is_valid():
            pbi = form.save(commit=False)
            pbi.save()
            return redirect('/project/' + str(project_pk) + '/productBacklog/pbi/' + str(pbi_pk), pk=pbi.pk)
    else:
        form = PBIModifyForm(instance=pbi)
    return render(request, 'pbi_modify.html', {'form': form, 'project': project, 'pbi': pbi, 'pbi_main': pbi_main})
