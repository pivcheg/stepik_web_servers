from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'login/', views.login, name='login'),
    url(r'signup/', views.signup, name='signup'),
    url(r'question/(?P<qid>\d+)/', views.question_detail, name='question_details'),
    # url(r'all_posts/', views.questions_list_on_page, name='all_posts'),
    #url(r'', views.home, name='home'),
    url(r'ask/', views.ask, name='ask'),
    url(r'popular/', views.popular, name='popular'),
    url(r'new/', views.new, name='new')
]
