from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.http import HttpRequest

from pybo.forms import AnswerForm
from pybo.models import Question, Answer

@login_required(login_url='common:login')
def answer_create(request:HttpRequest, question_id:int):
	question:Question = get_object_or_404(Question, pk = question_id)
	if request.method == 'POST':
		form = AnswerForm(request.POST)
		if form.is_valid():
			answer:Answer = form.save(commit=False)
			answer.create_date = timezone.now()
			answer.question = question
			answer.author = request.user
			answer.save()
			return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id = question_id), answer.id))
	else:
		form = AnswerForm()
	context = {'question': question, 'form': form}
	return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request:HttpRequest, answer_id:int):
	answer:Answer = get_object_or_404(Answer, pk = answer_id)
	if answer.author != request.user:
		messages.error(request, '수정 권한이 없습니다.')
		return redirect('pybo:detail', question_id=answer.question.id)
	if request.method == 'POST':
		form = AnswerForm(request.POST, instance=answer)
		if form.is_valid():
			answer = form.save(commit=False)
			answer.modify_date = timezone.now()
			answer.save()
			return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))

	else:
		form = AnswerForm(instance=answer)
	context = {'form' : form}
	return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request:HttpRequest, answer_id:int):
	answer:Answer = get_object_or_404(Answer, pk=answer_id)
	if answer.author != request.user:
		messages.error(request, '삭제 권한이 없습니다.')
	else:
		answer.delete()
	return redirect('pybo:detail', question_id=answer.question.id)
