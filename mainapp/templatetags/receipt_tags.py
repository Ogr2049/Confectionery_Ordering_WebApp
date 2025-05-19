from django import template
from mainapp import models

register = template.Library()

@register.simple_tag()
def is_like(request, receipt_id):
    receipt = models.Receipt.objects.get(id=receipt_id)
    for like in receipt.likes.all():
        if like.user == request.user:
            return True
    return False