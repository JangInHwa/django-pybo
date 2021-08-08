from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpRequest

from pybo.forms import QuestionForm
from pybo.models import Question


@login_required(login_url='common:login')
def question_create(request: HttpRequest):
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			question:Question = form.save(commit=False)
			question.create_date = timezone.now()
			question.author = request.user
			question.save()
			return redirect('pybo:index')
	else:
		form = QuestionForm()
	context = {'form': form}
	return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request:HttpRequest, question_id:int):
	question:Question = get_object_or_404(Question, pk = question_id)
	if request.user != question.author:
		messages.error(request, '수정 권한이 없습니다')
		return redirect('pybo:detail', question_id = question_id)

	if request.method == 'POST':
		form = QuestionForm(request.POST, instance=question)
		if form.is_valid():
			question = form.save(commit=False)
			question.modify_date = timezone.now()
			question.save()
			return redirect('pybo:detail', question_id=question.id)
	else:
		form = QuestionForm(instance=question)
	context = {'form':form}
	return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request:HttpRequest, question_id:int):
	question:Question = get_object_or_404(Question, pk=question_id)
	if request.user != question.author:
		messages.error(request, '삭제 권한이 없습니다')
	else:
		question.delete()
	return redirect('pybo:index')
