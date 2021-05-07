from django.urls import include, path, re_path
from cases import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login", auth_views.LoginView.as_view(), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),

    path("", views.index_view, name="index"),

    path('case', views.case_lookup_view, name="case"),
    path('case/<int:case_number>', views.case_view, name="view_case"),

    # handles get and post
    path("case/add", views.add_case_view, name="add_case_view"),
    path('case/<int:case_number>/add_event', views.add_event_view, name="add_event"),

    path("confirm", views.confirm_detail, name="confirm"),

    path('ssefinder/<int:event_pk>', views.sse_view, name="view_sse"),
    re_path('ssefinder', views.sse_lookup_view, name="sse_finder"),#must be in this order
]
