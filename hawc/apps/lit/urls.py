from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import api, views

router = DefaultRouter()
router.register(r"assessment", api.LiteratureAssessmentViewset, basename="assessment")
router.register(r"reference", api.ReferenceViewset, basename="reference")
router.register(r"search", api.SearchViewset, basename="search")
router.register(r"tags", api.ReferenceFilterTagViewset, basename="tags")
router.register(r"reference-cleanup", api.ReferenceCleanupViewset, basename="reference-cleanup")

app_name = "lit"
urlpatterns = [
    # overview
    url(r"^assessment/(?P<pk>\d+)/$", views.LitOverview.as_view(), name="overview"),
    # CRUD tags
    url(r"^assessment/tags/json/$", views.TagsJSON.as_view(), name="tags_list"),
    url(r"^assessment/(?P<pk>\d+)/tags/update/$", views.TagsUpdate.as_view(), name="tags_update",),
    url(r"^assessment/(?P<pk>\d+)/tags/update/copy/$", views.TagsCopy.as_view(), name="tags_copy",),
    url(
        r"^assessment/(?P<pk>\d+)/update/$",
        views.LiteratureAssessmentUpdate.as_view(),
        name="literature_assessment_update",
    ),
    # Reference-level details
    url(r"^reference/(?P<pk>\d+)/$", views.RefDetail.as_view(), name="ref_detail"),
    url(r"^reference/(?P<pk>\d+)/edit/$", views.RefEdit.as_view(), name="ref_edit"),
    url(r"^reference/(?P<pk>\d+)/delete/$", views.RefDelete.as_view(), name="ref_delete"),
    url(
        r"^reference/(?P<pk>\d+)/tag/$", views.TagByReference.as_view(), name="reference_tags_edit",
    ),
    url(r"^tag/(?P<pk>\d+)/tag/$", views.TagByTag.as_view(), name="references_tags_edit"),
    url(
        r"^assessment/(?P<pk>\d+)/tag/untagged/$",
        views.TagByUntagged.as_view(),
        name="tag_untagged",
    ),
    url(r"^assessment/(?P<pk>\d+)/references/$", views.RefList.as_view(), name="ref_list",),
    url(
        r"^assessment/(?P<pk>\d+)/references/extraction-ready/$",
        views.RefListExtract.as_view(),
        name="ref_list_extract",
    ),
    url(
        r"^assessment/(?P<pk>\d+)/references/visualization/$",
        views.RefVisualization.as_view(),
        name="ref_visual",
    ),
    url(
        r"^assessment/(?P<pk>\d+)/references/topic-model/$",
        views.RefTopicModel.as_view(),
        name="topic_model",
    ),
    url(
        r"^assessment/(?P<pk>\d+)/references/search/$",
        views.RefSearch.as_view(),
        name="ref_search",
    ),
    url(
        r"^assessment/(?P<pk>\d+)/references/(?P<tag_id>(\d+|untagged))/json/$",
        views.RefsByTagJSON.as_view(),
        name="refs_json",
    ),
    url(
        r"^assessment/(?P<pk>\d+)/references/upload/$",
        views.RefUploadExcel.as_view(),
        name="ref_upload",
    ),
    # CRUD searches
    url(r"^assessment/(?P<pk>\d+)/searches/$", views.SearchList.as_view(), name="search_list",),
    url(r"^assessment/(?P<pk>\d+)/search/new/$", views.SearchNew.as_view(), name="search_new",),
    url(
        r"^assessment/(?P<pk>\d+)/search/copy/$",
        views.SearchCopyAsNewSelector.as_view(),
        name="copy_search",
    ),
    url(
        r"^assessment/(?P<pk>\d+)/search/(?P<slug>[\w-]+)/$",
        views.SearchDetail.as_view(),
        name="search_detail",
    ),
    url(
        r"^assessment/(?P<pk>\d+)/search/(?P<slug>[\w-]+)/update/$",
        views.SearchUpdate.as_view(),
        name="search_update",
    ),
    url(
        r"^assessment/(?P<pk>\d+)/search/(?P<slug>[\w-]+)/delete/$",
        views.SearchDelete.as_view(),
        name="search_delete",
    ),
    url(
        r"^assessment/(?P<pk>\d+)/search/(?P<slug>[\w-]+)/query/$",
        views.SearchQuery.as_view(),
        name="search_query",
    ),
    # CRUD import
    url(r"^assessment/(?P<pk>\d+)/import/new/$", views.ImportNew.as_view(), name="import_new",),
    url(
        r"^assessment/(?P<pk>\d+)/ris-import/new/$",
        views.ImportRISNew.as_view(),
        name="import_ris_new",
    ),
    # Edit tags
    url(
        r"^assessment/(?P<pk>\d+)/search/(?P<slug>[\w-]+)/tag/$",
        views.TagBySearch.as_view(),
        name="search_tags_edit",
    ),
    url(
        r"^assessment/(?P<pk>\d+)/search/(?P<slug>[\w-]+)/tags/$",
        views.SearchRefList.as_view(),
        name="search_tags",
    ),
    url(
        r"^assessment/(?P<pk>\d+)/search/(?P<slug>[\w-]+)/tags-visuals/$",
        views.SearchTagsVisualization.as_view(),
        name="search_tags_visual",
    ),
    url(
        r"^ris-export-instructions/$",
        views.RISExportInstructions.as_view(),
        name="ris_export_instructions",
    ),
    url(r"^api/", include((router.urls, "api"))),
]
