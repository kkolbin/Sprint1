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

    # Метод для создания новой записи
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
            # В случае ошибки сервера
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Ошибка при выполнении операции',
                    'id': None
                }
            )
        else:
            # В случае невалидных данных
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Сервер не смог обработать некоторые поля',
                    'id': None
                }
            )

    # Метод для обновления записи
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
                # В случае ошибок валидации
                return Response(
                    {'state': '0',
                     'message': serializer.errors
                     }
                )
        else:
            # В случае, если статус не "новый"
            return Response(
                {'state': '0',
                 'message': f'При статусе: {pass_instance.get_status_display()}, редактирование невозможно.'
                 }
            )


# API view для получения данных по email
class EmailView(generics.ListAPIView):
    serializer_class = PassSerializer

    def get(self, request, *args, **kwargs):
        email = kwargs.get('email', None)
        if Pass.objects.filter(user__email=email).exists():
            # Если пользователь существует
            data = PassSerializer(
                Pass.objects.filter
                (
                    user__email=email
                ),
                many=True
            ).data
        else:
            # Если пользователя нет
            data = {'message': f'Пользователь с {email} не найден'}
        return JsonResponse(data, safe=False)
