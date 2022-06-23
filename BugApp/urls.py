
from django.urls import path
from . import views
app_name = 'BugApp'

urlpatterns = [
    path('', views.home, name='home'),
    path('tags', views.tags, name='tags'),
    path('addcomment', views.addComment, name='addcomment'),
    path('delete/<int:id>/<int:pk>', views.commentDelete, name='delete'),
    path('deleteans/<int:id>/<int:pk>',
         views.answercommentDelete, name='answercommentDelete'),
    path('tags/<str:search>', views.taggedSearch, name='tagssearch'),
    path('newQuestion', views.askQuestion, name='askQuestion'),
    path('question/<int:id>', views.single_question, name='single_question'),
    path('question/delete/<int:id>', views.question_delete, name='question_delete'),
    path('edit/<int:id>', views.editQuestion, name='editQuestion'),
    path('search', views.Search, name='searchQuestion'),

]
