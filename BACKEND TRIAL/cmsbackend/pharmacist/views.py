# cmsbackend/pharmacist/views.py
from rest_framework import viewsets
from .models import Medicine, MedicineBatch, Dispense, DispenseItem, MedicineBill
from .serializers import MedicineSerializer, MedicineBatchSerializer, DispenseSerializer, DispenseItemSerializer, MedicineBillSerializer
from rest_framework.response import Response
from rest_framework import status
# class MedicineViewSet(viewsets.ModelViewSet):
#     queryset = Medicine.objects.all()
#     serializer_class = MedicineSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Medicine
from .serializers import MedicineSerializer


class MedicineViewSet(ModelViewSet):

    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Medicine added successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Medicine updated successfully",
                "data": serializer.data
            }
        )

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.delete()

        return Response(
            {"message": "Medicine deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

# class MedicineBatchViewSet(viewsets.ModelViewSet):
#     queryset = MedicineBatch.objects.all()
#     serializer_class = MedicineBatchSerializer
class MedicineBatchViewSet(ModelViewSet):

    queryset = MedicineBatch.objects.all()
    serializer_class = MedicineBatchSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Medicine batch added successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

# class DispenseViewSet(viewsets.ModelViewSet):
#     queryset = Dispense.objects.all()
#     serializer_class = DispenseSerializer

# class DispenseItemViewSet(viewsets.ModelViewSet):
#     queryset = DispenseItem.objects.all()
#     serializer_class = DispenseItemSerializer
class DispenseViewSet(ModelViewSet):

    queryset = Dispense.objects.all()
    serializer_class = DispenseSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dispense = serializer.save()

        return Response(
            {
                "message": "Medicine dispensed successfully",
                "data": DispenseSerializer(dispense).data
            },
            status=status.HTTP_201_CREATED
        )

# class MedicineBillViewSet(viewsets.ModelViewSet):
#     queryset = MedicineBill.objects.all()
#     serializer_class = MedicineBillSerializer
class MedicineBillViewSet(ModelViewSet):

    queryset = MedicineBill.objects.all()
    serializer_class = MedicineBillSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Medicine bill created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
