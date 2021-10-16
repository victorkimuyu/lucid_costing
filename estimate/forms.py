from django import forms

from estimate.models import OtherCost, ContributionPart, OpenMarketPart, DealerPart


class DealerPartForm(forms.ModelForm):
    class Meta:
        model = DealerPart
        fields = []


class OpenMarketPartForm(forms.ModelForm):
    class Meta:
        model = OpenMarketPart
        fields = []


class ContributionPartForm(forms.ModelForm):
    class Meta:
        model = ContributionPart
        fields = []


class OtherCostForm(forms.ModelForm):
    class Meta:
        model = OtherCost
        fields = []
