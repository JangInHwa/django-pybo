from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from pybo.models import Question
import logging

# logger = logging.getLogger('pybo')

def index(request:HttpRequest):
	# logger.info('INFO 레벨로 출력')
	page = request.GET.get('page', '1')
	question_list = Question.objects.order_by('-create_date')

	paginator = Paginator(question_list, 10)
	page_obj = paginator.get_page(page)
	context = {'question_list': page_obj}
	return render(request, 'pybo/question_list.html', context)

def detail(request, question_id:int):
	question = get_object_or_404(Question, pk=question_id)
	context = {'question':  question}
	return render(request, 'pybo/question_detail.html', context)
