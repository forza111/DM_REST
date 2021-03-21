from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from .models import Movie


class PaginationMovies(PageNumberPagination):
    page_size = 1
    max_page_size = 1000

def get_client_ip(request):
    '''Получение IP пользователя'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    '''указываем CharFilter для того, чтобы мы искали по имени ( по умолчанию
    она по id'''
    pass


class MovieFilter(filters.FilterSet):
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')#in - вхождение
    year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['genres', 'year']