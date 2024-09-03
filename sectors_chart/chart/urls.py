from . import views
from django.urls import include, path

urlpatterns = [
    path("", views.index, name="index"),
    path("page-one/", views.plot_page_view, name="page_one"),
    path("plot-one/", views.chart_two, name="chart_one"),
    path('plot-two/', views.plot_view, name='chart_two'),
    path("page-two/", views.plot_two_page_view, name="page_two"),
]