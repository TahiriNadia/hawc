import json
from typing import Dict

from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView

from ..assessment.models import Assessment
from ..common.helper import HAWCDjangoJSONEncoder
from ..common.views import (
    BaseCreate,
    BaseDelete,
    BaseDetail,
    BaseList,
    BaseUpdate,
    TeamMemberOrHigherMixin,
)
from ..riskofbias.models import RiskOfBiasMetric
from . import forms, models, serializers


# SUMMARY-TEXT
class SummaryTextJSON(BaseDetail):
    model = models.SummaryText

    def dispatch(self, *args, **kwargs):
        self.assessment = get_object_or_404(Assessment, pk=kwargs.get("pk"))
        self.permission_check_user_can_view()
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        content = self.model.get_assessment_descendants(self.assessment.id, json_encode=True)
        return HttpResponse(content, content_type="application/json")


class SummaryTextList(BaseList):
    parent_model = Assessment
    model = models.SummaryText

    def get_queryset(self):
        rt = self.model.get_assessment_root_node(self.assessment.id)
        return self.model.objects.filter(pk__in=[rt.pk])


def validSummaryTextChange(assessment_id):
    response = {
        "status": "ok",
        "content": models.SummaryText.get_assessment_descendants(assessment_id, json_encode=False),
    }
    return HttpResponse(
        json.dumps(response, cls=HAWCDjangoJSONEncoder), content_type="application/json"
    )


class SummaryTextCreate(BaseCreate):
    # Base view for all Create, Update, Delete GET operations
    parent_model = Assessment
    parent_template_name = "assessment"
    model = models.SummaryText
    form_class = forms.SummaryTextForm

    def post(self, request, *args, **kwargs):
        if not request.is_ajax() or not request.user.is_authenticated:
            raise HttpResponseNotAllowed()
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        return HttpResponse(json.dumps(form.errors))

    def form_valid(self, form):
        self.object = self.model.create(form)
        return validSummaryTextChange(self.assessment.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["smart_tag_form"] = forms.SmartTagForm(assessment_id=self.assessment.id)
        return context


class SummaryTextUpdate(BaseUpdate):
    # AJAX POST-only
    model = models.SummaryText
    form_class = forms.SummaryTextForm
    success_message = None
    http_method_names = [
        "post",
    ]

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise HttpResponseNotAllowed()
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        return HttpResponse(json.dumps(form.errors))

    def form_valid(self, form):
        self.object = self.object.update(form)
        return validSummaryTextChange(self.assessment.id)


class SummaryTextDelete(BaseDelete):
    # AJAX POST-only
    model = models.SummaryText
    success_message = None
    http_method_names = [
        "post",
    ]

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise HttpResponseNotAllowed()
        return super().post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return validSummaryTextChange(self.assessment.id)


# VISUALIZATIONS
class VisualizationList(BaseList):
    parent_model = Assessment
    model = models.Visual

    def get_queryset(self):
        return self.model.objects.get_qs(self.assessment)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_published"] = self.assessment.user_is_part_of_team(self.request.user)
        return context


class VisualizationDetail(BaseDetail):
    model = models.Visual


class VisualizationCreateSelector(BaseDetail):
    model = Assessment
    template_name = "summary/visual_selector.html"


class VisualizationCreate(BaseCreate):
    success_message = "Visualization created."
    parent_model = Assessment
    parent_template_name = "assessment"
    model = models.Visual

    def get_form_class(self):
        visual_type = int(self.kwargs.get("visual_type"))
        try:
            return forms.get_visual_form(visual_type)
        except ValueError:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["visual_type"] = int(self.kwargs.get("visual_type"))
        return kwargs

    def get_template_names(self):
        visual_type = int(self.kwargs.get("visual_type"))
        if visual_type in {
            models.Visual.LITERATURE_TAGTREE,
            models.Visual.EXTERNAL_SITE,
        }:
            return "summary/visual_form_django.html"
        else:
            return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dose_units"] = models.Visual.get_dose_units()
        context["instance"] = {}
        context["visual_type"] = int(self.kwargs.get("visual_type"))
        context["smart_tag_form"] = forms.SmartTagForm(assessment_id=self.assessment.id)
        context["rob_metrics"] = json.dumps(
            list(RiskOfBiasMetric.objects.get_metrics_for_visuals(self.assessment.id))
        )
        context["initial_data"] = json.dumps(self.get_initial_visual(context))
        return context

    def get_initial_visual(self, context) -> Dict:
        instance = self.model()
        instance.id = 999999999999
        instance.assessment = self.assessment
        instance.visual_type = context["visual_type"]
        return serializers.VisualSerializer().to_representation(instance)


class VisualizationCreateTester(VisualizationCreate):
    parent_model = Assessment
    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        response = form.instance.get_editing_dataset(request)
        return HttpResponse(response, content_type="application/json")


class VisualizationUpdate(BaseUpdate):
    success_message = "Visualization updated."
    model = models.Visual

    def get_form_class(self):
        try:
            return forms.get_visual_form(self.object.visual_type)
        except ValueError:
            raise Http404

    def get_template_names(self):
        visual_type = self.object.visual_type
        if visual_type in {
            models.Visual.LITERATURE_TAGTREE,
            models.Visual.EXTERNAL_SITE,
        }:
            return "summary/visual_form_django.html"
        else:
            return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dose_units"] = models.Visual.get_dose_units()
        context["instance"] = self.object.get_json()
        context["visual_type"] = self.object.visual_type
        context["smart_tag_form"] = forms.SmartTagForm(assessment_id=self.assessment.id)
        context["rob_metrics"] = json.dumps(
            list(RiskOfBiasMetric.objects.get_metrics_for_visuals(self.assessment.id))
        )
        context["initial_data"] = json.dumps(
            serializers.VisualSerializer().to_representation(self.object)
        )
        return context


class VisualizationDelete(BaseDelete):
    success_message = "Visualization deleted."
    model = models.Visual

    def get_success_url(self):
        return reverse_lazy("summary:visualization_list", kwargs={"pk": self.assessment.pk})


# DATA-PIVOT
class DataPivotNewPrompt(TemplateView):
    """
    Select if you wish to upload a file or use a query.
    """

    model = models.DataPivot
    crud = "Read"
    template_name = "summary/datapivot_type_selector.html"

    def dispatch(self, *args, **kwargs):
        self.assessment = get_object_or_404(Assessment, pk=kwargs["pk"])
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assessment"] = self.assessment
        return context


class DataPivotNew(BaseCreate):
    # abstract view; extended below for actual use
    parent_model = Assessment
    parent_template_name = "assessment"
    success_message = "Data Pivot created."
    template_name = "summary/datapivot_form.html"

    def get_success_url(self):
        super().get_success_url()
        return self.object.get_visualization_update_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.GET.get("reset_row_overrides"):
            kwargs["initial"]["settings"] = models.DataPivot.reset_row_overrides(
                kwargs["initial"]["settings"]
            )
        return kwargs


class DataPivotQueryNew(DataPivotNew):
    model = models.DataPivotQuery
    form_class = forms.DataPivotQueryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["file_loader"] = False
        context["smart_tag_form"] = forms.SmartTagForm(assessment_id=self.assessment.id)
        return context


class DataPivotFileNew(DataPivotNew):
    model = models.DataPivotUpload
    form_class = forms.DataPivotUploadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["file_loader"] = True
        context["smart_tag_form"] = forms.SmartTagForm(assessment_id=self.assessment.id)
        return context


class DataPivotCopyAsNewSelector(TeamMemberOrHigherMixin, FormView):
    # Select an existing assessed outcome as a template for a new one
    model = Assessment
    template_name = "summary/datapivot_copy_selector.html"
    form_class = forms.DataPivotSelectorForm

    def get_assessment(self, request, *args, **kwargs):
        return get_object_or_404(Assessment, pk=self.kwargs.get("pk"))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["cancel_url"] = reverse("summary:visualization_list", args=(self.assessment.id,))
        return kwargs

    def form_valid(self, form):
        dp = form.cleaned_data["dp"]

        if hasattr(dp, "datapivotupload"):
            url = reverse_lazy("summary:dp_new-file", kwargs={"pk": self.assessment.id})
        else:
            url = reverse_lazy("summary:dp_new-query", kwargs={"pk": self.assessment.id})

        url += f"?initial={dp.pk}"

        if form.cleaned_data["reset_row_overrides"]:
            url += "&reset_row_overrides=1"

        return HttpResponseRedirect(url)


class GetDataPivotObjectMixin:
    def get_object(self):
        slug = self.kwargs.get("slug")
        assessment = self.kwargs.get("pk")
        obj = get_object_or_404(models.DataPivot, assessment=assessment, slug=slug)
        if hasattr(obj, "datapivotquery"):
            obj = obj.datapivotquery
        else:
            obj = obj.datapivotupload
        return super().get_object(object=obj)


class DataPivotByIdDetail(RedirectView):
    """
    Redirect to standard data pivot page; useful for developers referencing by database id.
    """

    def get_redirect_url(*args, **kwargs):
        return get_object_or_404(models.DataPivot, id=kwargs.get("pk")).get_absolute_url()


class DataPivotDetail(GetDataPivotObjectMixin, BaseDetail):
    model = models.DataPivot
    template_name = "summary/datapivot_detail.html"


class DataPivotUpdateSettings(GetDataPivotObjectMixin, BaseUpdate):
    success_message = "Data Pivot updated."
    model = models.DataPivot
    form_class = forms.DataPivotSettingsForm
    template_name = "summary/datapivot_update_settings.html"


class DataPivotUpdateQuery(GetDataPivotObjectMixin, BaseUpdate):
    success_message = "Data Pivot updated."
    model = models.DataPivotQuery
    form_class = forms.DataPivotQueryForm
    template_name = "summary/datapivot_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["file_loader"] = False
        context["smart_tag_form"] = forms.SmartTagForm(assessment_id=self.assessment.id)
        return context


class DataPivotUpdateFile(GetDataPivotObjectMixin, BaseUpdate):
    success_message = "Data Pivot updated."
    model = models.DataPivotUpload
    form_class = forms.DataPivotUploadForm
    template_name = "summary/datapivot_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["file_loader"] = True
        context["smart_tag_form"] = forms.SmartTagForm(assessment_id=self.assessment.id)
        return context


class DataPivotDelete(GetDataPivotObjectMixin, BaseDelete):
    success_message = "Data Pivot deleted."
    model = models.DataPivot
    template_name = "summary/datapivot_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("summary:visualization_list", kwargs={"pk": self.assessment.pk})
