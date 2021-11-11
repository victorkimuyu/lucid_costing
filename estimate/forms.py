from django import forms
from django.forms import inlineformset_factory

from .models import Estimate, DealerPart, OpenMarketPart, ContributionPart, OtherCost


# create a form for the estimate
class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = ("report", "dealer_discount", "vattable")
        widgets = {
            "report": forms.TextInput(attrs={"class": "form-control"}),
            "dealer_discount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "1",
                    "max": "100",
                }
            ),
            "vattable": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


# Create DealerPart Form by extending the forms.Form, the fields are item, quantity, an amount
class DealerPartForm(forms.ModelForm):
    class Meta:
        model = DealerPart
        fields = "__all__"
        widgets = {
            "item": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "dealerQty",
                    "min": "1",
                    "onchange": "calculateDealerPartAmount()",
                }
            ),
            "unit_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "dealerUnitPrice",
                    "min": "1",
                    "step": "0.01",
                    "onchange": "calculateDealerPartAmount()",
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "dealerAmount",
                    "step": "0.01",
                    "readonly": "readonly",
                    "required": "",
                }
            ),
        }


class OpenMarketPartForm(forms.ModelForm):
    class Meta:
        model = OpenMarketPart
        fields = "__all__"
        widgets = {
            "item": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "openMarketQty",
                    "min": "1",
                    "onchange": "calculateOpenMarketPartAmount()",
                }
            ),
            "unit_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "openMarketUnitPrice",
                    "min": "1",
                    "step": "0.01",
                }
            ),
            "negotiated_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "openMarketNegotiatedPrice",
                    "required": "",
                    "step": "0.01",
                    "min": "1",
                    "onchange": "calculateOpenMarketPartAmount()",
                    "onexit": "setNegotiatedPrice()",
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "openMarketAmount",
                    "required": "",
                    "readonly": "readonly",
                    "min": "1",
                    "step": "0.01",
                }
            ),
        }

    # override full_clean and set negotiated_price to unit_cost if it is not set
    def clean(self):
        cleaned_data = super().clean()
        unit_price = cleaned_data.get("unit_price")
        negotiated_price = cleaned_data.get("negotiated_price")
        if unit_price and not negotiated_price:
            cleaned_data["negotiated_price"] = unit_price

    # override save to set the amount field
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.amount = instance.quantity * instance.negotiated_price
        if commit:
            instance.save()
        return instance


class ContributionPartForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["contrib_amount"].label = "Amount"
        self.fields["contrib_perc"].label = "Cont. %"
        self.fields["amount"].label = "Balance"

    class Meta:
        model = ContributionPart
        fields = "__all__"
        widgets = {
            "item": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "contribQty",
                    "min": "1",
                    "onchange": "contribCalculations()",
                }
            ),
            "unit_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "contribUnitPrice",
                    "min": "1",
                    "step": "0.01",
                    "onchange": "contribCalculations()",
                }
            ),
            "negotiated_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "contribNegotiatedPrice",
                    "required": "",
                    "min": "1",
                    "step": "0.1",
                    "onchange": "contribCalculations()",
                }
            ),
            "contrib_perc": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "contribPerc",
                    "min": "1",
                    "step": "0.01",
                    "onchange": "contribCalculations()",
                }
            ),
            "contrib_amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "contribAmount",
                    "label": "Cont. %",
                    "min": "1",
                    "step": "0.1",
                    "readonly": "readonly",
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "contribBalance",
                    "readonly": "readonly",
                    "required": "",
                }
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
                attrs={"class": "form-control", "min": "1", "step": "0.1"}
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
