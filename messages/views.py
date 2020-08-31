from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .forms import MessageForm
from .models import Message

# Create your views here.
from .service import MessageService


def index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse('login'))

    if request.method == "POST":
        # save new message, user_id - current_user
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.user_id = user.id
            new_message.save()
        return redirect("messages:index")

    order_by = request.GET.get('order', '-pub_date')
    filters = {}
    last_24_hours = request.GET.get('last_24_hours', False) == 'true'
    if last_24_hours:
        filters['date_from'] = datetime.now() - timedelta(days=1)
    user_id = request.GET.get('user_id')
    if user_id:
        filters['user_id'] = user_id

    message_service = MessageService()
    messages = message_service.get_messages(
        order_by=order_by,
        **filters
    )

    return render(
        request,
        "index.html",
        {
            "form": MessageForm,
            "latest_messages": messages,
            "order_by": order_by,
            "last_24_hours": last_24_hours,
            "users": User.objects.all(),
            "selected_user": user_id,
        }
    )


def detail(request, message_id):
    return render(request, "detail.html", {"message": get_object_or_404(Message, pk=message_id)})


def message(request, message_id):
    messages = get_object_or_404(Message, pk=message_id)
    try:
        user = messages.user.get(pk=request.POST['user'])
    except (KeyError, User.DoesNotExist):
        return render(request, 'detail.html', {'message': message, 'error_message': "Message does not exist"})
    else:
        if user.correct:
            return render(request, "index.html", {"latest_messages": Message.text.order_by('-pub_date')[:5],
                                                  "message": "Nice! Choose another one!"})
        else:
            return render(request, 'answer.html', {'message': message(), 'error_message': 'Wrong Answer!'})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('messages:index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
