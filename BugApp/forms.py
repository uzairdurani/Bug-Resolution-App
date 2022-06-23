from django import forms
from django.db import models
from django.forms import fields, widgets
from .models import Questions, Answers
from django_quill.fields import QuillField
from django.core.exceptions import ValidationError


class NewQuestion(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    field_order = ['title', 'body', 'tags']

    class Meta:
        model = Questions
        fields = {'title', 'body', 'tags'}
        widgets = {
            'body': forms.Textarea(attrs={'class': 'mb-3 border-1 borderrounded-0', 'rows': '15', 'cols': '92', 'placeholder': 'Detail ..'}),
        }

    def clean(self):
        data = super(NewQuestion, self).clean()
        # data = self.cleaned_data
        if len(data['title']) < 15:

            self.add_error('title', "Title must be at least 15 characters.")
        if len(data['body']) < 30:
            self.add_error(
                'body', f"Body must be at least 30 characters; you entered {len(data['body'])}.")
        if len(data['tags']) < 1:

            self.add_error(
                'tags', f"Please enter at least one tag; .")


class Questionanswer(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Answers
        fields = {'body'}
        # widgets = {
        #     'body': forms.Textarea(attrs={'class': 'mb-3 border-1 borderrounded-0', 'rows': '15', 'cols': '92', 'placeholder': 'Detail ..'}),
        # }

    def clean(self):
        data = super(Questionanswer, self).clean()
        # data = self.cleaned_data
        # if len(data['body']) < 30:

        #     self.add_error(
        #         'body', f"Body must be at least 30 characters; you entered {len(data['body'])}.")
