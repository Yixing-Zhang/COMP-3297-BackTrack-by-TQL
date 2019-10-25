from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *


# Create your views here.
class ProductBacklogMain(TemplateView):
    template_name = "productbacklog_main.html"

    def get_context_data(self, **kwargs):
        project = self.kwargs['project']
        productBacklog = ProductBacklog.objects.get(project__pk=project)

        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=project)
        context['pbi_list'] = PBI.objects.filter(productBacklog__pk=productBacklog.pk).order_by('priority')
        remaining_estimated = 0
        finished_estimated = 0
        for pbi in context['pbi_list']:
            if pbi.status != "Finished":
                remaining_estimated += pbi.estimated
            else:
                finished_estimated += pbi.estimated
        total_estimated = remaining_estimated + finished_estimated
        context['total_estimated'] = total_estimated
        context['finished_estimated'] = finished_estimated
        context['remaining_estimated'] = remaining_estimated
        return context


class PBIMain(TemplateView):
    template_name = "pbi_main.html"

    def get_context_data(self, **kwargs):
        project = self.kwargs['project']
        pbi = self.kwargs['pbi']

        context = super().get_context_data(**kwargs)
        context['pbi'] = PBI.objects.get(pk=pbi)
        return context


class PBIAdd(TemplateView):
    template_name = "pbi_add.html"

    def get_context_data(self, **kwargs):
        project = self.kwargs['project']

        context = super().get_context_data(**kwargs)
        return context


class PBIModify(TemplateView):
    template_name = "pbi_modify.html"

    def get_context_data(self, **kwargs):
        project = self.kwargs['project']
        pbi = self.kwargs['pbi']

        context = super().get_context_data(**kwargs)
        context['pbi'] = PBI.objects.get(pk=pbi)
        return context


class PBIDelete(TemplateView):
    template_name = "pbi_delete.html"

    def get_context_data(self, **kwargs):
        project = self.kwargs['project']
        pbi = self.kwargs['pbi']

        context = super().get_context_data(**kwargs)
        context['pbi'] = PBI.objects.get(pk=pbi)
        return context
