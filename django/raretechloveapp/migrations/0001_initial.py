# Generated by Django 3.2.7 on 2021-09-10 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleMST',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_url', models.URLField()),
                ('category', models.CharField(choices=[('PC操作', 'PC操作'), ('Network', 'Network'), ('Web', 'Web'), ('Linux', 'Linux'), ('プログラミング', 'プログラミング')], max_length=255, verbose_name='カテゴリ')),
            ],
        ),
        migrations.CreateModel(
            name='UserMST',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255)),
                ('pw', models.CharField(max_length=255)),
                ('slack_name', models.CharField(max_length=255)),
                ('spread_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='QuestionTBL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_cd', models.DateTimeField(blank=True, null=True)),
                ('question_thread', models.TextField()),
                ('ts', models.DateTimeField()),
                ('qa_dist', models.BooleanField()),
                ('article_cd', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='raretechloveapp.articlemst')),
                ('user_cd', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='raretechloveapp.usermst')),
            ],
        ),
        migrations.CreateModel(
            name='QcountTBL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_count', models.IntegerField()),
                ('answer_count', models.IntegerField()),
                ('user_cd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='raretechloveapp.usermst')),
            ],
        ),
        migrations.CreateModel(
            name='DifficultyTBL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total1', models.IntegerField()),
                ('answer1', models.IntegerField()),
                ('ave1', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total2', models.IntegerField()),
                ('answer2', models.IntegerField()),
                ('ave2', models.DecimalField(decimal_places=2, max_digits=5)),
                ('article_cd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='raretechloveapp.articlemst')),
            ],
        ),
    ]
