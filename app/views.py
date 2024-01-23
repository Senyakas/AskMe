from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import request
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from app import models
from app.forms import LoginForm, RegistrationForm


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
                                             'objects': paginate(ANSWERS, request),
                                             'paginator_range' : get_range_for_pagination(ANSWERS, request, 15),
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

@login_required(login_url='/login', redirect_field_name='continue')
def ask(request):
    return render(request, 'ask.html')

@login_required(login_url='/login', redirect_field_name='continue')
def settings(request):
    return render(request, 'settings.html')

@csrf_protect
def log_in(request):
    if request.method == "GET":
        login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, "Wrong password or user does not exist")
    context = {'form': login_form}
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))

@csrf_protect
def signup(request):
    if request.method == "GET":
        signup_form = RegistrationForm()
    if request.method == "POST":
        signup_form = RegistrationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            if user:
                login(request, authenticate(request, **signup_form.cleaned_data))
                return redirect(reverse('index'))
            else:
                signup_form.add_error(None, "Failed to create user")
    context = {'form': signup_form}
    return render(request, 'signup.html', context)

def hot_questions(request):
    QUESTIONS = models.Question.objects.get_hot()
    answers = models.Answer.objects.get_answer_count(paginate(QUESTIONS, request))
    return render(request, 'hot_questions.html', {'questions' : paginate(QUESTIONS, request),
                                                  'objects': paginate(QUESTIONS, request),
                                                  'paginator_range': get_range_for_pagination(QUESTIONS, request),
                                                  'tags': models.Tag.objects.get_popular(),
                                                  'answers_count': answers})