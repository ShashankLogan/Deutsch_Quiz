from django.shortcuts import render
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question, Answer
from results.models import Result
from django.template import loader

# Create your views here.

class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'

def quiz_main(request):
    quiz = Quiz.objects.all()
    topics = list(set(Quiz.objects.only('topic')))
    categories = list(set(Quiz.objects.only('topic')))
    return render(request,'quizes/main.html',{'object_list':topics,'categories':categories})


def ViewQuizListByCategory(request, *args, **kwargs):
    '''
    catego = get_object_or_404(
        Category,
        category=kwargs['category_name']
    )
    '''
    topics = Quiz.objects.filter(topic =kwargs['category_name'])
    if kwargs['category_name'] == "All":
        topics = Quiz.objects.all()
    categories = list(set(Quiz.objects.only('topic')))
    #template = loader.get_template('main.html')

    object_list = {
        'topics': topics,
        'categories':categories,
    }
    return render(request, 'quizes/main.html',{'object_list':topics,'categories':categories} ) #{'object_list':topics}
    #return HttpResponse(template.render(context, request))

def quiz_view(request,pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request,'quizes/quiz.html',{'obj':quiz})

def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answer():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time':quiz.time,

    })

def save_quiz_view(request,pk):
    #print(request.POST)
    if request.is_ajax():
        questions = []
        data= request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        #print(type(data_))
        #print(data_)
        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)
        user = request.user
        quiz = Quiz.objects.get(pk=pk)
        score = 0
        multiplier = 100 / quiz.num_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            if a_selected != "":
                question_answers = Answer.objects.filter(question = q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct answer': correct_answer,'answered':a_selected}})

            else:
                results.append({str(q):'not answered'})

        score_ = score * multiplier

        #Result.objects.create(quiz = quiz, user = user, score = score_)

        if score_ >= quiz.score_to_pass:
            return JsonResponse({'passed':True,'score':score_, 'results':results})
        else:
            return JsonResponse({'passed':False, 'score':score_, 'results':results })

    #return JsonResponse({'text':'works'})


