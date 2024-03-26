import django_filters 
from django_filters import CharFilter
from.models import Tab

class TabFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Tab
        fields = ['name']