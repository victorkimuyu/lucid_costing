from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.urls import reverse
from polymorphic.models import PolymorphicModel


class Estimate(models.Model):
    report = models.CharField(max_length=10)
    dealer_discount = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )

    vattable = models.BooleanField(default=True)

    @property
    def dealer_parts(self):
        items = self.item_set.instance_of(DealerPart)
        if items:
            items_total = sum(item.amount for item in items)
            if not self.dealer_discount:
                return items_total.quantize(Decimal("0.01"))
            if self.dealer_discount > 0:
                discount = items_total * (self.dealer_discount / 100)
                return (items_total - discount).quantize(Decimal("0.01"))

    @property
    def open_market_parts(self):
        items = self.item_set.instance_of(OpenMarketPart)
        if items:
            return (items.aggregate(Sum("amount"))["amount__sum"]).quantize(
                Decimal("0.01")
            )

    @property
    def contribution_parts(self):
        items = self.item_set.instance_of(ContributionPart)
        if items:
            return (items.aggregate(Sum("amount"))["amount__sum"]).quantize(
                Decimal("0.01")
            )

    @property
    def other_costs(self):
        items = self.item_set.instance_of(OtherCost)
        if items:
            return (items.aggregate(Sum("amount"))["amount__sum"]).quantize(
                Decimal("0.01")
            )

    def __str__(self):
        return self.report

    @property
    def summary(self):
        items = {
            "dealer_parts": self.dealer_parts,
            "open_market_parts": self.open_market_parts,
            "contribution_parts": self.contribution_parts,
            "other_costs": self.other_costs,
        }

        items_total = sum(value for value in items.values() if value)
        vat = Decimal(0)
        if self.vattable:
            vat = items_total * Decimal(0.16)
        items["estimate_total"] = items_total
        items["vat"] = vat
        items["estimate_total"] = items_total + vat
        return items

    @property
    def vat(self):
        if self.vattable:
            result = self.summary["vat"]
            return result.quantize(Decimal("0.01"))

    @property
    def get_discount(self):
        if self.dealer_discount:
            items = self.item_set.instance_of(DealerPart)
            items_total = items.aggregate(Sum("amount"))["amount__sum"]
            discount = items_total * (self.dealer_discount / 100)
            return discount.quantize(Decimal("0.01"))
        else:
            return None

    @property
    def estimate_total(self):
        return self.summary["estimate_total"].quantize(Decimal("0.01"))

    def get_absolute_url(self):
        return reverse("estimate-detail", kwargs={"pk": self.pk})


class Item(PolymorphicModel):
    estimate = models.ForeignKey(Estimate, on_delete=models.PROTECT)
    item = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item


class DealerPart(Item):
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        cost = self.unit_price
        qty = self.quantity
        self.amount = qty * cost

        super(DealerPart, self).save(*args, **kwargs)


class OpenMarketPart(Item):
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    negotiated_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.negotiated_price:
            self.negotiated_price = self.unit_price
        self.amount = self.negotiated_price * self.quantity
        super(OpenMarketPart, self).save(*args, **kwargs)


class ContributionPart(Item):
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    negotiated_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    contrib_perc = models.IntegerField()
    contrib_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.negotiated_price:
            self.negotiated_price = self.unit_price
        # calculate contrib_amount and format result as a quantized Decimal
        if not self.contrib_perc:
            self.contrib_perc = 50
        self.contrib_amount = self.negotiated_price * Decimal(self.contrib_perc / 100).quantize(Decimal("0.01"))
        self.amount = (self.negotiated_price * self.quantity) - self.contrib_amount
        super(ContributionPart, self).save(*args, **kwargs)


class OtherCost(Item):
    pass
