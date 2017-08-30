from django.contrib.auth import get_user_model
from django.db import models, IntegrityError
from django.db.models import Q
from django.utils import timezone

from solotodo.models.product import Product
from solotodo.models.currency import Currency
from solotodo.models.product_type import ProductType
from solotodo.models.store import Store


class EntityQueryset(models.QuerySet):
    def get_available(self):
        return self.exclude(Q(active_registry__isnull=True) |
                            Q(active_registry__stock=0))

    def get_unavailable(self):
        return self.filter(Q(active_registry__isnull=True) |
                           Q(active_registry__stock=0))

    def get_active(self):
        return self.filter(active_registry__isnull=False)

    def get_inactive(self):
        return self.filter(active_registry__isnull=True)


class Entity(models.Model):
    store = models.ForeignKey(Store)
    product_type = models.ForeignKey(ProductType)
    scraped_product_type = models.ForeignKey(ProductType, related_name='+')
    currency = models.ForeignKey(Currency)
    product = models.ForeignKey(Product, null=True)
    cell_plan = models.ForeignKey(Product, null=True, related_name='+')
    active_registry = models.OneToOneField('EntityHistory', related_name='+',
                                           null=True)
    name = models.CharField(max_length=256, db_index=True)
    cell_plan_name = models.CharField(max_length=50, null=True,
                                      blank=True, db_index=True)
    part_number = models.CharField(max_length=50, null=True, blank=True,
                                   db_index=True)
    sku = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    key = models.CharField(max_length=256, db_index=True)
    url = models.URLField(max_length=512, db_index=True)
    discovery_url = models.URLField(max_length=512, db_index=True)
    picture_url = models.URLField(max_length=512, blank=True, null=True)
    description = models.TextField(null=True)
    is_visible = models.BooleanField(default=True)
    latest_association_user = models.ForeignKey(get_user_model(), null=True)
    latest_association_date = models.DateTimeField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    objects = EntityQueryset.as_manager()

    def __str__(self):
        result = '{} - {}'.format(self.store, self.name)
        if self.cell_plan_name:
            result += ' / {}'.format(self.cell_plan_name)
        result += ' ({})'.format(self.product_type)

        return result

    def is_available(self):
        if self.active_registry:
            return self.active_registry.stock != 0

        return False

    def update_with_scraped_product(self, scraped_product,
                                    product_type=None, currency=None):
        from solotodo.models import EntityHistory

        assert scraped_product is None or self.key == scraped_product.key

        if scraped_product:
            if product_type is None:
                product_type = ProductType.objects.get(
                    storescraper_name=scraped_product.product_type)

            if currency is None:
                currency = Currency.objects.get(
                    iso_code=scraped_product.currency)

            new_active_registry = EntityHistory.objects.create(
                entity=self,
                stock=scraped_product.stock,
                normal_price=scraped_product.normal_price,
                offer_price=scraped_product.offer_price,
                cell_monthly_payment=scraped_product.cell_monthly_payment,
            )

            updated_data = {
                'scraped_product_type': product_type,
                'currency': currency,
                'name': scraped_product.name,
                'cell_plan_name': scraped_product.cell_plan_name,
                'part_number': scraped_product.part_number,
                'sku': scraped_product.sku,
                'url': scraped_product.url,
                'discovery_url': scraped_product.discovery_url,
                'picture_url': scraped_product.picture_url,
                'description': scraped_product.description,
                'active_registry': new_active_registry
            }

            self.update_keeping_log(updated_data)
        else:
            self.active_registry = None
            self.save()

    @classmethod
    def create_from_scraped_product(cls, scraped_product, store, product_type,
                                    currency):
        from solotodo.models import EntityHistory

        new_entity = cls.objects.create(
            store=store,
            product_type=product_type,
            scraped_product_type=product_type,
            currency=currency,
            name=scraped_product.name,
            cell_plan_name=scraped_product.cell_plan_name,
            part_number=scraped_product.part_number,
            sku=scraped_product.sku,
            key=scraped_product.key,
            url=scraped_product.url,
            discovery_url=scraped_product.discovery_url,
            picture_url=scraped_product.picture_url,
            description=scraped_product.description,
            is_visible=True,
        )

        new_entity_history = EntityHistory.objects.create(
            entity=new_entity,
            stock=scraped_product.stock,
            normal_price=scraped_product.normal_price,
            offer_price=scraped_product.offer_price,
            cell_monthly_payment=scraped_product.cell_monthly_payment
        )

        new_entity.active_registry = new_entity_history
        new_entity.save()

    def update_keeping_log(self, updated_data, user=None):
        from solotodo.models import EntityLog

        if not user:
            user = get_user_model().get_bot()

        entity_log = EntityLog(
            entity=self,
            user=user,
        )

        save_log = False

        for field, new_value in updated_data.items():
            old_value = getattr(self, field)
            if field in EntityLog.DATA_FIELDS:
                setattr(entity_log, field, old_value)
                if old_value != new_value:
                    save_log = True

            setattr(self, field, new_value)

        self.save()

        if save_log:
            # Fill the remaining fields
            for field in EntityLog.DATA_FIELDS:
                if field not in updated_data:
                    entity_value = getattr(self, field)
                    setattr(entity_log, field, entity_value)
            entity_log.save()

    def save(self, *args, **kwargs):
        is_associated = self.product_id or self.cell_plan_id

        if self.latest_association_user_id and \
                not self.latest_association_date:
            raise IntegrityError('Resolved entity must have a date')

        if not self.latest_association_user_id and \
                self.latest_association_date:
            raise IntegrityError('Resolved entity must have a resolver')

        if not self.is_visible and is_associated:
            raise IntegrityError('Entity cannot be associated and be hidden '
                                 'at the same time')

        if not self.product_id and self.cell_plan_id:
            raise IntegrityError('Entity cannot have a cell plan but '
                                 'not a primary product')

        if is_associated and not self.latest_association_user_id:
            raise IntegrityError('Entity cannot be associated to product '
                                 'without resolver')

        if not is_associated and self.latest_association_user_id:
            raise IntegrityError('Entity cannot have a resolver without '
                                 'being associated')

        super(Entity, self).save(*args, **kwargs)

    def update_pricing(self):
        scraper = self.store.scraper
        scraped_products = scraper.products_for_url(
            self.discovery_url,
            product_type=self.scraped_product_type.storescraper_name,
            extra_args=self.store.storescraper_extra_args
        )

        entity_scraped_product = None
        for scraped_product in scraped_products:
            if scraped_product.key == self.key:
                entity_scraped_product = scraped_product
                break

        self.update_with_scraped_product(entity_scraped_product)

    def events(self):
        entity = self
        events = []

        def apply_log_to_entity(log):
            from solotodo.models import EntityLog

            local_changes = []

            for field in EntityLog.DATA_FIELDS:
                entity_value = getattr(entity, field)
                log_value = getattr(log, field)
                if entity_value != log_value:
                    setattr(entity, field, log_value)
                    local_changes.append({
                        'field': field,
                        'old_value': log_value,
                        'new_value': entity_value,
                    })

            return local_changes

        for log in self.entitylog_set.select_related():
            changes = apply_log_to_entity(log)
            events.append({
                'user': log.user,
                'timestamp': log.creation_date,
                'changes': changes
            })

        return events

    def user_has_staff_perms(self, user):
        return user.has_perm('product_type_entities_staff',
                             self.product_type) \
               and user.has_perm('store_entities_staff', self.store)

    class Meta:
        app_label = 'solotodo'
        unique_together = ('store', 'key')
        permissions = [
            ('backend_list_entity', 'Can view entity list in backend'),
        ]
