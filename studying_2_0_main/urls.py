from django.urls import path
from . import views

app_name = 'studying_2_0_main'

urlpatterns = [
path('', views.landing_page, name='landing_page'),
path('login/', views.login_user, name='login_user'),
path('contact/', views.contact, name='contact'),
path('about/', views.about, name='about'),
path('projects/', views.projects, name='projects'),
path('logout/', views.logout_user, name ='logout_user'),
path('home/', views.home, name='home'),
path('welcome/', views.welcome, name='welcome'),
path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
path('projects/new_project', views.new_project, name='new_project'),
path('projects/<int:project_id>/elements/<int:element_id>', views.element_detail, name='element_detail'),
path('projects/<int:project_id>/elements/new_element', views.new_element, name='new_element'),
]
