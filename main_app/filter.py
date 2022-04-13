from .models import Quote, Source
import django_filters


class QuoteFilter(django_filters.FilterSet):
    content = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Quote
        fields = ["content", "sources", "user"]


class SourceFilter(django_filters.FilterSet):
    quoter = django_filters.CharFilter(lookup_expr="icontains")
    origin = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Source
        fields = ["quoter", "origin"]
