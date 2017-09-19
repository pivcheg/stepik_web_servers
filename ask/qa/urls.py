from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'login/', views.login, name='login'),
    url(r'signup/', views.signup, name='signup'),
    url(r'question/(?P<qid>\d+)/', views.question_detail, name='question_details'),
    # url(r'all_posts/', views.questions_list_on_page, name='all_posts'),
    url(r'ask/', views.add_question, name='add_question'),
    url(r'popular/', views.popular_questions, name='popular_questions'),
    url(r'new/', views.new_questions, name='new_questions')
]
