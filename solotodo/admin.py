from custom_user.admin import EmailUserAdmin
from django.contrib import admin

# Register your models here.
from guardian.admin import GuardedModelAdmin

from solotodo.models import Currency, Entity, EntityHistory, ProductType, \
    SoloTodoUser, Store, Country, Product, StoreUpdateLog, Language, \
    StoreType, ProductTypeTier, NumberFormat, EntityLog

admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Currency)
admin.site.register(NumberFormat)


class EntityModelAdmin(admin.ModelAdmin):
    readonly_fields = ['store', 'product_type', 'scraped_product_type',
                       'currency', 'product', 'cell_plan', 'active_registry',
                       'latest_association_user']

admin.site.register(Entity, EntityModelAdmin)


class EntityLogModelAdmin(admin.ModelAdmin):
    readonly_fields = ['entity', 'product_type', 'scraped_product_type',
                       'currency', 'product', 'cell_plan', 'user']

    def get_queryset(self, request):
        return EntityLog.objects.select_related()

admin.site.register(EntityLog, EntityLogModelAdmin)


class EntityHistoryModelAdmin(admin.ModelAdmin):
    readonly_fields = ['entity']

admin.site.register(EntityHistory, EntityHistoryModelAdmin)


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'product_type']
    readonly_fields = ['creator', 'instance_model']

admin.site.register(Product, ProductModelAdmin)
admin.site.register(ProductTypeTier)
admin.site.register(ProductType, GuardedModelAdmin)


class SoloTodoUserAdmin(EmailUserAdmin):
    fieldsets = EmailUserAdmin.fieldsets + \
                (('Additional information', {'fields': (
                    'first_name',
                    'last_name',
                    'preferred_language',
                    'preferred_currency',
                    'preferred_country',
                    'preferred_number_format')}),
                 )

admin.site.register(SoloTodoUser, SoloTodoUserAdmin)
admin.site.register(StoreType)


class StoreModelAdmin(GuardedModelAdmin):
    list_display = ['__str__', 'type', 'country']
    list_filter = ['type', 'country']

admin.site.register(Store, StoreModelAdmin)
admin.site.register(StoreUpdateLog)
