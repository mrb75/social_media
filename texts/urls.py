from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
urlpatterns = [
    path("received/list/<int:pk>/", ReceivedTextsView.as_view(), name=""),
    path("sent/list/<int:pk>/", SentTextsView.as_view(), name=""),
    path("send/<int:pk>/", SendTextView.as_view(), name=""),
    path("edit/<int:pk>/", EditTextView.as_view(), name=""),
    path("remove/<int:pk>/", RemoveTextView.as_view(), name=""),
]

urlpatterns += router.urls
