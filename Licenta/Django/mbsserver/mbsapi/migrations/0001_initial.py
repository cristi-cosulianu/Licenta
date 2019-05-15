# Generated by Django 2.2.1 on 2019-05-14 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=200)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(blank=True, default='', max_length=255)),
                ('price', models.FloatField(blank=True, default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentsStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, default='', max_length=20)),
                ('reason', models.CharField(blank=True, default='', max_length=255)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mbsapi.Payments')),
            ],
        ),
        migrations.AddField(
            model_name='payments',
            name='payer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mbsapi.Persons'),
        ),
        migrations.CreateModel(
            name='BillsToPayments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mbsapi.Bills')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mbsapi.Payments')),
            ],
        ),
        migrations.AddField(
            model_name='bills',
            name='initiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mbsapi.Persons'),
        ),
    ]
