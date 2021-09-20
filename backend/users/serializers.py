from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from recipes.serializers import ShowRecipeLightSerializer
from .models import Follow


User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class UserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.follower.filter(user=obj, following=request.user).exists()


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Email')
    password = serializers.CharField(label='Password')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Неверные учетные данные.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Запрос должен содержать email и пароль.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following')

    # def validate(self, data):
    #     user = self.context.get('request').user
    #     following_id = data['following'].id

        # if self.context.get('request').method == 'GET':
        #     if Follow.objects.filter(user=user,
        #                              following__id=following_id).exists():
        #         raise serializers.ValidationError(
        #             'Вы уже подписаны на этого пользователя')
        #     if user.id == following_id:
        #         raise serializers.ValidationError('Нельзя подписаться на себя')

        # if (self.context.get('request').method == 'DELETE' and not
        #         Follow.objects.filter(user=user,
        #                               following__id=following_id).exists()):
        #     raise serializers.ValidationError(
        #         'Вы не были подписаны на этого пользователя')
        # return data


class ShowFollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = fields

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.follower.filter(user=obj, following=request.user).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            recipes = obj.recipes.all()[:(int(recipes_limit))]
        else:
            recipes = obj.recipes.all()
        context = {'request': request}
        return ShowRecipeLightSerializer(recipes, many=True,
                                         context=context).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
