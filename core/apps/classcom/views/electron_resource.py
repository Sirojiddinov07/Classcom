from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.classcom.models.electron_resource import (
    ElectronResource,
    ElectronResourceCategory,
    ElectronResourceSubCategory,
)
from core.apps.classcom.serializers.electron_resource import (
    ElectronResourceCategorySerializer,
    ElectronResourceSerializer,
    ElectronResourceSubCategorySerializer,
)
from core.apps.classcom.views import CustomPagination


class ElectronResourceCategoryView(APIView):
    serializer_class = ElectronResourceCategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        search = request.query_params.get("search")
        queryset = ElectronResourceCategory.objects.filter(is_active=True)
        if search:
            search_terms = search[:100].split()
            query = Q()
            for term in search_terms:
                query &= Q(name__icontains=term) | Q(
                    description__icontains=term
                )
            queryset = queryset.filter(query)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElectronResourceCategoryDetailView(APIView):
    serializer_class = ElectronResourceCategorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        category = ElectronResourceCategory.objects.get(pk=pk)
        serializer = self.serializer_class(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = ElectronResourceCategory.objects.get(pk=pk)
        serializer = self.serializer_class(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = ElectronResourceCategory.objects.get(pk=pk)
        category.is_active = False
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ElectronResourceSubCategoryView(APIView):
    serializer_class = ElectronResourceSubCategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        queryset = ElectronResourceSubCategory.objects.filter(is_active=True)
        search = request.query_params.get("search")
        category = request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)
        if search:
            search_terms = search[:100].split()
            query = Q()
            for term in search_terms:
                query &= Q(name__icontains=term) | Q(
                    description__icontains=term
                )
            queryset = queryset.filter(query)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElectronResourceSubCategoryDetailView(APIView):
    serializer_class = ElectronResourceSubCategorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        sub_category = ElectronResourceSubCategory.objects.get(pk=pk)
        serializer = self.serializer_class(sub_category)
        return Response(serializer.data)

    def put(self, request, pk):
        sub_category = ElectronResourceSubCategory.objects.get(pk=pk)
        serializer = self.serializer_class(sub_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        sub_category = ElectronResourceSubCategory.objects.get(pk=pk)
        sub_category.is_active = False
        sub_category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ElectronResourceView(APIView):
    serializer_class = ElectronResourceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        queryset = ElectronResource.objects.filter(is_active=True)
        search = request.query_params.get("search")
        category = request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)
        if search:
            search_terms = search[:100].split()
            query = Q()
            for term in search_terms:
                query &= Q(name__icontains=term) | Q(
                    description__icontains=term
                )
            queryset = queryset.filter(query)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElectronResourceDetailView(APIView):
    serializer_class = ElectronResourceSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        resource = ElectronResource.objects.get(pk=pk)
        serializer = self.serializer_class(resource)
        return Response(serializer.data)

    def put(self, request, pk):
        resource = ElectronResource.objects.get(pk=pk)
        serializer = self.serializer_class(resource, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        resource = ElectronResource.objects.get(pk=pk)
        resource.is_active = False
        resource.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
