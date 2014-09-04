from django.conf.urls import *

from validate import views

urlpatterns= patterns('',
   url(
        regex=r'^(?P<schema_name>[a-z0-9]+)/(?P<document_id>[A-z0-9\/\-]+)/$',
        view= views.ValidatorView.as_view(),
        name='validate'
   ),
   url(
        regex=r'^(?P<schema_name>[a-z0-9]+)/$',
        view= views.ValidatorPostView.as_view(),
        name='validate'
   )
)

