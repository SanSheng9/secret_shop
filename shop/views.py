from django.db.models import Avg, Value, Case, When
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from shop.models import Product, UserProductRelation, UserProfile
from shop.permissions import IsOwnerProfileOrReadOnly, IsOwnerOrStaffOrReadOnly
from shop.serializers import ProductSerializer, UserSerializer, UserProductRelationSerializer
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

# Product
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().select_related('seller')
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['price']
    search_fields = ['name']
    ordering_fields = ['price', 'name']

    def perform_create(self, serializer):
        serializer.validated_data['seller'] = self.request.user
        serializer.save()


# Users
class UserListCreateView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# User relation
class UserProductsRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserProductRelation.objects.all()
    serializer_class = UserProductRelationSerializer
    lookup_field = 'product'

    def get_object(self):
        obj, _ = UserProductRelation.objects.get_or_create(user=self.request.user, product_id=self.kwargs['product'])
        return obj

