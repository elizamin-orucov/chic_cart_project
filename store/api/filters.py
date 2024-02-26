#                               Filter for products
import django_filters
from ..models import Product
from django.db.models import Q
from services.choices import RATING
from base.models import Category, Color
from services.choices import DISCOUNT_CHOICES


class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search")
    totalprice = django_filters.RangeFilter(label="total price range")
    rating = django_filters.ChoiceFilter(choices=RATING, label="rating")
    color = django_filters.ModelMultipleChoiceFilter(field_name="color", label="colors", queryset=Color.objects.all())
    category = django_filters.ModelChoiceFilter(field_name="category", queryset=Category.objects.all())
    discount_interest = django_filters.ChoiceFilter(field_name="discount_interest", choices=DISCOUNT_CHOICES)

    class Meta:
        model = Product
        fields = (
            "search",
            "totalprice",
            "rating",
            "color",
            "category",
            "discount_interest",
        )

    # changing the filter_queryset to return products that are descendants of the selected category.
    def filter_queryset(self, queryset):
        # first, we get the category values from the form so that the queryset does not come empty.
        category_value = self.form.cleaned_data.pop("category")
        # let's get the search value to search on both name and category__name.
        search = self.form.cleaned_data.pop("search")
        # we get a filtered query set suitable for other filters.
        queryset = super().filter_queryset(queryset)
        # we check that category_value is not empty.
        if category_value:
            # here we filter the products by selected category and parent.
            queryset = queryset.filter(category__in=category_value.get_descendants(include_self=True)).distinct()
        # we check that search value is not empty.
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(category__name__icontains=search)
            ).distinct()
        # we sort the filtered query set by -created_at.
        return queryset.order_by("-created_at")









