from django_filters import FilterSet, CharFilter, OrderingFilter
from graphql_relay import from_global_id

from .models import Note


class NoteFilterSet(FilterSet):
    title__icontains = CharFilter(field_name="title", lookup_expr="icontains")

    order_by = OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("title", "title"),
        )
    )

    class Meta:
        model = Note
        fields = {
            "created_at": ["exact", "lt", "lte", "gt", "gte"],
        }

    # def filter_by_project_id(self, queryset, name, value):
    #     try:
    #         print("recibi un filtro de project_id ", value)
    #         decoded_id = from_global_id(value)[1]
    #         return queryset.filter(project__id=decoded_id)
    #     except Exception as e:
    #         print(e)
    #         return queryset.none()
