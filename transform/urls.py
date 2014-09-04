from django.conf.urls import *

from transform import views

urlpatterns= patterns('',
   url(
        regex=r'^(?P<schema_name>[A-z0-9\/]+)/$',
        view= views.TransformView.as_view(),
        name='transform'
   )
)

