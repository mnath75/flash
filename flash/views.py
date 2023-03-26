from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Flashcard, QuestionAnswer,Chapter,Timer
from .forms import FlashcardForm, QuestionAnswerForm,ResearchTopicForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date,datetime



def home(request):    
    return render(request,'flash/home.html')

def exam(request):
    obj = Flashcard.objects.all()
    return render(request,'flash/exam.html',{'obj':obj})

def exam_view(request,id):
    f_id = Flashcard.objects.get(id=id)
    chap = Chapter.objects.filter(flash=f_id)
    return render(request,'flash/exam_view.html',{'chap':chap})

def question_view(request,id):

    c_id = Chapter.objects.get(id=id)
    ques = QuestionAnswer.objects.filter(chapter=c_id)
    return render(request,'flash/question_view.html',{'ques':ques})


def flashcard_detail(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    questions_answers = flashcard.questions_answers.all()
    return render(request, 'flash/detail.html', {'flashcard': flashcard, 'questions_answers': questions_answers})

def flashcard_create(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save()
            return redirect('flashcard_detail', pk=flashcard.pk)
    else:
        form = FlashcardForm()
    return render(request, 'flash/create.html', {'form': form})

def question_answer_create(request, flashcard_pk):
    flashcard = get_object_or_404(Flashcard, pk=flashcard_pk)
    if request.method == 'POST':
        form = QuestionAnswerForm(request.POST)
        if form.is_valid():
            flashcard = form.save()
            return redirect('flashcard_detail', pk=flashcard.pk)
    else:
        form = QuestionAnswerForm()
    return render(request, 'flash/question_answer.html', {'form': form})

def research_topic(request):
    if request.method =="POST":
        form = ResearchTopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('research_topic')
    else:
        form = ResearchTopicForm()
    return render(request,'flash/research.html',{'form':form})

def login_view(request):    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'flash/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

def flashcard(request):
    obj = Flashcard.objects.all()
    return render(request,'flash/flashcard.html',{'obj':obj})

def subject(request,id):    
    
    obj = Chapter.objects.filter(flash__id=id)       
    return render(request,'flash/subject.html',{'id':id,'obj':obj})

def delete_data():
    data = Timer.objects.all()
    data.delete()

@login_required   
def exam_form(request,id): 

    status = False
    if request.user:
        status = request.user 

    delete_data()  
    
    obj = QuestionAnswer.objects.filter(chapter__id = id).first()

    if request.method == 'POST':
        q_id = QuestionAnswer.objects.get(id=obj.id)
        user_id = User.objects.get(username=status)
        time = request.POST['timer_one']        
        if request.POST.get('button') == obj.option:                    
            ans = Timer.objects.create(question=q_id,user=user_id,timer=time,answer=True,time_start=datetime.now())
            ans.save()
        else:            
            ans = Timer.objects.create(question=q_id,user=user_id,timer=time,answer=False,time_start=datetime.now())
            ans.save()
        return HttpResponseRedirect(reverse('next_question',kwargs={'id':obj.id})) 
    
    return render(request,'flash/form.html',{'obj':obj})

len_question = 0
@login_required 
def next_question(request,id):   
    
    global len_question      
    status = False
    if request.user:
        status = request.user     
    obj = QuestionAnswer.objects.filter(id__gt=id).first()
    
    if request.method == 'POST':
            q_id = QuestionAnswer.objects.filter(id__gt=id).first()
            user_id = User.objects.get(username=status)
            time = request.POST['timer_one']            
            if request.POST.get('button') == obj.option:                
                ans = Timer.objects.create(question=q_id,user=user_id,timer=time,answer=True,time_start=datetime.now())
                ans.save()
            else:
                ans = Timer.objects.create(question=q_id,user=user_id,timer=time,answer=False,time_start=datetime.now())
                ans.save()
            return HttpResponseRedirect(reverse('next_question',kwargs={'id':id+1}))    
    chap_question = QuestionAnswer.objects.get(id=id)
    question = QuestionAnswer.objects.filter(chapter__id = chap_question.chapter_id)
    len_question= len(question)   
    obj1 = QuestionAnswer.objects.filter(chapter__id = chap_question.chapter_id,id__gt=id).first() 
    if obj1:
        return render(request,'flash/next.html',{'obj':obj1})
    else:
        start_time = Timer.objects.all().first()
        end_time = Timer.objects.all().last()        
        final_start_time = start_time.time_start
        final_end_time = end_time.time_start        
        duration = final_end_time - final_start_time       
        seconds = duration.total_seconds()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        pre_url = request.META.get('HTTP_REFERER')        
        ques_id = pre_url.split('next_question/')[1]
        data = Timer.objects.all()
        my_list_true = []
        my_list_false = []
        for d in data:
            if d.answer:
                dt = QuestionAnswer.objects.get(id=d.question_id)
                my_list_true.append(dt)                
            else:
                df = QuestionAnswer.objects.get(id=d.question_id)
                my_list_false.append(df)        
        wrong_ans = len(my_list_false)
        right_count = len(my_list_true)        
       
        return render(request,'flash/score.html',{'count':right_count,'len_question':len_question,'wrong':wrong_ans,'ques_id':ques_id,'hours':hours,'minutes':minutes,'seconds':seconds})

@login_required 
def practice_form(request,id):
    obj = QuestionAnswer.objects.filter(chapter__id = id).first()      
    return render(request,'flash/practice_form.html',{'obj':obj})

count_practice = 0
len_question_practice = 0
@login_required 
def next_practice(request,id):
    global count_practice,len_question_practice       
    obj = QuestionAnswer.objects.get(id=id)
    if request.POST.get('button') == obj.option:
        count_practice += 1    
    chap_question = QuestionAnswer.objects.get(id=id)
    question = QuestionAnswer.objects.filter(chapter__id = chap_question.chapter_id)
    len_question_practice = len(question)    
    obj1 = QuestionAnswer.objects.filter(chapter__id = chap_question.chapter_id,id__gt=id).first()
    if obj1:
        return render(request,'flash/next_practice.html',{'obj':obj1})
    else:        
        # wrong_ans = len_question_practice - count_practice
        return render(request,'flash/practice_score.html')

        # return render(request,'flash/practice_score.html',{'count':count_practice,'len_question':len_question_practice,'wrong':wrong_ans})
    


def correct_answer(request,id):
    status = False
    if request.user:
        status = request.user    
    data = User.objects.get(username = status) 
    chap = QuestionAnswer.objects.get(id=id)
    answer = Timer.objects.filter(user=data,date=date.today(),question__chapter_id =chap.chapter_id,answer=True)    
    my_list = []    
    for a in answer:
        ques = QuestionAnswer.objects.get(id = a.question.id)
        my_list.append(ques)
    return render(request,'flash/correct_answer.html',{'ques':my_list})

def wrong_answer(request,id):
    status = False
    if request.user:
        status = request.user
    data = User.objects.get(username = status)
    chap = QuestionAnswer.objects.get(id=id)
    answer = Timer.objects.filter(user=data,date=date.today(),question__chapter_id =chap.chapter_id,answer=False)
    my_list = []
    for a in answer:
        ques = QuestionAnswer.objects.get(id = a.question.id)
        my_list.append(ques)
    return render(request,'flash/wrong_answer.html',{'ques':my_list})

    

    