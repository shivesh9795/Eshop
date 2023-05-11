from django import template



register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(x,cart):
    keys=cart.keys()
    for id in keys:
        if int(id) == (x.id):
            return True
    return False
    

@register.filter(name='cart_quantity')
def cart_quantity(x,cart):
    keys=cart.keys()
    for id in keys:
        if int(id) == (x.id):
            return cart.get(id)
    return 0

@register.filter(name='price_total')
def price_total(x,cart):
    return x.price*cart_quantity(x,cart)


@register.filter(name='total_cart_price')   
def total_cart_price(products,cart):
    sum=0
    for p in products:
        print(p)
        sum += price_total(p,cart)
    return sum
