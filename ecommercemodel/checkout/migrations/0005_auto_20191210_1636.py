# Generated by Django 2.2.5 on 2019-12-10 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_option',
            field=models.CharField(choices=[('deposito', 'Depósito em Conta'), ('boletobancario', 'Boleto Bancário'), ('pagseguro', 'PagSeguro'), ('paypal', 'PayPal')], default='deposito', max_length=30, verbose_name='Modo de Pagamento'),
        ),
    ]
