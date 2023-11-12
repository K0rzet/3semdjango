from django.db.models import Q
from django.utils.dateparse import parse_duration
from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

    @action(detail=False, methods=['get'])
    def filter_products(self, request):
        price_gt = self.request.query_params.get('price_gt')
        price_lt = self.request.query_params.get('price_lt')
        if price_gt is not None and price_lt is not None:
           queryset = Product.objects.filter(
               Q(price__gte=price_gt) & ~Q(price__gte=int(price_lt)-1) | Q(price=price_lt)
           )
           serializer = self.get_serializer(queryset, many=True)
           return Response(serializer.data)
        else:
            return self.list(request)

    @action(detail=False, methods=['get'])
    def available_products(self, request):
        manufacturing_time_max = parse_duration(self.request.query_params.get('manufacturing_time_max'))

        queryset = Product.objects.all()

        if manufacturing_time_max:
            queryset = queryset.filter(
                ~Q(manufacturing_time__gt=manufacturing_time_max) & Q(availability=True) | Q(stock_quantity__gt=0)
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    @authentication_classes([TokenAuthentication])
    def create_action(self, request, pk=None):
        product = self.get_object()
        user = self.request.user
        cart = get_object_or_404(Cart, user=user)
        new_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1,
            subtotal=product.price
        )

        serializer = CartItemSerializer(new_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartListView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CartItemListView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)