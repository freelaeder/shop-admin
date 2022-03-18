from django.urls import path
from apps.book.views import *

urlpatterns = [
    # 获取所有book
    path('books/', BookListView.as_view()),
    # 针对单个book
    path('books/<int:id>', BookOneView.as_view()),
    # 人物
    path('peoples/<int:pid>', PeopleView.as_view()),
    # 练习 modelSerializer
    path('mbooks/', MbookView.as_view()),
    # 练习 APIView
    path('abooks/', AbookView.as_view()),
    # 练习GenericAPIView
    path('gbooks/', GbookView.as_view()),
]
