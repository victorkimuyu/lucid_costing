from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from django import forms
from django.forms import inlineformset_factory

from estimate.models import DealerPart, OpenMarketPart, ContributionPart, Estimate, OtherCost


# using Form class, create a form for Estimate model
class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = ("report", "dealer_discount", "vattable")


class DealerForm(forms.ModelForm):
    class Meta:
        model = DealerPart
        fields = ("item", "quantity", "unit_price", "amount")


class OpenMarketForm(forms.ModelForm):
    class Meta:
        model = OpenMarketPart
        fields = ("item", "quantity", "unit_price", "negotiated_price", "amount")


class ContributionForm(forms.ModelForm):
    class Meta:
        model = ContributionPart
        fields = ("item", "quantity", "unit_price", "negotiated_price", "contrib_perc", "amount")


class OtherCostForm(forms.ModelForm):
    class Meta:
        model = OtherCost
        fields = ("item", "amount")


# Create the formset class.
DealerPartFormSet = inlineformset_factory(Estimate, DealerPart, form=DealerForm, extra=1)
OpenMarketPartFormSet = inlineformset_factory(Estimate, OpenMarketPart, form=OpenMarketForm, extra=1)
ContributionPartFormSet = inlineformset_factory(Estimate, ContributionPart, form=ContributionForm, extra=1)
OtherCostFormSet = inlineformset_factory(Estimate, OtherCost, form=OtherCostForm, extra=1)


# create crispy formset
class DealerPartFormSetHelper(DealerPartFormSet):
    def __init__(self, *args, **kwargs):
        super(DealerPartFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                'Dealer Part',
                'item',
                'quantity',
                'unit_price',
                'amount',
            )
        )


# create crispy formset
class OpenMarketPartFormSetHelper(OpenMarketPartFormSet):
    def __init__(self, *args, **kwargs):
        super(OpenMarketPartFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                'Open Market Part',
                'item',
                'quantity',
                'unit_price',
                'negotiated_price',
                'amount',
            )
        )


# create crispy formset
class ContributionPartFormSetHelper(ContributionPartFormSet):
    def __init__(self, *args, **kwargs):
        super(ContributionPartFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                'Contribution Part',
                'item',
                'quantity',
                'unit_price',
                'negotiated_price',
                'contrib_perc',
                'amount',
            )
        )


class OtherCostFormSetHelper(OtherCostFormSet):
    def __init__(self, *args, **kwargs):
        super(OtherCostFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                'Other Cost',
                'item',
                'amount',
            )
        )
