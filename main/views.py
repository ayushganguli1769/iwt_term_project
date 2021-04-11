from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .models import Question, subQuestion
#importing chatbot
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import logging 
logger = logging.getLogger() 
logger.setLevel(logging.CRITICAL)

bot = ChatBot(
    'Norman',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',read_only=True,
          logic_adapters=
    ['chatterbot.logic.MathematicalEvaluation', 'chatterbot.logic.BestMatch'])
list_trainer = ListTrainer(bot)
import json
def chat_input(request,text):
    global bot
    my_bot_response = bot.get_response(text)
    #print(my_bot_response)
    return_val = json.dumps({'question':text,'bot_response': str(my_bot_response)})
    return HttpResponse(return_val)
def test(request):
    return HttpResponse("ok")
def login(request):
    if 'login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user != None:
            auth.login(request,user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error_message': "Invalid Credentials"})
    return render(request, 'login.html')
@login_required
def dashboard(request):
    global list_trainer
    all_questions = Question.objects.all()
    #print(all_questions)
    try:
        if 'input_submit' in request.POST:
            total_main_questions = int(request.POST['total_question'])
            for i in range(1,total_main_questions+1):
                total_sub_questions = int(request.POST['subTotal' + str(i)])
                #print(total_sub_questions,'total_sub_questions')
                question_list = []
                for j in range(1,total_sub_questions+1):
                    curr_question_text = request.POST['subQuestionDiv'+ str(i) + 'Question' + str(j)]
                    question_list.append(curr_question_text)
                curr_answer = request.POST['answer' + str(i)]
                main_question = Question(display_text= question_list[0],filled= True,answer= curr_answer)
                main_question.save()
                for sub in question_list:
                    list_trainer.train([sub,curr_answer])
                    curr_sub_question = subQuestion(main_question= main_question, sub_question_display_text = sub)
                    curr_sub_question.save()
    except:
        return render(request,'dashboard.html',{'error':"Seems like some text fields aren't filled",'all_questions':all_questions})
    return render(request,'dashboard.html',{'all_questions':all_questions})
def chat_box(request):
    return render(request,'chat.html')