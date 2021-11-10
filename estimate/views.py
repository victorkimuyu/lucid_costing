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


# create Estimate create view and save it together with DealerPartsFormset
class EstimateCreateView(generic.CreateView):
    model = Estimate
    form_class = EstimateForm
    template_name = "estimate/estimate.html"
    context_object_name = "estimate"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["dealer_parts"] = DealerPartsFormset(self.request.POST)
            ctx["openmarket_parts"] = OpenMarketPartsFormset(self.request.POST)
            ctx["contribution_parts"] = ContributionPartsFormset(self.request.POST)
            ctx["other_costs"] = OtherCostsFormset(self.request.POST)

        else:
            ctx["dealer_parts"] = DealerPartsFormset()
            ctx["openmarket_parts"] = OpenMarketPartsFormset()
            ctx["contribution_parts"] = ContributionPartsFormset()
            ctx["other_costs"] = OtherCostsFormset()
        return ctx

    def form_valid(self, form):
        context = self.get_context_data()
        formsets = {
            "dealer_parts": context["dealer_parts"],
            "openmarket_parts": context["openmarket_parts"],
            "contribution_parts": context["contribution_parts"],
            "other_costs": context["other_costs"],
        }
        self.object = form.save()
        for formset in formsets.values():
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
        return HttpResponseRedirect(self.get_success_url())


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

    # create pagination for this list
    paginate_by = 2
