from django.urls import path, re_path
from .views import IndexTemplateView, get_pharmacy

app_name = 'dashboard'
urlpatterns = [
    path('pharmacy/',  get_pharmacy, name='pharmacy'),
    re_path(r"^.*", IndexTemplateView.as_view(), name="index"),
    ]