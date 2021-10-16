from django.contrib import admin

from estimate.models import DealerPart, OtherCost, ContributionPart, OpenMarketPart, Estimate


class DealerPartInline(admin.TabularInline):
    model = DealerPart
    fields = ['description', 'quantity', 'unit_cost', 'amount']
    readonly_fields = ['amount']


class OpenMarketPartInline(admin.TabularInline):
    model = OpenMarketPart
    fields = ['description', 'quantity', 'unit_cost', 'negotiated', 'amount']
    readonly_fields = ['amount']


class ContributionPartInline(admin.TabularInline):
    model = ContributionPart
    fields = ['description', 'quantity', 'unit_cost', 'negotiated', 'contrib_perc', 'amount']
    readonly_fields = ['amount']


class OtherCostInline(admin.TabularInline):
    model = OtherCost
    fields = ['description', 'amount']


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    inlines = [DealerPartInline, OpenMarketPartInline, ContributionPartInline, OpenMarketPartInline, OtherCostInline]
    list_display = ['report', 'dealer_parts', 'open_market_parts', 'contribution_parts', 'other_costs',
                    'vat', 'estimate_total']
