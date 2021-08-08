from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.fields.related import ManyToManyField
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from pybo.models import Answer, Question

@login_required(login_url='common:login')
def vote_question(request:HttpRequest, question_id):
	question:Question = get_object_or_404(Question, pk = question_id)
	if question.author == request.user:
		messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
	else:
		question.voter.add(request.user)
	return redirect('pybo:detail', question_id=question.id)

@login_required(login_url='common:login')
def vote_answer(request:HttpRequest, answer_id):
	answer:Answer = get_object_or_404(Answer, pk = answer_id)
	if answer.author == request.user:
		messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
	else:
		answer.voter.add(request.user)
	return redirect('pybo:detail', question_id = answer.question.id)
