from django.conf.urls import url
from . import views
# from django.contrib.auth.views import password_change

urlpatterns = [
    # url(r'^login/', views.user_login, {'template_name': 'login.html'}, name='user_login'),
    # url(r'^accounts/profile/', password_change, name='password_change'),
    url(r'^login/', views.login, name='login'),
    url(r'^accounts/login/', views.login, name='login'),
    url(r'signup/', views.signup, name='signup'),
    url(r'logout/', views.logout, name='logout'),
    url(r'question/(?P<qid>\d+)/', views.question_detail, name='question_details'),
    url(r'ask/', views.add_question, name='add_question'),
    url(r'popular/', views.popular_questions, name='popular_questions'),
    url(r'new/', views.new_questions, name='new_questions')
]
