from django.http import request
from django.shortcuts import render
from django.core.paginator import Paginator

ANSWERS = [
    {
        'id': i,
        'content': 'Lorem ipsum dolor graecis sollicitudin agam scripserit saperet partiendo adipisci reque pharetra noluisse maluisset eius neglegentur suas causae sem convallis commune constituto comprehensam contentiones ludus assueverit porro tortor pellentesque elaboraret wisi semper causae postulant diam cubilia dicant idque viverra vim conclusion emque suas quidamsit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren'
    } for i in range(100)
]

QUESTIONS = [
    {
        'id': i,
        'title': 'Question ' + str(i),
        'content': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et',
        'tags' : [],
    } for i in range(100)
]

for i in range(100):
    if i % 2 == 0:
        QUESTIONS[i]['tags'] = ['C++', 'Databases']
    else:
        QUESTIONS[i]['tags'] = ['CSS', 'HTML']
    if i % 3 == 0:
        QUESTIONS[i]['tags'].append('Python')
    if i % 5 == 0:
        QUESTIONS[i]['tags'].append('Django')
    if i % 7 == 0:
        QUESTIONS[i]['tags'].append('Bootstrap')

def paginate(objects, request, per_page = 15):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page', 1)
    return paginator.page(page)

def index(request):
    return render(request, 'index.html', {'questions' : paginate(QUESTIONS, request)})

def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': item, 'answers': paginate(ANSWERS, request, 5)})

def tag_listing(request, tag):
    requested_questions = []
    for item in QUESTIONS:
        if tag in item['tags']:
            requested_questions.append(item)
    return render(request, 'tag_listing.html', {'questions' : paginate(requested_questions, request), 'tag' : tag})

def ask(request):
    return render(request, 'ask.html')

def settings(request):
    return render(request, 'settings.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def hot_questions(request):
    return render(request, 'hot_questions.html', {'questions' : paginate(QUESTIONS, request)})