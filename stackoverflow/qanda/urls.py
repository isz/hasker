from django.urls import path, re_path

from . import views

app_name = 'qanda'
urlpatterns = [
    path(r'ask/', views.AskQuestionView.as_view(), name='ask_question'),
    path(r'<int:pk>/page-<int:page>/', views.QuestionDetail.as_view(), name='question_page'),
    re_path(r'^(?P<pk>\d+)/(?P<action>like|dislike|cancel)/$', views.VoteQuestionView.as_view(), name='vote_question'),
    path(r'<int:pk>/correct/<int:answ_id>', views.CorrectAnswerView.as_view(), name='correct_answer'),
    path(r'<int:pk>/', views.QuestionDetail.as_view(), name='question'),
    

    re_path(r'^answer/(?P<pk>\d+)/(?P<action>like|dislike|cancel)/$', views.VoteAnswerView.as_view(), name='vote_answer'),
    path(r'answer/', views.CreateAnswerView.as_view(), name='answer'),

    path(r'', views.QuestionListView.as_view(), name='questions_list'),
]