import factory.fuzzy
from bengaluru.models import FiveHundred
from datetime import datetime


class FiveHundredFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FiveHundred

    date = factory.Faker('date')
    time = factory.LazyAttribute(
        lambda self: self.date
    )
    rank = factory.fuzzy.FuzzyInteger(1, 5)
    symbol = factory.Faker('first_name')
    identifier = factory.Faker('first_name')
    company_name = factory.Faker('company')
    isin = factory.Faker('ean', length=8)
    last_price = factory.fuzzy.FuzzyDecimal(100, 7000, 2)
    percentage_change = factory.fuzzy.FuzzyDecimal(1, 100, 2)
