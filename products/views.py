from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView,ListAPIView,ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from products.models import Product,Review,Cart,ProductTag,FavoriteProduct,ProductImage
from products.serializers import ProductSerializer,ReviewSerializer,CartSerializer,ProductTagSerializer,ProductImageSerializer,FavoriteProductSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class ProductViewSet(ListModelMixin,CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[IsAuthenticated]
   
    
class ReviewViewSet(ListModelMixin,CreateModelMixin,GenericViewSet):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_pk'])

class CartViewSet(ListModelMixin,CreateModelMixin,GenericViewSet):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer
    permission_clases=[IsAuthenticated]
    
    def get_queryset(self):
        queryset=self.queryset.filter(user=self.request.user)
        return queryset
    
    
class ProductTagListViewSet(ListModelMixin,GenericViewSet):
    queryset=ProductTag.objects.all()
    serializer_class=ProductTagSerializer
    permission_classes=[IsAuthenticated]
    
class FavoriteProductViewSet(ListModelMixin,RetrieveModelMixin,DestroyModelMixin,CreateModelMixin,GenericViewSet):
    queryset=FavoriteProduct.objects.all()
    serializer_class=FavoriteProductSerializer
    permission_clases=[IsAuthenticated]
    
    def get_queryset(self):
        queryset=self.queryset.filter(user=self.request.user)
        return queryset
    
class ProductImageViewSet(ListModelMixin,RetrieveModelMixin,DestroyModelMixin,CreateModelMixin,GenericViewSet):
    queryset=ProductImage.objects.all()
    serializer_class=ProductImageSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(product__id=self.kwargs['product_pk'])