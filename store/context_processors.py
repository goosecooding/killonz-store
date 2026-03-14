def cart_count(request):
    cart = request.session.get('cart', {})
    return {'cart_count': sum(cart.values())}

from django.utils.translation import get_language

def language_context(request):
    return {'current_lang': get_language()}
