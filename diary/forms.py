from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Diary, Category, User


class DiarySearchForm(forms.Form):
    """検索フォーム。"""
    key_word = forms.CharField(
        label='Search',
        required=False,
    )

UserModel = get_user_model()

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'input'
       self.fields['password'].widget.attrs['class'] = 'input'

class UserCreateForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'

"""
class DiaryCreateForm(forms.Form):
    title = forms.CharField(
        label='Title',
        max_length=32,
        required=True,
    )
    category = forms.ModelChoiceField(
        label='Category',
        queryset=Category.objects.all(),
        required=True,
        empty_label='選択して下さい',
    )
    text = forms.CharField(
        label='Contents',
        widget=forms.Textarea,
        required=True,
    )
"""
"""
CHOICES = (
("request.POSTの中身", "画面に表示される内容"),
("0", "1000"),
("1", "2000"),
("2", "3000"),
("3", "4000"),
)
class DiaryCreateForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ('title', 'text', 'category')

    category = forms.ChoiceField(
        widget=forms.Select,
        choices=CHOICES,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'
"""

class DiaryCreateForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ('title', 'text', 'category')

    category = forms.ModelChoiceField(
        label='カテゴリ',
        queryset=Category.objects,
        #required=False
    )
