import json
import traceback

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.book.models import BookInfo, PeopleInfo
from apps.book.serializers import BookInfoSerializer, PeopleInfoSerializer, BookModelSerializer, PeopleModelSerializer


class BookListView(View):
    # 获取书籍所有数据
    def get(self, request):
        try:
            bookinfo = BookInfo.objects.all()
            print(f'bookinfo{bookinfo}')
            # 使用序列化器
            bs = BookInfoSerializer(bookinfo, many=True)
            print(f'bs.data{bs.data}')
        except Exception as e:
            print(e)
            JsonResponse({'code': 1, 'errmsg': 'err'})

        # book_list = []
        # for item in bookinfo:
        #     book_list.append({
        #         'id': item.id,
        #         'name': item.name,
        #         'pub_date': item.pub_date
        #     })
        # return JsonResponse(book_list, safe=False)

        return JsonResponse(bs.data, safe=False)

    # 添加一条数据
    def post(self, request):
        # # 获取所有数据
        # data_dict = json.loads(request.body)
        # print(data_dict)
        # name = data_dict.get('name')
        # pub_date = data_dict.get('pub_date')
        # # 校验完整性
        # if not all([name, pub_date]):
        #     return JsonResponse('err', safe=False)
        # # 连接数据库
        # try:
        #     # 如果该书名存在不添加
        #     count = BookInfo.objects.filter(name=name).count()
        #     if count:
        #         return JsonResponse('err', safe=False)
        #     book = BookInfo.objects.create(name=name, pub_date=pub_date)
        # except Exception as e:
        #     return JsonResponse('err', safe=False)

        # 使用序列化器
        # 准备数据
        data_dict = {
            "name": "6666",
            "pub_date": "2022-03-17",
            'readcount': 1,
            'commentcount': 20
        }
        # 创建序列化对象。把子典传进来
        # 反序列化更新
        bs = BookInfoSerializer(data=data_dict)
        # 验证
        # print(bs.is_valid())
        # print(bs.errors)
        try:
            # 抛出异常
            bs.is_valid(raise_exception=True)
            # 保存
            bs.save()

        except Exception as e:
            traceback.print_exc()
            print(e)
            return JsonResponse({'code': 400})

        return JsonResponse(f'成功添加数据', safe=False)


# 针对单个图书
class BookOneView(View):
    # 获取一条数据
    def get(self, request, id):
        # 连接数据库
        try:
            book = BookInfo.objects.get(id=id)
            print(f'book{book.id}')
            # 获取图书对应的人物
            # peoples = book.people.all()
            # print(f'peoples{peoples}')

            # 创建序列化对象 获取当前的图书
            bs = BookInfoSerializer(book)
            # 获取图书对应的人物 如果对应多个数据，添加many
            # ps = PeopleInfoSerializer(peoples, many=True)
            # peoples = PeopleInfo.objects.filter(book=book.id)

            # print(peoples)
            # 组合数据
            data = bs.data
            # data['peoples'] = ps.data
        except Exception as e:
            return JsonResponse('err', safe=False)

        # return JsonResponse({'id': book.id, 'name': book.name, 'pub_date': book.pub_date})
        return JsonResponse(data, safe=False)

    # 修改一条数据
    def put(self, request, id):
        # # 获取参数
        # data_dict = json.loads(request.body)
        # print(data_dict)
        # name = data_dict.get('name')
        # pub_date = data_dict.get('pub_date')
        # # 连接数据库，分情况更新
        # try:
        #     if name:
        #         BookInfo.objects.filter(id=id).update(name=name)
        #     else:
        #         return JsonResponse('名字未更新', safe=False)
        #     if pub_date:
        #         BookInfo.objects.filter(id=id).update(pub_date=pub_date)
        #     else:
        #         return JsonResponse('日期未更新', safe=False)
        #
        #     if name and pub_date:
        #         BookInfo.objects.filter(id=id).update(name=name, pub_date=pub_date)
        #     else:
        #         return JsonResponse('全部更新', safe=False)
        # except Exception as e:
        #     return JsonResponse('err', safe=False)

        # 使用反序列化更新数据
        bookid = BookInfo.objects.get(id=id)
        print(f'bookid{bookid}')
        data_dict = {
            "name": "99",
            "pub_date": "2022-03-17",
            'readcount': 22,
            'commentcount': 20
        }
        # 使用序列化器，把子典和要修改的书传递进来
        bs = BookInfoSerializer(bookid, data=data_dict)

        # 捕获异常
        try:
            bs.is_valid(raise_exception=True)
            # 保存
            bs.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400})

        return JsonResponse('ok', safe=False)

    # 删除一条数据
    def delete(self, request, id):
        try:
            # 如果没有传递id
            if not id:
                return JsonResponse('err', safe=False)
            BookInfo.objects.filter(id=id).delete()
        except Exception as e:
            print(e)
            return JsonResponse('err', safe=False)

        return JsonResponse('ok', safe=False)


class PeopleView(View):
    def get(self, request, pid):
        try:
            # 查找指定人物
            peoples = PeopleInfo.objects.get(id=pid)
            # 使用序列化器
            ps = PeopleInfoSerializer(peoples)
            # 根据人物获取图书
            # bs = BookInfo.objects.get(id=peoples.book_id)
            data = ps.data
            # data['bookname'] = bs.name
        except Exception as e:
            print(e)
            return JsonResponse('err', safe=False)

        return JsonResponse(data)


class MbookView(View):
    # 获取全部
    def get(self, request):
        # 使用Modelserializer
        books = BookInfo.objects.all()
        # 如果有多个查询集，使用 many
        mbs = BookModelSerializer(books, many=True)
        return JsonResponse(mbs.data, safe=False)

    # 添加一条
    def post(self, request):

        # data_dict = {
        #     'book_id': 6,
        #     'name': '靖哥哥111',
        #     'password': '123456abc',
        #     'description': '描述',
        #     'is_delete': 1
        # }

        # 注意保存多个数据时，记得添加many = True

        # data_dict = [
        #     {
        #         'book_id': 19,
        #         'name': '靖妹妹～～～',
        #         'password': '123456abc'
        #     },
        #     {
        #         'book_id': 19,
        #         'name': '靖表哥～～～',
        #         'password': '123456abc'
        #     }
        # ]

        data_dict = {
            'name': '离离原上草',
            'people': [
                {
                    'name': '靖妹妹111',
                    'password': '123456abc'
                },
                {
                    'name': '靖表哥222',
                    'password': '123456abc'
                }
            ]
        }
        # 添加书籍 需要改换书籍的序列化器·
        mbs = BookModelSerializer(data=data_dict)
        try:
            mbs.is_valid(raise_exception=True)
            mbs.save()
        except Exception as e:
            traceback.print_exc()
            print(e)
            return JsonResponse({'code': 400})

        return JsonResponse('ok', safe=False)


# 练习Apiview
class AbookView(APIView):
    def get(self, request):
        print(f'request.GET{request.GET}')
        print(f'request.query_params{request.query_params}')
        # 查询数据
        books = BookInfo.objects.all()
        # 创建序列化器，并传递查询结果
        bms = BookModelSerializer(books, many=True)
        # 返回结果

        return Response(bms.data)

    def post(self, request):
        # print(f'request.body{request.body}')
        # print(f'request.post{request.post}')
        # data_dict = json.loads(request.body)
        print(request.data)
        print(type(request.data))
        return Response({'name': 'freelaeder'}, status=status.HTTP_200_OK)


class GbookView(ListModelMixin, GenericAPIView):
    # 重写queryset 方法
    def get_queryset(self):
        return BookInfo.objects.all()

    # 或者添加属性名
    # queryset = BookInfo.objects.all()

    # 重写serializer 方法
    # def get_serializer_class(self):
    #     return BookModelSerializer

    # 或者添加属性名 值是需要使用的序列化器
    serializer_class = BookModelSerializer

    def get(self, request):
        # 查询搜有的图书
        # books = self.get_queryset()
        # 创建序列化器，传递查询集 ，注意添加many =True
        # bms = self.get_serializer(books, many=True)

        # return Response(data=bms.data, status=status.HTTP_200_OK)
        return self.list(request)
