from django.http import request
from django.shortcuts import render
from django.core.paginator import Paginator

QUESTIONS = [
    {
        'id': i,
        'title': 'Question ' + str(i),
        'content': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et'
    } for i in range(100)
]

ANSWERS = [
    {
        'id': i,
        'content': 'Lorem ipsum dolor graecis sollicitudin agam scripserit saperet partiendo adipisci reque pharetra noluisse maluisset eius neglegentur suas causae sem convallis commune constituto comprehensam contentiones ludus assueverit porro tortor pellentesque elaboraret wisi semper causae postulant diam cubilia dicant idque viverra vim conclusion emque suas quidamsit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren'
    } for i in range(100)
]
def paginate(objects, request, per_page = 15):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page', 1)
    return paginator.page(page)

def index(request):
    return render(request, 'index.html', {'questions' : paginate(QUESTIONS, request)})

def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': item, 'answers': paginate(ANSWERS, request, 5)})
def tag_listing(request):
    return render(request, 'tag_listing.html', {'questions' : paginate(QUESTIONS, request)})

def ask(request):
    return render(request, 'ask.html')