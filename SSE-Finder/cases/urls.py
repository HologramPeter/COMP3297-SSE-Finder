from django.urls import path
from cases import views

urlpatterns = [
    path("", views.index_detail, name="index"),
    path("case", views.case_detail, name="case"),
    path('event/<int:case_number>', views.event_detail, name="event"),
    path('confirm', views.confirm_detail, name="confirm"),
    path('ssefinder', views.show_sse, name="sse_finder")
]
