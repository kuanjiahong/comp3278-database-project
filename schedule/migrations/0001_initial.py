# Generated by Django 4.1.2 on 2022-10-10 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=11)),
                ('name', models.CharField(max_length=100)),
                ('offered', models.BooleanField()),
                ('moodle_link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Teaching',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('T', 'Tutor'), ('L', 'Lecturer')], max_length=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.course')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.staff')),
            ],
        ),
        migrations.AddField(
            model_name='staff',
            name='courses',
            field=models.ManyToManyField(through='schedule.Teaching', to='schedule.course'),
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_id', models.IntegerField()),
                ('location', models.CharField(max_length=100)),
                ('class_day', models.CharField(choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], max_length=3)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('class_type', models.CharField(choices=[('T', 'Tutorial'), ('L', 'Lecture')], max_length=1)),
                ('zoom_link', models.URLField()),
                ('teacher_message', models.CharField(blank=True, max_length=1000)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.course')),
            ],
        ),
        migrations.AddConstraint(
            model_name='class',
            constraint=models.CheckConstraint(check=models.Q(('start_time__lt', models.F('end_time'))), name='valid_start_end_time'),
        ),
        migrations.AlterUniqueTogether(
            name='class',
            unique_together={('course', 'class_id')},
        ),
    ]
