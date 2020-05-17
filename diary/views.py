from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import (
    LoginView, LogoutView,
)
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView,
)
from .mixins import OnlyYouMixin
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm, DiaryCreateForm
)
from django.views import generic
from .models import Diary, Category, Writer
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404, resolve_url
from django.db.models import Q
from .forms import DiarySearchForm
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

UserModel = get_user_model()

class TopView(LoginRequiredMixin, TemplateView):
    template_name = 'diary/top.html'

class Login(LoginView):
    form_class = LoginForm
    template_name = 'diary/login.html'

class Logout(LogoutView):
    template_name = 'diary/top.html'

class UserCreate(CreateView):
    form_class = UserCreateForm
    template_name = 'diary/signup.html'
    success_url = reverse_lazy('diary:diary')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class UserUpdate(UpdateView):
    model = UserModel
    #form_class = UserUpdateForm
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = 'diary/user_update.html'
    success_url = reverse_lazy('diary:user_detail')

    def get_object(self):
        return self.request.user

@method_decorator(login_required, name='dispatch')
class UserDetail(TemplateView):
    #model = UserModel
    template_name = 'diary/user_detail.html'
    def get_queryset(self):
        return User.objects.get(user=self.request.user)

class UserDelete(OnlyYouMixin, DeleteView):
    model = UserModel
    template_name = 'diary/user_delete.html'
    success_url = reverse_lazy('diary:top')

"""
@login_required
def PostCreate(request):
    diary = Diary()
    diary.user = request.user
    if request.method == "POST":
        form = DiaryCreateForm(request.POST, instance=diary)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.user = request.user
            diary.save()
        else:
            return render(request, 'diary/create.html', {'form': form})
    else:
        form = DiaryCreateForm(instance=diary)
    return render(request, 'diary/create.html', {'form': form})
"""
"""
@login_required
def PostCreate(request):
    template_name = 'diary/create.html'
    ctx = {}
    if request.method == 'GET':
        form = DiaryCreateForm()
        ctx['form'] = form
        return render(request, template_name, ctx)

    if request.method == 'POST':
        diary_form = DiaryCreateForm(request.POST)
        if diary_form.is_valid():
            diary = Diary()
            cleaned_data = diary_form.cleaned_data
            diary.title = cleaned_data['title']
            diary.text = cleaned_data['text']
            diary.user = request.user
            diary.category = cleaned_data['category']
            diary.save()
            return redirect(reverse_lazy('diary:diary'))
        else:
            ctx['form'] = diary_form
            return render(request, template_name, ctx)
"""

class PostCreate(generic.CreateView):
    template_name = 'diary/create.html'
    model = Diary
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(PostCreate, self).form_valid(form)

class ArchiveListMixin:
    model = Diary
    paginate_by = 12
    date_field = 'created_at'
    template_name = 'diary/mydiary.html'
    allow_empty = True
    make_object_list = True


class DiaryList(ArchiveListMixin, generic.ArchiveIndexView):

    def get_queryset(self):
        result = super().get_queryset().select_related('category')
        return result.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Latest diary'
        #context['pk'] = self.kwargs['pk']
        return context

class DiaryDetail(generic.DetailView):
    model = Diary

    def get_object(self, queryset=None):
        diary = super().get_object()
        if diary.created_at <= timezone.now():
            return diary
        raise Http404

class DiaryCategoryList(ArchiveListMixin, generic.ArchiveIndexView):

    def get_queryset(self):
        self.category = category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return super().get_queryset().filter(category=category, user=self.request.user).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = '「{}」 Category Diary'.format(self.category.name)
        return context

class DiarySearchList(ArchiveListMixin, generic.ArchiveIndexView):

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        self.request.form = form = DiarySearchForm(self.request.GET)
        form.is_valid()
        self.key_word = key_word = form.cleaned_data['key_word']
        if key_word:
            queryset = queryset.filter(Q(title__icontains=key_word) | Q(text__icontains=key_word))
        return queryset.select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = '「{}」 の検索結果'.format(self.key_word)
        return context
