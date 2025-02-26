from django.urls import path,include
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers
from products.views import ProductViewSet,ReviewViewSet,CartViewSet,ProductTagListViewSet,FavoriteProductViewSet,ProductImageViewSet

router=routers.DefaultRouter()
router.register('products',ProductViewSet)
router.register('favorite_products',FavoriteProductViewSet)
router.register('reviews',ReviewViewSet)
router.register('cart',CartViewSet)
router.register('tags',ProductTagListViewSet)

Favorite_product_router=routers.NestedDefaultRouter(
    router,'favorite_products','favorite_product'
)

product_router=routers.NestedDefaultRouter(
    router,'products',lookup='product'
)
product_router.register('images',ProductImageViewSet)
product_router.register('reviews',ReviewViewSet)



urlpatterns = [
    path('',include(router.urls)),
    path('',include(product_router.urls)),
    # path('products/<int:product_id>/images/',ProductImageViewSet.as_view({"get":"list","post":"create"}),name='images'),
    # path('products/<int:product_id>/images/<int:pk>/',ProductImageViewSet.as_view({"get":"retrieve","delete":"destroy"}),name='image'),
    # path('products/<int:product_id>/reviews/', ReviewViewSet.as_view(), name="reviews"),
    # path('cart/',CartViewSet.as_view(),name='cart_view'),
    # path('tags/',ProductTagListView.as_view(),name='tags'),
    # path('favorite_products/',FavoriteProductViewSet.as_view({"get":"list","post":"create"}),name='favorite_products'),
    # path('favorite_products/<int:pk>/',FavoriteProductViewSet.as_view({"get":"retrieve","delete":"destroy"}),name='favorite_products')
    
    
]