from django.conf.urls import *

from schema import views

urlpatterns= patterns('',
   url(
        regex=r'^(?P<schema_name>[A-z0-9\/]+)/$',
        view= views.SchemaView.as_view(),
        name='schema'
   )
)

