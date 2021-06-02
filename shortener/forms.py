from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

from django import forms
from django.contrib.auth.models import Group

from .tasks import send_emails_task

groups = Group.objects.all()
GROUP_CHOICES = [(g.name, g.name) for g in groups]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class SendEmailForm(forms.Form):
    group = forms.CharField(
        label='User groups', widget=forms.Select(choices=GROUP_CHOICES)
    )
    subject = forms.CharField(
        label="Subject", widget=forms.Textarea(attrs={'rows': 1})
    )
    message = forms.CharField(
        label="Letter", widget=forms.Textarea(attrs={'rows': 5})
    )

    def send_email(self):

        users = CustomUser.objects.filter(
            groups__name=self.cleaned_data['group']
        )
        emails = [u.email for u in users]
        send_emails_task.delay(
            emails, self.cleaned_data['subject'], self.cleaned_data['message']
        )

