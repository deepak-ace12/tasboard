from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from todo.models import Todo


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if (email and User.objects.filter(
                email=email).exclude(username=username).exists()):
            raise forms.ValidationError(
                'A user with this email address already exists.')
        return email

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'password1', 'password2'
        )


class TodoForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.instanace = kwargs.get('instance')
        super(TodoForm, self).__init__(*args, **kwargs)
        self.fields['assignee'].queryset = User.objects.filter(
            profile__domain=self.user.profile.domain,
            profile__is_approved=True
        )

    def clean(self):
        super(TodoForm, self).clean()
        status = self.cleaned_data.get('status')
        assignee = self.cleaned_data.get('assignee')
        if status == Todo.DONE and assignee != self.user:
            raise ValidationError(
                "ERROR: You are not allowed to mark this task complete."
            )
        return self.cleaned_data

    def save(self, commit=True):
        todo = super(TodoForm, self).save(commit=False)
        if not todo.id:
            todo.assignor = self.user
        if commit:
            todo.save()

        return todo

    class Meta:
        model = Todo
        exclude = ('assignor',)
