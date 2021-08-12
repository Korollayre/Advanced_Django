from django.db import models
from users.models import User
from products.models import Product


# class BasketQuerySet(models.QuerySet):
#
#     def delete(self):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super().delete()


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def total_quantity(self):
        basket = Basket.objects.filter(user=self.user)
        return sum(el.quantity for el in basket)

    def total_sum(self):
        basket = Basket.objects.filter(user=self.user)
        return sum(el.sum() for el in basket)

    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete()

