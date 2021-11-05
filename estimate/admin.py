from django.contrib import admin

from estimate.models import DealerPart, OtherCost, ContributionPart, OpenMarketPart, Estimate


class DealerPartInline(admin.TabularInline):
    model = DealerPart
    fields = ['item', 'quantity', 'unit_price', 'amount']
    readonly_fields = ['amount']


class OpenMarketPartInline(admin.TabularInline):
    model = OpenMarketPart
    fields = ['item', 'quantity', 'unit_price', 'negotiated_price', 'amount']
    readonly_fields = ['amount']


class ContributionPartInline(admin.TabularInline):
    model = ContributionPart
    fields = ['item', 'quantity', 'unit_price', 'negotiated_price', 'contrib_perc', 'amount']
    readonly_fields = ['amount']


class OtherCostInline(admin.TabularInline):
    model = OtherCost
    fields = ['item', 'amount']


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    inlines = [DealerPartInline, OpenMarketPartInline, ContributionPartInline, OpenMarketPartInline, OtherCostInline]
    list_display = ['report', 'dealer_parts', 'open_market_parts', 'contribution_parts', 'other_costs',
                    'vat', 'estimate_total']
