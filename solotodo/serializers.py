from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from solotodo.models import Language, Store, Currency, Country, StoreType, \
    Category, StoreUpdateLog, Entity, EntityHistory, Product, NumberFormat


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('url', 'email', 'first_name', 'last_name',
                  'preferred_language', 'preferred_country',
                  'preferred_currency', 'preferred_number_format',
                  'permissions')
        read_only_fields = ('email', 'first_name', 'last_name',
                            'permissions')


class StoreTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StoreType
        fields = ('url', 'name')


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ('url', 'code', 'name')


class NumberFormatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NumberFormat
        fields = ('url', 'name', 'thousands_separator', 'decimal_separator')


class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Currency
        fields = ('url', 'id', 'name', 'iso_code', 'decimal_places', 'prefix',
                  'exchange_rate', 'exchange_rate_last_updated')


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ('url', 'name', 'currency', 'number_format')


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Store
        fields = ('url', 'id', 'name', 'country', 'is_active', 'type',
                  'storescraper_class')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'id', 'name',)


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(read_only=True, source='__str__')

    class Meta:
        model = Product
        fields = ('url', 'id', 'name')


class StoreUpdatePricesSerializer(serializers.Serializer):
    discover_urls_concurrency = serializers.IntegerField(
        min_value=1,
        required=False
    )
    products_for_url_concurrency = serializers.IntegerField(
        min_value=1,
        required=False
    )
    queue = serializers.ChoiceField(
        choices=['us', 'cl'],
        required=False
    )
    async = serializers.BooleanField()
    categories = serializers.HyperlinkedRelatedField(
        view_name='category-detail',
        queryset=Category.objects.all(),
        many=True,
        required=False
    )

    def __init__(self, instance, data=empty, **kwargs):
        super(StoreUpdatePricesSerializer, self).__init__(None, data, **kwargs)
        scraper = instance.scraper
        self.fields['discover_urls_concurrency'].initial = \
            scraper.preferred_discover_urls_concurrency
        self.fields['products_for_url_concurrency'].initial = \
            scraper.preferred_products_for_url_concurrency
        self.fields['queue'].initial = scraper.preferred_queue
        self.fields['async'].initial = scraper.prefer_async
        valid_categories = instance.scraper_categories()
        self.fields['categories'].child_relation.queryset = \
            valid_categories
        self.fields['categories'].initial = [
            reverse('category-detail', kwargs={'pk': category.pk},
                    request=kwargs['context']['request'])
            for category in valid_categories]


class EntityHistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EntityHistory
        fields = ['entity', 'timestamp', 'stock', 'normal_price',
                  'offer_price', 'cell_monthly_payment']


class EntitySerializer(serializers.HyperlinkedModelSerializer):
    active_registry = EntityHistorySerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    cell_plan = ProductSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='entity-detail')
    external_url = serializers.URLField(source='url')

    class Meta:
        model = Entity
        fields = (
            'url',
            'id',
            'store',
            'category',
            'scraped_category',
            'currency',
            'product',
            'cell_plan',
            'active_registry',
            'name',
            'cell_plan_name',
            'part_number',
            'sku',
            'key',
            'external_url',
            'discovery_url',
            'description',
            'is_visible',
            'latest_association_user',
            'latest_association_date',
            'creation_date',
            'last_updated',
            'picture_url'
        )


class StoreUpdateLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StoreUpdateLog
        fields = ('url', 'store', 'categories', 'status', 'creation_date',
                  'last_updated', 'queue', 'discovery_url_concurrency',
                  'products_for_url_concurrency', 'use_async', 'registry_file',
                  'available_products_count', 'unavailable_products_count',
                  'discovery_urls_without_products_count')


class EntityEventValueSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(source='__str__')


class EntityEventUserSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        model = get_user_model()
        fields = ['url', 'id', 'full_name']
