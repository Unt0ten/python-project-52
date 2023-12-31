# Generated by Django 4.2.7 on 2023-11-26 12:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('statuses', '0001_initial'),
        ('labels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': 'Task with such Name already exist.'}, help_text='Obligatory field.', max_length=255, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, help_text='Describe the task.', max_length=1000, null=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='author', to='users.person', verbose_name='Author')),
                ('executor', models.ForeignKey(blank=True, help_text='Select the task executor.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='executor', to='users.person', verbose_name='Executor')),
                ('labels', models.ManyToManyField(blank=True, help_text='Select one or more tags.', to='labels.labelmodel', verbose_name='Labels')),
                ('status', models.ForeignKey(help_text='Obligatory field. Select one of the task statuses.', on_delete=django.db.models.deletion.PROTECT, to='statuses.statusmodel', verbose_name='Status')),
            ],
        ),
    ]
