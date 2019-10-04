from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.client_main_page, name='client'),  # main client page
    path('profile', views.client_profile, name='client_profile'),
    path('edit', views.client_edit_main, name='client_edit'),
    path('edit/skills', views.client_edit_skills, name='client_edit_skills'),
    path('edit/photo', views.client_edit_photo, name='client_edit_photo'),
    path('edit/cv', views.client_edit_cv, name='client_edit_cv'),
    path('edit/education', views.client_edit_education, name='client_edit_education'),
    path('edit/experience', views.client_edit_experience, name='client_edit_experience'),
    path('chat', login_required(views.MessagesView.as_view()), name='contact_with_centre'),
    path(r'opinion/', opinion_list, name='opinion_list'),
    path(r'opinion/create/', OpinionCreate.as_view(), name='opinion_create'),
    path(r'opinion/<int:pk>/', opinion_detail, name='opinion_detail'),
    path(r'opinion/edit/<int:pk>/', answer_create, name='opinion_answer'),
    path(r'opinion/edit/<int:pk>/delete/', OpinionDelete.as_view(), name = 'opinion_delete'),
    path('login/', client_login),
    path('logout/', client_logout),
    path('tasks/', tasks, name = 'tasks_list'),
    path('edit/form_edu', views.form_education, name='form_edu'),
    ##Poland urls
    path('vacancies/', vacancies_list, name='vacancies_list'),
    path('resume_detail/vacancy/<str:slug>/', vacancy_detail, name='vacancy_detail_url'),
    path('resumes/', resumes_list, name='resume_list_url'),
    path('resume_detail/<str:slug>/', resume_detail, name='resume_detail_url'),
    path('resume_detail/<str:slug>/accepted_vacancies/', accepted_vacancies, name='accepted_vacancies_url'),
    path('resume_detail/<str:slug>/rejected_vacancies/', rejected_vacancies, name='rejected_vacancies_url'),
    path('accept_reject/', views.accept_reject),
    path('settings_on_off/', settings_on_off, name='settings_on_off_url'),
    path('on_off/', views.on_off),    # on_off settings for notifications
    path('viewed/', views.viewed),


]
