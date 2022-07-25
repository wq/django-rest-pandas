from django.urls import include, path
urlpatterns = [
    path('', include('tests.testapp.urls'))
]
