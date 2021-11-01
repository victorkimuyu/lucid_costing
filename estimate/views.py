from django.views import generic
from extra_views import InlineFormSetFactory
from string import ascii_lowercase as letters

from .models import OtherCost, OpenMarketPart, ContributionPart, DealerPart, Estimate


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


class CreateEstimateView(generic.CreateView):
    model = Estimate
    inlines = [DealerPartInline, OpenMarketPartInline, ContributionPartInline, OtherCostInline]
    fields = ['report', 'vattable', 'dealer_discount']
    template_name = 'estimate/estimate.html'


class EstimateDetailView(generic.DetailView):
    model = Estimate
    context_object_name = "estimate"
    template_name = 'estimate/estimate-detail.html'

    def get_context_data(self, **kwargs):
        estimate = self.get_object()
        context = super().get_context_data(**kwargs)
        context["report"] = estimate.report
        context['dealer_parts'] = estimate.item_set.instance_of(DealerPart)
        context['open_market_parts'] = estimate.item_set.instance_of(OpenMarketPart)
        context['contribution_parts'] = estimate.item_set.instance_of(ContributionPart)
        context['other_costs'] = estimate.item_set.instance_of(OtherCost)
        return context


class EstimateListView(generic.ListView):
    model = Estimate
    context_object_name = "estimates"
    template_name = "estimate/estimate-list.html"
