import django_filters
from .models import *


class PostFilterSet(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = {
            'caption': ['contains'],
            'date_created': ['exact', 'gte', 'lte']
        }
