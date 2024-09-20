from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

#below are the URL to call the function in view file
#in the mainpage app URL goes like
#        .../    just a slash.

app_name = 'mainpage'

urlpatterns = [
    path("",views.landing_view,name="mainpage"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)