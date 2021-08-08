from typing import ContextManager
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey, ManyToManyField

# Create your models here.

class Question(models.Model):
	subject = models.CharField(max_length=200)
	content = models.TextField()
	create_date = models.DateTimeField()
	modify_date = models.DateTimeField(null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
	voter:ManyToManyField = models.ManyToManyField(User, related_name='voted_question')
	def __str__(self):
		return self.subject


class Answer(models.Model):
	question:Question = models.ForeignKey(Question, on_delete=models.CASCADE)
	content = models.TextField()
	create_date = models.DateTimeField()
	modify_date = models.DateTimeField(null=True, blank=True)
	author:User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
	voter:ManyToManyField = models.ManyToManyField(User, related_name='voted_answer')
	def __str__(self):
		return str(self.question.subject) + '에 대한 답변'

class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	create_date = models.DateTimeField()
	modify_date = models.DateTimeField(null = True, blank=True)
	question:Question = ForeignKey(Question, on_delete=models.CASCADE, null = True, blank=True)
	answer:Answer = ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)



