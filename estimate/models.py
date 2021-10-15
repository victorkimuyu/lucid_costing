from django.db import models
from django.db.models import Sum
from polymorphic.models import PolymorphicModel


class Estimate(models.Model):
    report = models.CharField(max_length=10)
    dealer_discount = models.IntegerField(null=True, blank=True)

    is_vattable = models.BooleanField(default=True)

    @property
    def dealer_parts(self):
        items = self.item_set.instance_of(DealerPart)
        if items:
            items_total = items.aggregate(Sum("amount"))['amount__sum']
            if self.dealer_discount:
                if self.dealer_discount > 0:
                    discount = items_total * (self.dealer_discount / 100)
                    return items_total - discount
            else:
                return items_total

    @property
    def open_market_parts(self):
        items = self.item_set.instance_of(OpenMarketPart)
        if items:
            return items.aggregate(Sum("amount"))['amount__sum']

    @property
    def contribution_parts(self):
        items = self.item_set.instance_of(ContributionPart)
        if items:
            return items.aggregate(Sum("amount"))['amount__sum']

    @property
    def other_costs(self):
        items = self.item_set.instance_of(OtherCost)
        if items:
            return items.aggregate(Sum("amount"))['amount__sum']

    def __str__(self):
        return self.report

    @property
    def summary(self):
        items = {
            'dealer_parts': self.dealer_parts,
            'open_market_parts': self.open_market_parts,
            'contribution_parts': self.contribution_parts,
            'other_costs': self.other_costs
        }

        items_total = sum([value for value in items.values() if value])
        vat = 0
        if self.is_vattable:
            vat = items_total * 0.16
        items["estimate_total"] = items_total
        items['vat'] = vat
        items['estimate_total'] = items_total + vat
        return items

    @property
    def vat(self):
        return self.summary['vat']

    @property
    def estimate_total(self):
        return self.summary['estimate_total']


class Item(PolymorphicModel):
    estimate = models.ForeignKey(Estimate, on_delete=models.PROTECT)
    description = models.CharField(max_length=50)
    amount = models.IntegerField()

    def __str__(self):
        return self.description


class Part(Item):
    quantity = models.IntegerField()
    unit_cost = models.FloatField()


class DealerPart(Part):
    def save(self, *args, **kwargs):
        cost = self.unit_cost
        qty = self.quantity
        self.amount = qty * cost

        super(DealerPart, self).save(*args, **kwargs)


class OpenMarketPart(Part):
    negotiated = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.negotiated:
            self.negotiated = self.unit_cost
        self.amount = (self.negotiated * self.quantity)
        super(OpenMarketPart, self).save(*args, **kwargs)


class ContributionPart(Part):
    negotiated = models.FloatField(null=True, blank=True)
    contrib_perc = models.FloatField(default=0)

    @property
    def contrib_amount(self):
        if not self.negotiated:
            self.negotiated = self.unit_cost
        if self.contrib_perc:
            return (self.contrib_perc / 100) * self.negotiated * self.quantity
        else:
            return 0

    def save(self, *args, **kwargs):
        if not self.negotiated:
            self.negotiated = self.unit_cost
        self.amount = (self.negotiated * self.quantity) - self.contrib_amount
        super(ContributionPart, self).save(*args, **kwargs)


class OtherCost(Item):
    pass
