# Generated by Django 2.2.5 on 2019-12-17 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0014_auto_20191217_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('1', 'Aguardando Pagamento'), ('2', 'Pagamento em Análise'), ('3', 'Pagamento Autorizado'), ('7', 'Cancelado')], default=None, max_length=30, null=True, verbose_name='Situação'),
        ),
    ]
