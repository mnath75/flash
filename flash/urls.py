from django.urls import path
from . import views

urlpatterns = [
    path('home',views.home,name="home"),
    path('',views.login_view,name="login_view"),
    path('logout',views.logout_view,name="logout_view"),
    path('flashcards',views.flashcard,name="flashcard"), 
    path('subject/<int:id>/',views.subject,name='filter_chapter'),   
    path('exam',views.exam,name='exam'),
    path('exam_view/<int:id>',views.exam_view,name="exam_view"),
    path('question_view/<int:id>',views.question_view,name="question_view"),
    path('detail/<int:pk>',views.flashcard_detail,name='flashcard_detail'),
    path('create/',views.flashcard_create,name='flashcard_create'),
    path('question/<int:flashcard_pk>',views.question_answer_create,name='question_answer_create'),
    path('research',views.research_topic,name='research_topic'),
    path('exam_form/<int:id>',views.exam_form,name="exam_form"),
    path('next_question/<int:id>',views.next_question,name="next_question"),
    path('practice_chapter/<int:id>',views.practice_form, name="practice_form"),
    path('next_practice_chapter/<int:id>',views.next_practice, name="next_practice"),
    path('correct_answer/<int:id>',views.correct_answer,name='correct_answer'),
    path('wrong_answer/<int:id>',views.wrong_answer,name='wrong_answer'),
    

]