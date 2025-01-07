from django_filters.rest_framework import FilterSet
from .models import Sale


class IncomeInDateRangeFilter(FilterSet):

    class Meta:
        Model = Sale
        fields = {
            'datetime': {'lt', 'gt'}
        }
