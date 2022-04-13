from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("quotes/", views.quotes_index, name="quotes_index"),
    path("quotes/<int:quote_id>/", views.quote_details, name="quote_details"),
    path("quotes/create/", views.QuoteCreate.as_view(), name="quotes_create"),
    path("quotes/<int:pk>/update/", views.QuoteUpdate.as_view(), name="quote_update"),
    path("quotes/<int:pk>/delete/", views.QuoteDelete.as_view(), name="quote_delete"),
    path(
        "quotes/<int:quote_id>/add_quote_review/",
        views.add_quote_review,
        name="add_quote_review",
    ),
    path(
        "quotes/<int:quote_id>/delete_quote_review/<int:review_id>/",
        views.delete_quote_review,
        name="delete_quote_review",
    ),
    path(
        "quotes/<int:quote_id>/assoc_source/<int:source_id>/",
        views.assoc_source,
        name="assoc_source",
    ),
    path(
        "quotes/<int:quote_id>/unassoc_source/<int:source_id>/",
        views.unassoc_source,
        name="unassoc_source",
    ),
    path("quotes/personal/", views.quotes_personal, name="quotes_personal"),
    path("sources/", views.sources_index, name="sources_index"),
    path("sources/<int:source_id>/", views.source_details, name="source_details"),
    path("sources/create/", views.SourceCreate.as_view(), name="source_create"),
    path(
        "sources/<int:pk>/update/", views.SourceUpdate.as_view(), name="source_update"
    ),
    path(
        "sources/<int:pk>/delete/", views.SourceDelete.as_view(), name="source_delete"
    ),
    path("quotes/personal/", views.quotes_personal, name="quotes_personal"),
    path("accounts/signup/", views.signup, name="signup"),
]
