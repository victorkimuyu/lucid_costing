from django import forms
from django.forms import inlineformset_factory

from .models import Estimate, DealerPart, OpenMarketPart, ContributionPart, OtherCost


# create a form for the estimate
class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = "__all__"


# Create DealerPart Form by extending the forms.Form, the fields are item, quantity, an amount
class DealerPartForm(forms.ModelForm):

    class Meta:
        model = DealerPart
        fields = "__all__"
        widgets = {
            "item": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
        }

        # Create OpenMarketPart Form by extending the forms.Form, the fields are item, quantity, unit_price and amount


class OpenMarketPartForm(forms.ModelForm):
    class Meta:
        model = OpenMarketPart
        fields = "__all__"
        widgets = {
            "item": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
            "negotiated_price": forms.NumberInput(attrs={"class": "form-control", "required": ""}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
        }


# Create ContributionPart Form by extending the forms.Form, the fields are item, quantity, unit_price and amount
class ContributionPartForm(forms.ModelForm):

    class Meta:
        model = ContributionPart
        fields = "__all__"
        widgets = {
            "item": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
            "negotiated_price": forms.NumberInput(attrs={"class": "form-control", "required": ""}),
            "contrib_perc": forms.NumberInput(attrs={"class": "form-control"}),
            "contrib_amount": forms.NumberInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
        }


# Create OtherCost Form by extending the forms.Form, the fields are item, quantity, unit_price and amount
class OtherCostForm(forms.ModelForm):
    class Meta:
        model = OtherCost
        fields = "__all__"
        widgets = {
            "item": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
        }


# create inline_formsets for DealerPart, OpenMarketPart, ContributionPart, OtherCost
DealerPartsFormset = inlineformset_factory(
    Estimate,
    DealerPart,
    form=DealerPartForm,
    fields=("item", "quantity", "unit_price", "amount"),
    extra=1,
)
OpenMarketPartsFormset = inlineformset_factory(
    Estimate,
    OpenMarketPart,
    form=OpenMarketPartForm,
    fields=("item", "quantity", "unit_price", "negotiated_price", "amount"),
    extra=1,
)
ContributionPartsFormset = inlineformset_factory(
    Estimate,
    ContributionPart,
    form=ContributionPartForm,
    fields=(
        "item",
        "quantity",
        "unit_price",
        "negotiated_price",
        "contrib_perc",
        "contrib_amount",
        "amount",
    ),
    extra=1,
)
OtherCostsFormset = inlineformset_factory(
    Estimate, OtherCost, form=OtherCostForm, fields=("item", "amount"), extra=1
)
