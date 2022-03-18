from rest_framework import serializers

from apps.book.models import BookInfo, PeopleInfo


class PeopleSerializer(serializers.Serializer):
    """英雄数据序列化器"""
    id = serializers.IntegerField(label='ID')
    name = serializers.CharField(label='名字')
    password = serializers.CharField(label='密码')
    description = serializers.CharField(label='描述信息')
    # book_id = serializers.IntegerField(label='书籍id')


# 准备书籍列表信息的模型类
class BookInfoSerializer(serializers.Serializer):
    # 创建图书序列化器
    id = serializers.IntegerField(label='ID', required=False)
    name = serializers.CharField(label='名称')
    pub_date = serializers.DateField(label='发布日期')
    # read_only 只可以读取到，不可以作为反序列化输入，通白来讲，该字段不可以修改
    readcount = serializers.IntegerField(label='阅读量')
    # write_only 只可以修改，不可以作为序列化输出，
    commentcount = serializers.IntegerField(label='评论量')

    # 注意要跟models中的外键保持一致
    people = PeopleSerializer(many=True, required=False)

    # 创建
    def create(self, validated_data):
        print(f'validated_data{validated_data}')
        return BookInfo.objects.create(**validated_data)

    # 更新
    def update(self, instance, validated_data):
        # instance 是原对象
        # validated_data 是更新的字典数据
        instance.name = validated_data.get('name', instance.name)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.readcount = validated_data.get('readcount', instance.readcount)
        instance.commentcount = validated_data.get('commentcount', instance.commentcount)
        instance.save()

        return instance

    # 校验阅读量
    # def validate_readcount(self, values):
    #     if values < 100:
    #         # 抛出异常
    #         raise serializers.ValidationError('阅读量不能小于100')
    #     return values

    # 所有参数的校验
    def validate(self, attrs):
        # attr 是所有的属性值
        readcount = attrs.get('readcount')
        commentcount = attrs.get('commentcount')
        if readcount < commentcount:
            raise serializers.ValidationError('阅读量不能小于评论量')
        return attrs


class PeopleInfoSerializer(serializers.Serializer):
    """英雄数据序列化器"""
    id = serializers.IntegerField(label='ID')
    name = serializers.CharField(label='名字')
    password = serializers.CharField(label='密码')
    description = serializers.CharField(label='描述信息')
    # book_id = serializers.IntegerField(label='书籍id')
    # 注意跟models保持一致，人物获取书用 book
    book = BookInfoSerializer()


# 人物
class PeopleModelSerializer(serializers.ModelSerializer):
    # book_id 用来替换 自动生成的readonly（）
    # 重写 会替换自动生成的
    book_id = serializers.IntegerField(required=False)
    book = serializers.StringRelatedField()

    class Meta:
        # 指定model 表
        model = PeopleInfo
        # 指定字段
        fields = ('id', 'book_id', 'book', 'name', 'password', 'is_delete', 'description')
        # 添加参数
        extra_kwargs = {
            'password': {'write_only': True},
            'is_delete': {'read_only': True}
        }


# 书籍
class BookModelSerializer(serializers.ModelSerializer):
    # 指定people 字段指向people表
    # people = PeopleModelSerializer(many=True)

    class Meta:
        # 指定模型类
        model = BookInfo
        # 获取所有字段
        # fields = '__all__'
        # 指定字段
        fields = ('id', 'name', 'readcount', 'commentcount', 'pub_date')
        # 排除字段
        # exclude = ('image', 'is_delete',)

        # 添加只读
        read_only_fields = ('readcount',)
        # 此方法执行不成功，改用下方
        # write_only_fields = ('commentcount',)
        extra_kwargs = {
            # 添加只写
            # 'commentcount': {'write_only': True}
        }

    def create(self, validated_data):
        # 获取参数
        print(f'validated_data{validated_data}')
        # 从数据中删除people
        peoples = validated_data.pop('people')
        print(f'peoples{peoples}')
        # 保存图书
        book = BookInfo.objects.create(**validated_data)
        # 保存人物
        for p in peoples:
            PeopleInfo.objects.create(book=book, **p)

        # 返回图书
        return book
