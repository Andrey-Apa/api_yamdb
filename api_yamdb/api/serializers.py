from rest_framework import serializers

from django.core.validators import MaxValueValidator, MinValueValidator

from reviews.models import Review, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(1, 'Оценка не может быть меньше 1!'),
            MaxValueValidator(10, 'Оценка не может быть больше 10!'),
        )
    )
    
    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date')
    
    def validate(self, data):
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if (self.context['request'].method == 'POST' and
            Review.objects.filter(author=user, title=title_id).exists()):
                raise serializers.ValidationError(
                    'Вы уже оставили свой отзыв на это произведение!'
                )
        return data
