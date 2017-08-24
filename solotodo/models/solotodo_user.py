from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils import translation, timezone
from django.utils.translation import ugettext_lazy as _
from custom_user.models import AbstractEmailUser

from .number_format import NumberFormat
from .country import Country
from .currency import Currency
from .language import Language


class SoloTodoUser(AbstractEmailUser):
    first_name = models.CharField(_('first name'), max_length=30, blank=True,
                                  null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True,
                                 null=True)
    preferred_language = models.ForeignKey(Language, blank=True, null=True)
    preferred_currency = models.ForeignKey(Currency, blank=True, null=True)
    preferred_country = models.ForeignKey(Country, blank=True,
                                          null=True)
    preferred_number_format = models.ForeignKey(
        NumberFormat, blank=True, null=True)
    permissions = property(lambda self: sorted(self.get_all_permissions()))

    @classmethod
    def get_bot(cls):
        return cls.objects.get(email=settings.BOT_USERNAME)

    def email_recipient_text(self):
        first_name = self.first_name or ''
        last_name = self.last_name or ''
        full_name = '{} {}'.format(first_name, last_name).strip()
        if full_name:
            return '{} <{}>'.format(full_name, self.email)
        else:
            return self.email

    def send_entity_update_failure_email(self, entity, request_user,
                                         traceback):
        if self.preferred_language:
            email_language = self.preferred_language.code
        else:
            email_language = settings.LANGUAGE_CODE

        sender = SoloTodoUser().get_bot().email_recipient_text()
        translation.activate(email_language)

        email_recipients = [self.email_recipient_text()]

        html_message = render_to_string('mailing/index.html', {
            'entity': entity,
            'request_user': request_user,
            'timestamp': timezone.now(),
            'host': settings.BACKEND_HOST,
            'error': traceback
        })

        subject = _('Error updating entity')

        send_mail('{} {}'.format(subject, entity.id),
                  'Error', sender, email_recipients,
                  html_message=html_message)

    class Meta:
        app_label = 'solotodo'
        verbose_name = 'SoloTodo User'
        verbose_name_plural = 'SoloTodo Users'
