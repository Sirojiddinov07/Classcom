from django.db import models


class OrderNumberService:
    @staticmethod
    def update_order_numbers(instance, order_field_name="order_number"):
        model = instance.__class__
        order_number = getattr(instance, order_field_name)

        if not instance.pk:
            if order_number is None:
                max_order_number = (
                    model.objects.aggregate(models.Max(order_field_name))[
                        f"{order_field_name}__max"
                    ]
                    or 0
                )
                setattr(instance, order_field_name, max_order_number + 1)
            else:
                model.objects.filter(
                    **{f"{order_field_name}__gte": order_number}
                ).update(**{order_field_name: models.F(order_field_name) + 1})
        else:
            old_instance = model.objects.get(pk=instance.pk)
            old_order_number = getattr(old_instance, order_field_name)

            if order_number is not None and old_order_number is not None:
                if order_number < old_order_number:
                    model.objects.filter(
                        **{
                            f"{order_field_name}__gte": order_number,
                            f"{order_field_name}__lt": old_order_number,
                        }
                    ).update(
                        **{order_field_name: models.F(order_field_name) + 1}
                    )
                else:
                    model.objects.filter(
                        **{
                            f"{order_field_name}__gt": old_order_number,
                            f"{order_field_name}__lte": order_number,
                        }
                    ).update(
                        **{order_field_name: models.F(order_field_name) - 1}
                    )

        # Remove instance.save() to avoid recursion
