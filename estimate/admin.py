from django.contrib import admin

from estimate.models import DealerPart, OpenMarketPart, OtherCost, Estimate, ContributionPart


# @admin.register(DealerPart)
# class DealerPartAdmin(admin.ModelAdmin):
#     readonly_fields = ['amount']
#
#
# @admin.register(OpenMarketPart)
# class OpenMarketPartAdmin(admin.ModelAdmin):
#     list_display = ['description', 'quantity', 'unit_cost', 'negotiated', 'amount']
#     readonly_fields = ['amount']
#
#
# @admin.register(ContributionPart)
# class ContributionPartAdmin(admin.ModelAdmin):
#     fields = ['estimate', 'description', 'quantity', 'unit_cost', 'negotiated', 'contrib_perc', 'contrib_amount',
#               'amount']
#     readonly_fields = ['contrib_amount', 'amount']
#     list_display = ['description', 'amount']
#
#
# @admin.register(OtherCost)
# class OtherCostAdmin(admin.ModelAdmin):
#     list_display = ['description', 'amount']


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
