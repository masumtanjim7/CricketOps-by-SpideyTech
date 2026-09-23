from django.urls import path
from .views import CommitDeliveryView

urlpatterns = [
    path('matches/<uuid:match_id>/deliveries/', CommitDeliveryView.as_asgi() if hasattr(CommitDeliveryView, 'as_asgi') else CommitDeliveryView.as_view(), name='commit-delivery'),
]