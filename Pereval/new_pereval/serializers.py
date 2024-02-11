from rest_framework import serializers
from .models import Users, Coords, Levels, PassImages, Pass
from drf_writable_nested import WritableNestedModelSerializer


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'fam', 'name', 'otc', 'phone']
        verbose_name = 'Турист'

    def save(self, **kwargs):
        self.is_valid()
        user = Users.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            new_user = Users.objects.create(
                email=self.validated_data.get('email'),
                phone=self.validated_data.get('phone'),
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
            )
            return new_user


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']
        verbose_name = 'Координаты'


class LevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = ['spring', 'summer', 'autumn', 'winter']
        verbose_name = 'Уровень сложности'


class PassImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PassImages
        fields = ['image_id']
        verbose_name = 'Фотография(и)'


class PassSerializer(WritableNestedModelSerializer):
    user = UsersSerializer()
    date_added = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    coords = CoordsSerializer()
    level = LevelsSerializer()
    images = PassImagesSerializer()

    class Meta:
        model = Pass
        fields = [
            'id', 'status', 'user', 'date_added', 'coords', 'level',
            'beauty_title', 'title', 'other_titles', 'connect', 'images'
        ]
        read_only_fields = ['status']
        filterset_fields = ['user__email']
        verbose_name = 'Перевал'

    def validate(self, data):
        if self.instance is not None:
            turist = self.instance.user
            data_turist = data.get('user')

            # Check if data_turist is not None before using it
            if data_turist is not None and turist != UsersSerializer(data_turist).data:
                raise serializers.ValidationError(
                    {'non_field_errors': ['E-mail, ФИО и номер телефона изменить нельзя!']}
                )

            # Simplified validation using a list of fields to check
            validating_fields = [
                turist.email, turist.fam, turist.name, turist.otc, turist.phone
            ]
            if data_turist is not None and any(data_turist[field] != value for field, value in zip(UsersSerializer.Meta.fields[1:], validating_fields)):
                raise serializers.ValidationError(
                    {'non_field_errors': ['E-mail, ФИО и номер телефона изменить нельзя!']}
                )

        return data
