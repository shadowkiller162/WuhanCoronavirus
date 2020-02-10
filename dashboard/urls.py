from django.urls import path, re_path
from .views import IndexTemplateView, get_pharmacy, get_google_location

app_name = 'dashboard'
urlpatterns = [
    path('pharmacy/',  get_pharmacy, name='pharmacy'),
    path('get_google_location/',  get_google_location, name='get_google_location'),
    re_path(r"^.*", IndexTemplateView.as_view(), name="index"),
    ]