from django.shortcuts import render

from rest_framework import generics
from .models import Caller, CallDetails
from .serializers import UserDataSerializer, CDRSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime

user_file = "user_details.txt"
cdr_file = "call_detail_records.txt"


def load_user_data(request):
    """
    Loads user data from a text file and adds it to a Django model.
    Args:
        file_path (str): The path to the text file.
    """
    with open(user_file, 'r') as file:
        for line in file:
            data = [field.strip() for field in line.strip().split(',')]
            obj = Caller(*data)
            obj.save()


def load_cdr_data(request):
    """
    Loads cdr data from a text file and adds it to a Django model.
    Args:
        file_path (str): The path to the text file.
    """
    with open(cdr_file, 'r') as file:
        next(file)
        for line in file:
            data = [field.strip() for field in line.strip().split(',')]
            obj = CallDetails(*data)
            obj.save()


class UserDataByName(generics.ListAPIView):
    serializer_class = UserDataSerializer

    def get_queryset(self):
        user_name = self.kwargs['user_name']
        try:
            user = Caller.objects.get(user_name=user_name)
            phone_no = user.phone_number
            call_details = CallDetails.objects.filter(caller=phone_no)
            serializer = CDRSerializer(call_details, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)


class UserDataByNameAndDate(generics.ListAPIView):
    serializer_class = UserDataSerializer

    def get_queryset(self):
        user_name = self.kwargs.get('user_name')
        date = self.kwargs.get('date')
        if user_name and date:
            try:
                user = Caller.objects.get(user_name=user_name)
                phone_no = user.phone_number
                call_details = CallDetails.objects.filter(caller=phone_no, date=date)
                serializer = CDRSerializer(call_details, many=True)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)


class UserDataByDateRange(generics.ListAPIView):
    serializer_class = UserDataSerializer

    def get_queryset(self):
        user_name = self.kwargs.get('user_name')
        from_date_str = self.kwargs.get('from_date')
        to_date_str = self.kwargs.get('to_date')
        from_date = datetime.strptime(from_date_str, '%d-%m-%Y').date()
        to_date = datetime.strptime(to_date_str, '%d-%m-%Y').date()

        if user_name and from_date and to_date:
            try:
                user = Caller.objects.get(user_name=user_name)
                phone_no = user.phone_number
                call_details = CallDetails.objects.filter(
                    Q(caller=phone_no) & Q(date__range=[from_date, to_date])
                )
                serializer = CDRSerializer(call_details, many=True)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)



