from django.http import request
from django.shortcuts import render
from django.core.paginator import Paginator
from app import models

def paginate(objects, request, per_page = 15):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page', 1)
    return paginator.page(page)

def get_range_for_pagination(objects, request, per_page = 15):
    pages = paginate(objects, request, per_page)
    start_page = max(1, pages.number - 2)
    end_page = min(pages.paginator.num_pages, pages.number + 2)
    pagination_range = range(start_page, end_page + 1)
    return pagination_range

def index(request):
    QUESTIONS = models.Question.objects.get_all()
    answers = models.Answer.objects.get_answer_count(paginate(QUESTIONS, request))
    return render(request, 'index.html', {'questions' : paginate(QUESTIONS, request),
                                          'objects' : paginate(QUESTIONS, request),
                                          'paginator_range' : get_range_for_pagination(QUESTIONS, request),
                                          'tags': models.Tag.objects.get_popular(),
                                          'answers_count': answers})

def question(request, question_id):
    item = models.Question.objects.get_by_id(question_id)
    ANSWERS = models.Answer.objects.get_by_question(question_id)
    return render(request, 'question.html', {'question': item,
                                             'answers': paginate(ANSWERS, request),
                                             'objects': paginate(ANSWERS, request, 5),
                                             'paginator_range' : get_range_for_pagination(ANSWERS, request, 5),
                                             'tags': models.Tag.objects.get_popular()})

def tag_listing(request, tag):
    requested_questions = models.Question.objects.get_by_tag(tag)
    QUESTIONS = models.Question.objects.get_all()
    answers = models.Answer.objects.get_answer_count(paginate(QUESTIONS, request))
    return render(request, 'tag_listing.html', {'questions' : paginate(requested_questions, request),
                                                'tag' : tag,
                                                'objects': paginate(requested_questions, request),
                                                'paginator_range': get_range_for_pagination(requested_questions, request),
                                                'tags': models.Tag.objects.get_popular(),
                                                'answers_count': answers})

def ask(request):
    return render(request, 'ask.html')

def settings(request):
    return render(request, 'settings.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def hot_questions(request):
    QUESTIONS = models.Question.objects.get_hot()
    answers = models.Answer.objects.get_answer_count(paginate(QUESTIONS, request))
    return render(request, 'hot_questions.html', {'questions' : paginate(QUESTIONS, request),
                                                  'objects': paginate(QUESTIONS, request),
                                                  'paginator_range': get_range_for_pagination(QUESTIONS, request),
                                                  'tags': models.Tag.objects.get_popular(),
                                                  'answers_count': answers})