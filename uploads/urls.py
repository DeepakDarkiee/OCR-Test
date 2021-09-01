from core import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path("home/", views.SimpleUpload.as_view(), name="home"),
    path("document/", views.DocumentView.as_view(), name="document"),
    path("search/", views.SearchResultsView.as_view(), name="search"),
    path("admin/", admin.site.urls),
    path("", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
