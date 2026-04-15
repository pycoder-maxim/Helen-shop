from .models import Category, Wishlist

def categories(request):
    return {'categories': Category.objects.all()}

# Добавьте эту функцию:
def wishlist_count(request):
    if request.user.is_authenticated:
        return {'wishlist_count': Wishlist.objects.filter(user=request.user).count()}
    return {'wishlist_count': 0}