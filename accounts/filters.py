import django_filters 
from django_filters import DateFilter

from .models import *
# similar to how you set the model form
class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = '__all__'
