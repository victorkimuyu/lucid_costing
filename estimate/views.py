from django.db import transaction
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import ListView, DetailView

from .forms import (
    EstimateForm,
    DealerPartsFormset,
    OpenMarketPartsFormset,
    ContributionPartsFormset,
    OtherCostsFormset
)
from .models import Estimate, DealerPart, OpenMarketPart, ContributionPart, OtherCost


# Create EstimateCreateView
class EstimateCreateView(generic.CreateView):
    model = Estimate
    form_class = EstimateForm
    template_name = 'estimate/estimate.html'
    context_object_name = "estimate"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['dealer_parts'] = DealerPartsFormset(self.request.POST)
            ctx['openmarket_parts'] = OpenMarketPartsFormset(self.request.POST)
            ctx['contribution_parts'] = ContributionPartsFormset(self.request.POST)
            ctx['other_costs'] = OtherCostsFormset(self.request.POST)
        else:
            ctx['dealer_parts'] = DealerPartsFormset()
            ctx['openmarket_parts'] = OpenMarketPartsFormset()
            ctx['contribution_parts'] = ContributionPartsFormset()
            ctx['other_costs'] = OtherCostsFormset()
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        dealer_parts = ctx['dealer_parts']
        openmarket_parts = ctx['openmarket_parts']
        contribution_parts = ctx['contribution_parts']
        other_costs = ctx['other_costs']

        if dealer_parts.is_valid() and openmarket_parts.is_valid() and contribution_parts.is_valid() and other_costs.is_valid():
            with transaction.atomic():
                self.object = form.save()
                dealer_parts.instance = self.object
                dealer_parts.save()
                openmarket_parts.instance = self.object
                openmarket_parts.save()
                contribution_parts.instance = self.object
                contribution_parts.save()
                other_costs.instance = self.object
                other_costs.save()
                return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form,
                                                                 dealer_parts=dealer_parts,
                                                                 openmarket_parts=openmarket_parts,
                                                                 contribution_parts=contribution_parts,
                                                                 other_costs=other_costs))

    def form_invalid(self, form):
        ctx = self.get_context_data()
        dealer_parts = ctx['dealer_parts']
        openmarket_parts = ctx['openmarket_parts']
        contribution_parts = ctx['contribution_parts']
        other_costs = ctx['other_costs']
        return self.render_to_response(self.get_context_data(form=form,
                                                             dealer_parts=dealer_parts,
                                                             openmarket_parts=openmarket_parts,
                                                             contribution_parts=contribution_parts,
                                                             other_costs=other_costs))


class EstimateDetailView(DetailView):
    model = Estimate
    form_class = EstimateForm
    context_object_name = "estimate"
    template_name = "estimate/estimate-detail.html"

    def get_context_data(self, **kwargs):
        estimate = self.get_object()
        context = super().get_context_data(**kwargs)
        context["dealer_parts"] = estimate.item_set.instance_of(DealerPart)
        context["open_market_parts"] = estimate.item_set.instance_of(OpenMarketPart)
        context["contribution_parts"] = estimate.item_set.instance_of(ContributionPart)
        context["other_costs"] = estimate.item_set.instance_of(OtherCost)
        return context


class EstimateListView(ListView):
    model = Estimate
    template_name = "estimate/estimate_list.html"
    context_object_name = "estimates"

    def get_queryset(self):
        return Estimate.objects.filter(user=self.request.user)

    paginate_by = 2
