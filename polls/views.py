# from django.shortcuts import render

# # Create your views here.
# from django.http import HttpResponse
 
# # def index(request):
# #     response = HttpResponse()
# #     response.write("<h1>Welcome</h1>")
# #     response.write("This is the polls app")
# #     return response

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)
 
# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)
 
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

# from django.http import HttpResponse
 
# from .models import Question
 
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
 
from .models import Question 
 
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
 
from .models import Question
 
def detail(request, question_id): 
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question':question})
