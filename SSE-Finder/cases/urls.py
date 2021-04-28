from django.urls import include, path
from cases import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index_detail, name="index"),
    path("case", views.case_detail, name="case"),
    path('event/<int:case_number>', views.event_detail, name="event"),
    path('confirm', views.confirm_detail, name="confirm"),
    path('ssefinder', views.show_sse, name="sse_finder"),
    path('ssefinder/<int:event_pk>', views.view_sse, name="view_sse"),
    
    path("login", auth_views.LoginView.as_view(), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
]
