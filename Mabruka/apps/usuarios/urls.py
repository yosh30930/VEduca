from django.conf.urls import url
from .views import ResponsableListView

urlpatterns = [
    url(r'^responsables/$', ResponsableListView.as_view(), name='responsable-list'),
]
