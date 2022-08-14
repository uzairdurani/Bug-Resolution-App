from hashlib import new

from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from BugApp.forms import NewQuestion, Questionanswer
from .models import Questions, Answers, QuestionView, Comment, AnswersComment
from django.db.models import Q, F
from django.contrib.auth.models import User
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def count_answers(question, id):
    return len(Answers.objects.filter(question__pk=id))


@register.filter
def checkAnswer(question, id):
    return len(Answers.objects.filter(question__pk=id)) != 0


@register.filter
def countVotes(question, id):
    question = Questions.objects.get(Q(pk=id))
    votes = question.thumbsup - question.thumbsdown
    return votes


@register.filter
def countViews(question, id):
    viewss = QuestionView.objects.filter(question__id=id).count()
    return viewss


def home(request):
    questions = Questions.objects.all()
    tags = {}
    for i in questions:

        tags[i.title] = i.tags.all()

    return render(request, 'App/pageContent.html',  {"questions": questions, 'tags': tags, })


def tags(request):
    list_of_tags = []
    questions = Questions.objects.all()
    for i in questions:
        for j in i.tags.all():
            list_of_tags.append(str(j).strip())
    list_of_tags = list(set(list_of_tags))
    counter = {}
    for i in list_of_tags:
        questions = Questions.objects.filter(tags__name__in=[i])
        counter[i] = len(questions)
    print(counter)
    return render(request, 'App/tags.html', {'tags': list_of_tags, 'counter': counter})


@login_required
def taggedSearch(request, search):
    questions = Questions.objects.filter(tags__name__in=[search])
    tags = {}
    for i in questions:

        tags[i.title] = i.tags.all()

    return render(request, 'App/pageContent.html',  {"questions": questions, 'tags': tags, })


def single_question(request, id):
    if not request.user.is_authenticated and request.method == 'POST':
        return redirect('https://bugresolution.herokuapp.com/account/login/')

    if request.method == 'POST':
        newQuestionForm = Questionanswer(request.POST or None)
        if newQuestionForm.is_valid():
            user = newQuestionForm.save(commit=False)
            user.author = request.user
            user.question = Questions.objects.get(pk=id)
            user.thumbsup = 0
            user.thumbsdown = 0

            user.save()
            return redirect(to='https://bugresolution.herokuapp.com/question/'+str(id))

    else:
        try:
            questions = Questions.objects.get(pk=id)
        except Questions.DoesNotExist:
            raise Http404()
        if not QuestionView.objects.filter(
                question=questions,
                session=request.session.session_key):
            view = QuestionView(question=questions,
                                ip=request.META['REMOTE_ADDR'],
                                session=request.session.session_key)
            view.save()
        # questions.views_count = F('views_count') + 1
        # questions.save()
        questions.refresh_from_db()
        viewss = QuestionView.objects.filter(question=questions).count()
        answers = Answers.objects.filter(Q(question__id=id))
        tag = questions.tags.all()
        tags = {questions.title: questions.tags.all()}
        newQuestionForm = NewQuestion()

        # check that author and current user is same so show than it edit form
        checkUser = request.user == questions.author
        comments = Comment.objects.filter(Q(question__id=id))

        answercomments = {}
        for i in answers:
            answercomments[i.id] = AnswersComment.objects.filter(
                Q(answers__id=i.id))

        return render(request, 'App/singleQuestion.html',  {"question": questions,
                                                            'tags': tags,
                                                            'counter': viewss,
                                                            'answers': answers,
                                                            'AdminPost': checkUser,
                                                            'form': newQuestionForm,
                                                            'commentsQues': comments,
                                                            'answersComment': answercomments
                                                            }
                      )


@login_required
def askQuestion(request):

    if request.method == 'POST':

        newQuestionForm = NewQuestion(request.POST or None)

        if newQuestionForm.is_valid():
            if not Questions.objects.filter(Q(title=request.POST['title']) & Q(author__id=request.user.id)).exists():
                user = newQuestionForm.save(commit=False)
                new = Questions.objects.create(
                    title=request.POST['title'], body=request.POST['body'], author=request.user)
                array = request.POST['tags'].split(',')

                for i in array:
                    new.tags.add(i)

                if not new.slug:
                    new.slug = slugify(new.title)
                new.save()
                return redirect(to='BugApp:home')
            else:
                value = Questions.objects.filter(
                    Q(title=request.POST['title']) & Q(author__id=request.user.id)).first()

                return redirect(to='https://bugresolution.herokuapp.com/question/'+str(value.id))

        else:
            errors = newQuestionForm.errors
            # error = errors.as_data()['__all__'][0][0]

            return render(request, 'App/askQuestion.html', {'form': newQuestionForm, })
    else:
        newform = NewQuestion()
    return render(request, 'App/askQuestion.html', {'form': newform})


@login_required
def editQuestion(request, id):
    instance = get_object_or_404(Questions, pk=id)
    if request.method == 'POST':
        form = NewQuestion(request.POST or None, instance=instance)
        if form.is_valid():
            array = request.POST['tags'].split(',')

            for i in array:
                instance.tags.add(i)
            form.save()
            return redirect(to='https://bugresolution.herokuapp.com/question/'+str(instance.id))
        else:
            return render(request, 'App/askQuestion.html', {'form': form, })

    else:

        form = NewQuestion(instance=instance)

        return render(request, 'App/askQuestion.html', {'form': form, 'type': 'edit', 'question': instance.id})


def Search(request):
    if request.method == "POST":
        search = request.POST['search']
        searchItems = Questions.objects.filter(
            Q(title__icontains=search))
        tags = {}
        for i in searchItems:

            tags[i.title] = i.tags.all()

        return render(request, 'App/Search.html',  {"questions": searchItems, 'tags': tags, })

    else:
        return redirect(to='BugApp:home')


@login_required
def addComment(request):

    if request.method == 'POST':

        if request.POST.get('action') == 'delete':
            id = request.POST.get('nodeid')
            c = Comment.objects.get(id=id)
            c.delete()
            return JsonResponse({'remove': id})
        else:
            if not request.user.is_authenticated:
                return JsonResponse({'status': 0, 'result': 'urls hit', 'user': 'user'})
            else:
                id = int(request.POST.get('postid'))
                classModel = request.POST.get('classModel')

                review = request.POST['comment']

                user = request.user

                if classModel == 'question':
                    ques = Questions.objects.get(pk=id)

                    newobj = Comment.objects.create(
                        author=user, question=ques, content=review)

                elif classModel == 'answer':
                    ques = Answers.objects.get(pk=id)

                    newobj = AnswersComment.objects.create(
                        author=user, answers=ques, content=review)

                return JsonResponse({'status': 1, 'result': f'{review}', 'user': f'{user.username}'})


@login_required
def commentDelete(request, id, pk):
    try:
        instance = Comment.objects.get(pk=id)

    except Comment.DoesNotExist:
        raise Http404()
    instance.delete()
    return redirect(to='https://bugresolution.herokuapp.com/question/'+str(pk))


@login_required
def answercommentDelete(request, id, pk):
    try:
        instance = AnswersComment.objects.get(pk=id)

    except Comment.DoesNotExist:
        raise Http404()
    instance.delete()
    return redirect(to='https://bugresolution.herokuapp.com/question/'+str(pk))


@login_required
def question_delete(request, id):
    try:
        instance = Questions.objects.get(pk=id)

    except Comment.DoesNotExist:
        raise Http404()
    instance.delete()
    return redirect(to='/')
