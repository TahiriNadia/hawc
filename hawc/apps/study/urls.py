from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import api, views

router = DefaultRouter()
router.register(r"study", api.Study, basename="study")
router.register(r"study-cleanup", api.StudyCleanupFieldsView, basename="study-cleanup")

app_name = "study"
urlpatterns = [
    url(r"^api/", include((router.urls, "api"))),
    # study
    url(r"^assessment/(?P<pk>\d+)/$", views.StudyList.as_view(), name="list"),
    url(r"^(?P<pk>\d+)/add-details/$", views.StudyCreateFromReference.as_view(), name="new_study",),
    url(
        r"^assessment/(?P<pk>\d+)/new-study/$",
        views.ReferenceStudyCreate.as_view(),
        name="new_ref",
    ),
    url(
        r"^assessment/(?P<pk>\d+)/copy-studies/$", views.StudiesCopy.as_view(), name="studies_copy",
    ),
    url(r"^(?P<pk>\d+)/$", views.StudyRead.as_view(), name="detail"),
    url(r"^(?P<pk>\d+)/edit/$", views.StudyUpdate.as_view(), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", views.StudyDelete.as_view(), name="delete"),
    url(r"^(?P<pk>\d+)/risk-of-bias/$", views.StudyRoBRedirect.as_view(), name="rob_redirect",),
    # attachment
    url(r"^attachment/(?P<pk>\d+)/$", views.AttachmentRead.as_view(), name="attachment_detail",),
    url(
        r"^(?P<pk>\d+)/attachment/add/$",
        views.AttachmentCreate.as_view(),
        name="attachment_create",
    ),
    url(
        r"^attachment/(?P<pk>\d+)/delete/$",
        views.AttachmentDelete.as_view(),
        name="attachment_delete",
    ),
    url(
        r"^(?P<pk>\d+)/editability-update/(?P<updated_value>.*)/$",
        views.EditabilityUpdate.as_view(),
        name="editability_update",
    ),
]
