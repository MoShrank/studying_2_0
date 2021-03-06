from django.urls import path
from . import views
from studying_2_0_main.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'studying_2_0_main'

urlpatterns = [
path('', views.landing_page, name='landing_page'),
path('login/', views.login_user, name='login_user'),
path('contact/', views.contact, name='contact'),
path('about/', views.about, name='about'),
path('logout/', views.logout_user, name ='logout_user'),
path('home/', views.home, name='home'),
path('profile/', views.profile, name='profile'),
path('profile/edit', views.profile_edit, name='profile_edit'),
path('projects/', Projects.as_view()),
path('projects/new_project', NewProject.as_view()),
path('projects/<int:project_id>/edit', EditProject.as_view()),
path('projects/<slug:slug>-<int:project_id>/', ProjectDetail.as_view()),
path('projects/new_project/add_user', views.add_user, name='add_user'),

path('projects/<int:project_id>/elements/<int:element_id>', views.element_detail, name='element_detail'),
path('projects/<int:project_id>/<int:folder_id>', views.folder_detail, name='folder_detail'),

path('projects/<int:project_id>/elements/new_element/element', NewElement.as_view()),
path('projects/<int:project_id>/elements/new_element/folder', NewFolder.as_view()),

path('projects/<int:project_id>/edit/folder/<int:folder_id>', EditFolder.as_view()),
path('projects/<int:project_id>/edit/element/<int:element_id>', EditElement.as_view()),
path('projects/<int:project_id>/edit/delete', views.delete_element, name='delete_element'),

path('search', views.search, name='search'),
path('results/<str:tag>', views.results, name='results'),

]


if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
