import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.book.models import BookInfo, PeopleInfo
from apps.book.serializers import BookInfoSerializer, PeopleInfoSerializer


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
        # 获取所有数据
        data_dict = json.loads(request.body)
        print(data_dict)
        name = data_dict.get('name')
        pub_date = data_dict.get('pub_date')
        # 校验完整性
        if not all([name, pub_date]):
            return JsonResponse('err', safe=False)
        # 连接数据库
        try:
            # 如果该书名存在不添加
            count = BookInfo.objects.filter(name=name).count()
            if count:
                return JsonResponse('err', safe=False)
            book = BookInfo.objects.create(name=name, pub_date=pub_date)
        except Exception as e:
            return JsonResponse('err', safe=False)

        return JsonResponse(f'成功添加数据{book}', safe=False)


# 针对单个图书
class BookOneView(View):
    # 获取一条数据
    def get(self, request, id):
        # 连接数据库
        try:
            book = BookInfo.objects.get(id=id)
            print(f'book{book.id}')
            # 获取图书对应的人物
            peoples = book.people.all()
            print(f'peoples{peoples}')
            # 创建序列化对象 获取当前的图书
            bs = BookInfoSerializer(book)
            # 获取图书对应的人物 如果对应多个数据，添加many
            ps = PeopleInfoSerializer(peoples, many=True)
            # peoples = PeopleInfo.objects.filter(book=book.id)

            # print(peoples)
            # 组合数据
            data = bs.data
            data['peoples'] = ps.data
        except Exception as e:
            return JsonResponse('err', safe=False)

        # return JsonResponse({'id': book.id, 'name': book.name, 'pub_date': book.pub_date})
        return JsonResponse(data, safe=False)

    # 修改一条数据
    def put(self, request, id):
        # 获取参数
        data_dict = json.loads(request.body)
        print(data_dict)
        name = data_dict.get('name')
        pub_date = data_dict.get('pub_date')
        # 连接数据库，分情况更新
        try:
            if name:
                BookInfo.objects.filter(id=id).update(name=name)
            else:
                return JsonResponse('名字未更新', safe=False)
            if pub_date:
                BookInfo.objects.filter(id=id).update(pub_date=pub_date)
            else:
                return JsonResponse('日期未更新', safe=False)

            if name and pub_date:
                BookInfo.objects.filter(id=id).update(name=name, pub_date=pub_date)
            else:
                return JsonResponse('全部更新', safe=False)
        except Exception as e:
            return JsonResponse('err', safe=False)

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
            bs = BookInfo.objects.get(id=peoples.book_id)
            data = ps.data
            data['bookname'] = bs.name
        except Exception as e:
            print(e)
            return JsonResponse('err', safe=False)

        return JsonResponse(data)
