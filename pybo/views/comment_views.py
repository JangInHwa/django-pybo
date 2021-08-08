from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.http import HttpRequest, HttpResponse

from pybo.forms import CommentForm
from pybo.models import Question, Answer, Comment

def comment_modify(request:HttpRequest, comment:Comment, question_id) -> HttpResponse:
	if request.user != comment.author:
		messages.error(request, '댓글 수정 권한이 없습니다.!')
		return redirect('pybo:detail', question_id =question_id)
	if request.method == 'POST':
		form = CommentForm(request.POST, instance=comment)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.modify_date = timezone.now()
			comment.save()
			return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=question_id), comment.id))
	else:
		form = CommentForm(instance=comment)
	context = {'form' : form}
	return render(request, 'pybo/comment_form.html', context)

def comment_delete(request:HttpRequest, comment:Comment, question_id):
	if request.user != comment.author:
		messages.error(request, '댓글 삭제 권한이 없습니다')
	else:
		comment.delete()
	return redirect('pybo:detail', question_id = question_id)

@login_required(login_url='common:login')
def comment_create_question(request:HttpRequest, question_id):
	question = get_object_or_404(Question, pk = question_id)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment:Comment = form.save(commit=False)
			comment.author = request.user
			comment.create_date = timezone.now()
			comment.question = question
			comment.save()
			return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=question_id), comment.id))
	else:
		form = CommentForm()
	context = {'form':form}
	return render(request, 'pybo/comment_form.html', context)



@login_required(login_url='common:login')
def comment_modify_question(request:HttpRequest, comment_id):
	comment:Comment = get_object_or_404(Comment, pk = comment_id)
	return comment_modify(request, comment, comment.question.id)

@login_required(login_url='common:login')
def comment_delete_question(request:HttpRequest, comment_id):
	comment:Comment = get_object_or_404(Comment, pk = comment_id)
	return comment_delete(request, comment, comment.question.id)

@login_required(login_url='common:login')
def comment_create_answer(request:HttpRequest, answer_id):
	answer:Answer = get_object_or_404(Answer, pk = answer_id)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment:Comment = form.save(commit=False)
			comment.author = request.user
			comment.answer = answer
			comment.create_date = timezone.now()
			comment.save()
			return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), comment.id))
	else:
		form = CommentForm()
	context = {'form' : form}
	return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
	comment:Comment = get_object_or_404(Comment, pk = comment_id)
	return comment_modify(request, comment, comment.answer.question.id)

@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
	comment:Comment = get_object_or_404(Comment, pk = comment_id)
	return comment_delete(request, comment, comment.answer.question.id)

