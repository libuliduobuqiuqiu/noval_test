# coding=utf-8
from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import linecache
import chardet
import codecs
import time
import os


def index(request):
    return render_to_response('index.html',{'objects': book_list()})


def book_update(request):
    #   异步更新上传文件列表
    if request.method == 'GET':
        return JsonResponse({x: v for x,v in enumerate(book_list())})


def book_read(request):
    #   获取上传书籍的内容
    if request.method == 'GET':
        book_name = request.GET['book_name']            # 书籍名称
        file_path = "static/books/" + book_name         # 书籍路径

        with open(file_path,encoding='gbk', errors='ignore') as f:
            book_contents = f.readlines()

        paginator = Paginator(book_contents, 50)
        try:
            page = int(request.GET['page'])  # 页码
            book_content = paginator.page(page)
        except Exception as e:
            book_content = paginator.page(1)
        return render_to_response('book.html',{'book_content': book_content, 'book_name': book_name})


def book_del(request):
    #   删除已上传的书籍文件
    if request.method == 'GET':
        book_name = request.GET['book_name']
        file_path = "static/books/" + book_name

        if os.path.exists(file_path):
            os.remove(file_path)
    return HttpResponseRedirect('/index/')


def file_receive(request):
    #   接收File-Input空间传送的文件
    if request.method == 'POST':
        file = request.FILES['input-b8']
        file_path = "static/books/"+file.name
        with open(file_path,"wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
    return JsonResponse({'status':'success'})


def book_list():
    #   获取books目录下的书籍
    file_list = []
    filedir_path = "static/books/"
    list_file = os.listdir(filedir_path)
    for book in list_file:
        book_info = {}
        book_path = filedir_path + book

        book_info['name'] = book
        book_info['timestamp'] = os.path.getctime(book_path)
        book_info['book_time'] = time_format(book_info['timestamp'])
        book_info['book_size'] = os.path.getsize(book_path)
        file_list.append(book_info)
    books = sorted(file_list,key= lambda x:x['timestamp'],reverse=True)
    return books


def time_format(timestamp):
    #   格式化时间戳成指定的时间
    time_struct = time.localtime(timestamp)
    time_string = time.strftime('%Y-%m-%d %H:%M',time_struct)
    return time_string
