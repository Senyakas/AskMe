from django.shortcuts import render
from django.core.paginator import Paginator

QUESTIONS = [
    {
        'id': i,
        'title': 'Question ' + str(i),
        'content': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et'
    } for i in range(100)
]

def paginate(objects, page, per_page = 15):
    paginator = Paginator(objects, per_page)
    return paginator.page(page)

def index(request):
    return render(request, 'index.html', {'questions' : paginate(QUESTIONS, 2)})

def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': item})