# Generated by Django 2.2.5 on 2022-03-16 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('pub_date', models.DateField(null=True, verbose_name='发布日期')),
                ('readcount', models.IntegerField(default=0, verbose_name='阅读量')),
                ('commentcount', models.IntegerField(default=0, verbose_name='评论量')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('image', models.ImageField(null=True, upload_to='book', verbose_name='图片')),
            ],
            options={
                'verbose_name': '图书',
                'db_table': 'bookinfo',
            },
        ),
        migrations.CreateModel(
            name='PeopleInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('description', models.CharField(max_length=200, null=True, verbose_name='描述信息')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='people', to='book.BookInfo', verbose_name='图书')),
            ],
            options={
                'verbose_name': '人物信息',
                'db_table': 'peopleinfo',
            },
        ),
    ]
