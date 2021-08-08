from django import forms
from django.db.models import fields
from django.forms import widgets
from pybo.models import Answer, Comment, Question

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['subject', 'content']
		labels = {
			'subject' : '제목',
			'content' : '내용',
		}

class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['content']
		labels = {
			'content':'답변내용'
		}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']
		labels = {
			'content': '댓글 내용'
		}
