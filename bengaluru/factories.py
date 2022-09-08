import factory.fuzzy
from bengaluru.models import FiveHundred


class FiveHundredFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FiveHundred

    date = factory.Faker('date')
    time = factory.Faker('date_time')
    rank = factory.fuzzy.FuzzyInteger(1, 5)
    symbol = factory.Faker('first_name')
    identifier = factory.Faker('first_name')
    company_name = factory.Faker('company')
    isbin = factory.Faker('ean', length=8)
    price = factory.fuzzy.FuzzyDecimal(100, 7000, 2)
