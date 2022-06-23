from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import RegistrationForm, UserEditForm, UserProfileForm,MyForm
from .tokens import account_activation_token
from .models import Profile
# from blog.models import Post, Vote
from django.http import JsonResponse
from django.db.models import F, Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from BugApp.models import Questions, Answers, QVote, AVote

# Create your views here.


def thumbs(request):

    if request.POST.get('action') == 'thumbs':

        id = int(request.POST.get('postid'))
        button = request.POST.get('button')
        classModel = request.POST.get('classModel')
        if classModel == 'question':
            update = Questions.objects.get(id=id)

            if update.thumbs.filter(id=request.user.id).exists():

                # Get the users current vote (True/False)
                q = QVote.objects.filter(
                    Q(question_id=id) & Q(user_id=request.user.id))[0]

                evote = q.vote

                if evote == True:
                    print('what fucking is going on True')

                    # Now we need action based upon what button pressed

                    if button.startswith('thumbsup'):

                        update.thumbsup = F('thumbsup') - 1
                        update.thumbs.remove(request.user)
                        update.save()
                        update.refresh_from_db()
                        up = update.thumbsup
                        down = update.thumbsdown
                        q.delete()

                        return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

                    if button.startswith('thumbsdown'):

                        # Change vote in Post
                        update.thumbsup = F('thumbsup') - 1
                        update.thumbsdown = F('thumbsdown') + 1
                        update.save()

                        # Update Vote

                        q.vote = False
                        q.save(update_fields=['vote'])

                        # Return updated votes
                        update.refresh_from_db()
                        up = update.thumbsup
                        down = update.thumbsdown

                        return JsonResponse({'up': up, 'down': down})

                if evote == False:
                    print('what fucking is going on false')

                    if button.startswith('thumbsup'):

                        # Change vote in Post
                        update.thumbsup = F('thumbsup') + 1
                        update.thumbsdown = F('thumbsdown') - 1
                        update.save()

                        # Update Vote

                        q.vote = True
                        q.save(update_fields=['vote'])

                        # Return updated votes
                        update.refresh_from_db()
                        up = update.thumbsup
                        down = update.thumbsdown

                        return JsonResponse({'up': up, 'down': down})

                    if button.startswith('thumbsdown'):

                        update.thumbsdown = F('thumbsdown') - 1
                        update.thumbs.remove(request.user)
                        update.save()
                        update.refresh_from_db()
                        up = update.thumbsup
                        down = update.thumbsdown
                        q.delete()

                        return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

            else:        # New selection

                if button.startswith('thumbsup'):

                    update.thumbsup = F('thumbsup') + 1
                    update.thumbs.add(request.user)
                    update.save()
                    # Add new vote
                    new = QVote(question_id=id,
                                user_id=request.user.id, vote=True)
                    new.save()
                else:
                    # Add vote down

                    update.thumbsdown = F('thumbsdown') + 1
                    update.thumbs.add(request.user)
                    update.save()
                    # Add new vote
                    new = QVote(question_id=id,
                                user_id=request.user.id, vote=False)
                    new.save()

                # Return updated votes
                update.refresh_from_db()
                up = update.thumbsup
                down = update.thumbsdown

                return JsonResponse({'up': up, 'down': down})
        elif classModel == 'answer':
            update = Answers.objects.get(id=id)

            if update.thumbs.filter(id=request.user.id).exists():
                print('get started function /////////////////////')
                # Get the users current vote (True/False)
                q = AVote.objects.filter(
                    Q(answer_id=id) & Q(user_id=request.user.id))[0]
                evote = q.vote

                if evote == True:
                    print('get started function True /////////////////////')

                    # Now we need action based upon what button pressed

                    if button.startswith('thumbsup2'):
                        print('get click on thumup function /////////////////////')
                        update.thumbsup = F('thumbsup') - 1
                        update.thumbs.remove(request.user)
                        update.save()
                        update.refresh_from_db()
                        up = update.thumbsup
                        down = update.thumbsdown
                        q.delete()

                        return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

                    if button.startswith('thumbsdown2'):
                        print(
                            'get started clicked on down function /////////////////////')

                        # Change vote in Post
                        update.thumbsup = F('thumbsup') - 1
                        update.thumbsdown = F('thumbsdown') + 1
                        update.save()

                        # Update Vote

                        q.vote = False
                        q.save(update_fields=['vote'])

                        # Return updated votes
                        update.refresh_from_db()
                        up = update.thumbsup
                        down = update.thumbsdown

                        return JsonResponse({'up': up, 'down': down})

                if evote == False:

                    if button.startswith('thumbsup'):

                        # Change vote in Post
                        update.thumbsup = F('thumbsup') + 1
                        update.thumbsdown = F('thumbsdown') - 1
                        update.save()

                        # Update Vote

                        q.vote = True
                        q.save(update_fields=['vote'])

                        # Return updated votes
                        update.refresh_from_db()
                        up = update.thumbsup
                        down = update.thumbsdown

                        return JsonResponse({'up': up, 'down': down})

                    if button.startswith('thumbsdown'):

                        update.thumbsdown = F('thumbsdown') - 1
                        update.thumbs.remove(request.user)
                        update.save()
                        update.refresh_from_db()
                        up = update.thumbsup
                        down = update.thumbsdown
                        q.delete()

                        return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

            else:        # New selection

                if button.startswith('thumbsup'):
                    print('get created up function /////////////////////')

                    update.thumbsup = F('thumbsup') + 1
                    update.thumbs.add(request.user)
                    update.save()
                    # Add new vote
                    new = AVote(answer_id=id,
                                user_id=request.user.id, vote=True)
                    new.save()
                else:
                    # Add vote down
                    print('get clicked on donw function /////////////////////')
                    update.thumbsdown = F('thumbsdown') + 1
                    update.thumbs.add(request.user)
                    update.save()
                    # Add new vote
                    new = AVote(answer_id=id,
                                user_id=request.user.id, vote=False)
                    new.save()

                # Return updated votes
                update.refresh_from_db()
                up = update.thumbsup
                down = update.thumbsdown
                print('get clicked on donw function /////////////////////')

                return JsonResponse({'up': up, 'down': down})

        pass


@ login_required
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()

        return JsonResponse({'result': result, })


def avatar(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        avatar = Profile.objects.filter(user=user)
        context = {
            "avatar": avatar,
        }
        print(avatar)
        return context
    else:
        return {
            'NotLoggedIn': User.objects.none()
        }


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)

        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid() and user_form.is_valid():

            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request,
                  'accounts/update.html',
                  {
                      'user_form': user_form,
                      'profile_form': profile_form
                  }
                  )


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'section': 'profile'})


@login_required
def delete_user(request):

    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return redirect('accounts:login')

    return render(request, 'accounts/delete.html')


def account_register(request):

    if request.method == 'POST':
        newform=MyForm(request.POST)
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid() and newform.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('login')

        else:
            # registerForm = RegistrationForm()
            return render(request, 'registration/register.html', {'form': registerForm,'newform':newform})
       
    else:
        newform=MyForm()
        registerForm = RegistrationForm()
        return render(request, 'registration/register.html', {'form': registerForm,'newform':newform})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')



# code for sending mail to user
     
        # current_site = get_current_site(request)
        # subject = 'Activate your Account'
        # message = render_to_string('registration/account_activation_email.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': account_activation_token.make_token(user),
        # })

        # # user.email_user(subject=subject, message=message)
        # send_mail(subject, message, 'muhammeduzair098@gmail.com',
        #           [user.email], fail_silently=False)
        # print('email send')
        # return HttpResponse('registered succesfully and activation sent')
        # return redirect(to='accounts:login')