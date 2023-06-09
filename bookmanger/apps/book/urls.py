from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.book.views import *

urlpatterns = [
    # 获取所有book
    path('books/', BookListView.as_view()),
    # 针对单个book
    path('books/<bname>', BookOneView.as_view()),
    # 人物
    path('peoples/<int:pid>', PeopleView.as_view()),
    # 练习 modelSerializer
    # 3 修改图书的添加  同时满足如下所有要求
    path('mbooks/', MbookView.as_view()),
    # 练习 APIView
    # 查询阅读量
    path('abooks/', AbookView.as_view()),
    # 练习GenericAPIView
    path('gbooks/', GbookView.as_view()),

]

# 创建路由对象  (最终使用)
router = DefaultRouter()
# 注册路由
# 2使用ModelViewSet完成图书和人物的增删改查
router.register(prefix=r'booksmodel', viewset=BookViewSet, basename='')
router.register(prefix=r'peosmodel', viewset=PeoViewSet, basename='')

# 把路由添加到urlpatterns
urlpatterns += router.urls
