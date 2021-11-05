from django.db import transaction
from django.views.generic import CreateView, ListView, DetailView

from .forms import (
    EstimateForm,
    DealerPartFormSet,
    OpenMarketPartFormSet,
    ContributionPartFormSet,
    OtherCostFormSet,
)
from .models import Estimate, DealerPart, OpenMarketPart, ContributionPart, OtherCost


# Create estimate CreateView and include inline formsets
class EstimateCreateView(CreateView):
    model = Estimate
    form_class = EstimateForm
    template_name = "estimate/estimate.html"
    context_object_name = "estimate"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dealer_part_formset"] = DealerPartFormSet(self.request.POST or None)
        context["open_market_part_formset"] = OpenMarketPartFormSet(self.request.POST or None)
        context["contribution_part_formset"] = ContributionPartFormSet(self.request.POST or None)
        context["other_cost_formset"] = OtherCostFormSet(self.request.POST or None)
        return context

    def form_valid(self, form):
        ctx = self.get_context_data()
        sections = {
            "dealer_part_formset": ctx["dealer_part_formset"],
            "open_market_part_formset": ctx["open_market_part_formset"],
            "contribution_part_formset": ctx["contribution_part_formset"],
            "other_cost_formset": ctx["other_cost_formset"],
        }

        for section in sections.values():
            print(type(section))
            if section and section.is_valid():
                with transaction.atomic():
                    self.object = form.save()
                    section.instance = self.object
                    section.save()
                    return super().form_valid(form)
            else:
                return self.form_invalid(form)


class EstimateDetailView(DetailView):
    model = Estimate
    context_object_name = "estimate"
    template_name = "estimate/estimate-detail.html"

    def get_context_data(self, **kwargs):
        estimate = self.get_queryset().
        context = super().get_context_data(**kwargs)
        context["report"] = estimate.report
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

