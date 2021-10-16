from django.urls import path

from estimate.views import CreateEstimateView, UpdateEstimateView, EstimateDetailView, EstimateListView

urlpatterns = [
    path('estimate/new/', CreateEstimateView.as_view(), name='create-estimate'),
    path('estimate/<int:pk>/edit', UpdateEstimateView.as_view(), name='update-estimate'),
    path('estimate/<int:pk>/', EstimateDetailView.as_view(), name='estimate'),
    path('estimates/', EstimateListView.as_view(), name='estimate-list'),
]
