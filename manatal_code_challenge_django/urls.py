from django.contrib import admin
from django.urls import path, include
from pages.models import School, Student
from rest_framework_nested import routers

from pages.views import SchoolViewSet, StudentViewSet, homePageView

def optional_trailing_slash(urls):
   for url in urls[0]:
       url.pattern._regex = url.pattern._regex.replace('/$', '/?$')
   return urls

# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'schools', SchoolViewSet)
router.register(r'students',StudentViewSet, basename='Student')

domains_router = routers.NestedSimpleRouter(router, r'schools', lookup='school')
domains_router.register(r'students', StudentViewSet, basename='Student')

urlpatterns = [
    path(r'', optional_trailing_slash(include(router.urls))),
    path(r'', optional_trailing_slash(include(domains_router.urls))),
    path(r'', homePageView)
]
