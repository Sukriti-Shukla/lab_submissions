# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('download/', views.download, name='download'),
    path('analyze/', views.analyze, name='analyze'),
    path('my_submissions/', views.my_submissions, name='my_submissions'),
    path('update_experiment/<int:experiment_id>/', views.update_experiment, name='update_experiment'),
    path('delete_experiment/<int:experiment_id>/', views.delete_experiment, name='delete_experiment'),
    path('input_experiment/', views.input_experiment, name='input_experiment'),
    path('upload_template/', views.upload_template, name='upload_template'),
    path('get_experiment_data/<int:experiment_id>/', views.get_experiment_data, name='get_experiment_data'),
    path('analyze_experiment/<int:experiment_id>/', views.analyze_experiment, name='analyze_experiment'),
    path('analysis_test/', views.analysis_test, name='analysis_test'),
    path('analysis_test/<int:experiment_id>/', views.analyze_view, name='analyze_view'),
    path('test_dash', views.test_dash, name='test_dash'),
]
