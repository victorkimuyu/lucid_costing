from django.views import generic
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory

from .models import DealerPart, OpenMarketPart, ContributionPart, OtherCost, Estimate


class DealerPartInline(InlineFormSetFactory):
    model = DealerPart
    fields = ['description', 'quantity', 'unit_cost', 'amount']


class OpenMarketPartInline(InlineFormSetFactory):
    model = OpenMarketPart
    fields = ['description', 'quantity', 'unit_cost', 'negotiated', 'amount']


class ContributionPartInline(InlineFormSetFactory):
    model = ContributionPart
    fields = ['description', 'quantity', 'unit_cost', 'negotiated', 'contrib_perc', 'amount']


class OtherCostInline(InlineFormSetFactory):
    model = OtherCost
    fields = ['description', 'amount']


class CreateEstimateView(CreateWithInlinesView):
    model = Estimate
    inlines = [DealerPartInline, OpenMarketPartInline, ContributionPartInline, OtherCostInline]
    fields = ['report', 'vattable', 'dealer_discount']
    template_name = 'estimate/estimate.html'


class UpdateEstimateView(UpdateWithInlinesView):
    model = Estimate
    context_object_name = 'estimate'
    template_name = 'estimate/estimate.html'
    fields = ['report', 'vattable', 'dealer_discount']
    inlines = [DealerPartInline, OpenMarketPartInline, ContributionPartInline, OtherCostInline]


class EstimateDetailView(generic.DetailView):
    context_object_name = "estimate"
    model = Estimate
    template_name = 'estimate/estimate-detail.html'
    

class EstimateListView(generic.ListView):
    model = Estimate
    context_object_name = "estimates"
    template_name = "estimate/estimate-list.html"
