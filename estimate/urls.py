from django.urls import path

from estimate.views import EstimateCreateView, EstimateDetailView, EstimateListView

urlpatterns = [
    path('', EstimateListView.as_view(), name='estimate-list'),
    path('estimates/new/', EstimateCreateView.as_view(), name='create-estimate'),
    path('estimates/<int:pk>/', EstimateDetailView.as_view(), name='estimate-detail'),
    path('estimates/update/<int:pk>/', EstimateDetailView.as_view(), name='update-estimate'),
]