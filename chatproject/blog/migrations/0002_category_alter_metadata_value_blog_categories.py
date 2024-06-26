# Generated by Django 4.2.13 on 2024-06-07 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='metadata',
            name='value',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='blog',
            name='categories',
            field=models.ManyToManyField(to='blog.category'),
        ),
    ]
