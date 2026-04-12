from rest_framework import serializers
from django.contrib.auth import get_user_model

#get_user_model returns the model that is active in this project

User = get_user_model()   # -> type[AbstractUser]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","full_name","email","password"]

        extra_kwargs = {
            'password' : {'write_only': True}
        }

    def create(self,validated_data):
        password = validated_data.pop("password",None)
        instance = User(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


