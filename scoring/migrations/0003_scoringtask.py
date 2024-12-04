# Generated by Django 4.2.5 on 2024-12-03 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0002_alter_questionanswer_options_questionanswer_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScoringTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified.', verbose_name='modified at')),
                ('deleted', models.BooleanField(default=False, help_text='Set to False when an element is deleted')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('result', models.JSONField(blank=True, null=True)),
                ('query', models.TextField()),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
