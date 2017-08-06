from django import forms


class MetaFieldMakeNonNullablePrimitiveForm(forms.Form):
    default = forms.CharField(required=True, max_length=255)

    def __init__(self, meta_field, data=None, *args, **kwargs):
        try:
            field = getattr(forms, meta_field.model.name)(required=True)
        except AttributeError:
            # field = getattr(forms, meta_field.model.name)(
            #     required=True
            # )

            field = forms.ModelChoiceField(
                queryset=meta_field.model.instancemodel_set.all(),
                required=True
            )
        self.base_fields['default'] = field

        super(MetaFieldMakeNonNullablePrimitiveForm, self).__init__(
            data, *args, **kwargs)
