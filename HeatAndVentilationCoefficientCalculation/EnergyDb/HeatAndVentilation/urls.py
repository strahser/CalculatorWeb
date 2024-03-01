from django.urls import path
from . import views
app_name = "HeatAndVentilation"
urlpatterns = [
    path('api/result_data/<int:pk>/', views.BuildingListView.as_view(), name='result_data'),
    path("building_create/", views.BuildingCreateView.as_view(), name="building_create"),
    path("building_update/<int:pk>/", views.BuildingUpdateView.as_view(), name="building_update"),
    path('check_thermal_resistence/', views.check_thermal_resistence, name='check_thermal_resistence'),
    path('StructureListView/<int:pk>/', views.StructureListView.as_view(), name="StructureListView"),
    path("StructureUpdateView/<int:pk>/", views.StructureUpdateView.as_view(), name="StructureUpdateView"),
    path("StructureDeleteView/<int:pk>/", views.StructureDeleteView.as_view(), name="StructureDeleteView"),
    path("StructureCopyView/<int:pk>/", views.StructureCopyView, name="StructureCopyView"),
    path("StructureLayerUpdateView/<int:pk>/", views.StructureLayerUpdateView.as_view(), name="StructureLayerUpdateView"),
    path("StructureLayerDeleteView/<int:pk>/", views.StructureLayerDeleteView.as_view(), name="StructureLayerDeleteView"),
    path("StructureLayerCreateView/<int:base_pk>/", views.StructureLayerCreateView, name="StructureLayerCreateView"),
    path("StructureLayerCopyView/<int:pk>/", views.StructureLayerCopyView, name="StructureLayerCopyView"),
]