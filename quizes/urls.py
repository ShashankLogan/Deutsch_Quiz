from django.urls import path
from django.conf.urls import url
from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view,
    quiz_main,
    ViewQuizListByCategory
)

app_name = 'quizes'

urlpatterns = [
    #path('',QuizListView.as_view(),name='main-view'),
    path('',quiz_main,name='main-view'),
    path('<pk>/',quiz_view,name = 'quiz-view'),
    path('<pk>/data',quiz_data_view,name = 'quiz-data-view'),
    path('<pk>/save/',save_quiz_view,name='save-view'),
    url(regex=r'/(?P<category_name>[\w|\W-]+)/$',
                            view=ViewQuizListByCategory,
                            name='quiz_category_list_matching'),
    url(regex=r'/(?P<category_name>[\w|\W-]+)/(?P<quiz_name>[\w|\W-]+)/<pk>',
                            view=quiz_view,
                            name='quiz-view-category'),

]
