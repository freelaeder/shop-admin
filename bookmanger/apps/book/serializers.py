from rest_framework import serializers


# 准备书籍列表信息的模型类
class BookInfoSerializer(serializers.Serializer):
    # 创建图书序列化器
    id = serializers.IntegerField(label='ID')
    name = serializers.CharField(label='名称')
    pub_date = serializers.DateField(label='发布日期')
    readcount = serializers.IntegerField(label='阅读量')
    commentcount = serializers.IntegerField(label='评论量')


class PeopleInfoSerializer(serializers.Serializer):
    """英雄数据序列化器"""
    id = serializers.IntegerField(label='ID')
    name = serializers.CharField(label='名字')
    password = serializers.CharField(label='密码')
    description = serializers.CharField(label='描述信息')
    book_id = serializers.IntegerField(label='书籍id')
