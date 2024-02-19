import django_filters
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import *
from .models import *


# ViewSet для модели Users
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


# ViewSet для модели Coords
class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


# ViewSet для модели Levels
class LevelsViewSet(viewsets.ModelViewSet):
    queryset = Levels.objects.all()
    serializer_class = LevelsSerializer


# ViewSet для модели PassImages
class PassImageViewSet(viewsets.ModelViewSet):
    queryset = PassImages.objects.all()
    serializer_class = PassImagesSerializer


# ViewSet для модели Pass
class PassViewSet(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('user__email',)

    def create(self, request, *args, **kwargs):
        serializer = PassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Успех',
                    'id': serializer.data['id']
                }
            )
        elif status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Ошибка при выполнении операции',
                    'id': None
                }
            )
        else:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Сервер не смог обработать некоторые поля',
                    'id': None
                }
            )

    def update(self, request, *args, **kwargs):
        pass_instance = self.get_object()
        if pass_instance.status == 'NW':
            serializer = PassSerializer(
                pass_instance,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {'state': '1',
                     'message': 'Данные изменены'
                     }
                )
            else:
                return Response(
                    {'state': '0',
                     'message': serializer.errors
                     }
                )
        else:
            return Response(
                {'state': '0',
                 'message': f'При статусе: {pass_instance.get_status_display()}, редактирование невозможно.'
                 }
            )

    # Добавление метода GET для получения одной записи по её id
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Добавление метода PATCH для редактирования записи по её id
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == 'NW':
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'state': '1', 'message': 'Данные изменены'})
            else:
                return Response({'state': '0', 'message': serializer.errors})
        else:
            return Response({'state': '0', 'message': f'При статусе: {instance.get_status_display()}, редактирование невозможно.'})


class EmailView(generics.ListAPIView):
    serializer_class = PassSerializer

    def get(self, request, *args, **kwargs):
        email = kwargs.get('email', None)
        if Pass.objects.filter(user__email=email).exists():
            data = PassSerializer(
                Pass.objects.filter
                (
                    user__email=email
                ),
                many=True
            ).data
        else:
            data = {'message': f'Пользователь с {email} не найден'}
        return JsonResponse(data, safe=False)

