from django.shortcuts import render

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
    LoginForm, UserCreateForm, UserUpdateForm,
)
from django.views import generic
from .models import Diary, Category
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .forms import DiarySearchForm
from django.views.generic.detail import DetailView


UserModel = get_user_model()

class TopView(TemplateView):
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

class UserUpdate(OnlyYouMixin, UpdateView):
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'diary/user_update.html'

    def get_success_url(self):
        return resolve_url('diary:user_detail', pk=self.kwargs['pk'])

class UserDetail(OnlyYouMixin, DetailView):
    model = UserModel
    template_name = 'diary/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

class UserDelete(OnlyYouMixin, DeleteView):
    model = UserModel
    template_name = 'diary/user_delete.html'
    success_url = reverse_lazy('diary:top')


class ArchiveListMixin:
    model = Diary
    paginate_by = 12
    date_field = 'created_at'
    template_name = 'diary/mydiary.html'
    allow_empty = True
    make_object_list = True


class DiaryList(ArchiveListMixin, generic.ArchiveIndexView):
    #OnlyYouMixinの継承予定, 
    #model = UserModel

    def get_queryset(self):
        return super().get_queryset().select_related('category')

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
        return super().get_queryset().filter(category=category).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = '「{}」 Category Diary'.format(self.category.name)
        return context

class DiarySearchList(ArchiveListMixin, generic.ArchiveIndexView):

    def get_queryset(self):
        queryset = super().get_queryset()
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
