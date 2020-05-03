from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Diary, Category
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .forms import DiarySearchForm


class ArchiveListMixin:
    model = Diary
    paginate_by = 12
    date_field = 'created_at'
    template_name = 'diary/mydiary.html'
    allow_empty = True
    make_object_list = True


class DiaryList(ArchiveListMixin, generic.ArchiveIndexView):

    def get_queryset(self):
        return super().get_queryset().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Latest diary'
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
