from dataclasses import dataclass

# "provides a decorator... for automatically adding generated special methods such as __init__() and __repr__() to user-defined classes."
# Aim is to create the class how you probably want it and provide options if you want something different
# https://docs.python.org/3/library/dataclasses.html


@dataclass
class Country:
    code: str
    population: int = 0


fr = Country(code="FR", population=75)
print(fr)
# > Country(code='FR', population=75)

print(fr.code)
# > "FR"


# Mutable by default but @dataclass(frozen=True) will make it immutable
fr.code = "FRANCE"

# Doesn't have automatic type validation (though mypy will catch this)
fr = Country(code="FR", population="75M")
print(fr)
# > Country(code='FR', population='75M')

# Nor type conversion
fr = Country(code="FR", population="75")
# > Country(code='FR', population="75")


@dataclass
class EmeaCountry(Country):
    code: str
    population: int = 0


fr = Country(code="FR", population=75)
fr2 = Country(code="FR", population=75)
fr3 = EmeaCountry(code="FR", population=75)

print(fr == fr2)
# > True
print(fr == fr2 == fr3)
# > False

# Unlike classes the __eq__ checks values, unlike namedtuples this checks the class as well
# If you don't want this behaviour you can pass @dataclass(eq=False) and then f2 == fr2 would be false

from dataclasses import field, fields


@dataclass(order=True)
class Country:
    code: str = field(compare=False)
    population: int = field(compare=True, default=0)


fr = Country(code="FR", population=75)
de = Country(code="DE", population=85)
it = Country(code="IT", population=60)
pt = Country(code="PT", population=10)
at = Country(code="AT", population=15)

emea = [fr, de, it, pt, at]

print(sorted(emea))
# > [Country(code='PT', population=10), Country(code='AT', population=15), Country(code='IT', population=60), Country(code='FR', population=75), Country(code='DE', population=85)]
# Pretty difficult to do on a normal class, there is a helper decorator in functools (total_ordering) but it doesn't check class


from typing import List
from dataclasses import field, fields


@dataclass(order=True)
class Country:
    code: str
    revenue: int = field(repr=False, metadata={"currency": "EUROS"})
    daily_revenue: int = field(init=False, repr=False, metadata={"currency": "EUROS"})
    population: int = 0
    stores: List = field(repr=False, default_factory=list, compare=False)


    def __post_init__(self):
        self.daily_revenue = self.revenue / 365

    @property
    def number_stores(self):
        return len(self.stores)

    def add_store(self, store: str):
        self.stores.append(store)


fr = Country(
    code="FR", population=75, revenue=1000, stores=["TOULON CENTRAL", "TOULOUSE SOUTH"]
)
fr.add_store("BIARRITZ")

revenue_field = fields(fr)[2]
print(revenue_field.metadata["currency"])
# > "EUROS"

print([field.name for field in fields(fr)])
# > ['code', 'stores', 'revenue', 'daily_revenue', 'population']


# Subclassing

try:

    @dataclass
    class ApacCountry(Country):
        region: str


except TypeError as error:
    pass

# > Error - Non-default argument 'region' follows default argument


# Composition

from typing import List
from dataclasses import asdict


@dataclass
class Store:
    code: str
    size: str
    revenue: int


@dataclass
class Country:
    code: str
    stores: List[Store]


stores = [
    Store(code="PARIS", size="M", revenue=100),
    Store(code="LYON", size="S", revenue=100),
]
fr = Country(code="FR", stores=stores)
print(fr.stores)
# > [Store(code='PARIS', size='M', revenue=100), Store(code='LYON', size='S', revenue=100)]
print(asdict(fr))
# > {'code': 'FR', 'stores': [{'code': 'PARIS', 'size': 'M', 'revenue': 100}, {'code': 'LYON', 'size': 'S', 'revenue': 100}]}

import pandas as pd

stores += [
    Store(code="BREST", size="S", revenue=100),
    Store(code="CALAIS", size="M", revenue=100),
    Store(code="NANTES", size="S", revenue=100),
    Store(code="NICE", size="S", revenue=100),
    Store(code="BORDEAUX", size="S", revenue=100),
]


@dataclass(frozen=True)
class Country:
    code: str
    stores: List[Store]

    def as_dataframe(self):
        return pd.DataFrame(
            [{"country_code": self.code} | asdict(store) for store in self.stores]
        )


fr = Country(code="FR", stores=stores)
print(fr.as_dataframe().head())

# >   country_code    code size  revenue
# > 0           FR   PARIS    M      100
# > 1           FR    LYON    S      100
# > 2           FR   BREST    S      100
# > 3           FR  CALAIS    M      100
# > 4           FR  NANTES    S      100


@dataclass
class Store:
    code: str
    size: str
    revenue: int = field(repr=False)
    country = None

    def register_country(self, country):
        self.country = country

    def __str__(self):
        return f'<Store> Code: "{self.code}" Country: "{self.country.code}"'


@dataclass
class Country:
    code: str
    stores: List[Store] = field(repr=False)
    population: int = 0

    def __post_init__(self):
        for store in self.stores:
            store.register_country(self)


stores = [
    Store(code="PARIS", size="M", revenue=100),
    Store(code="LYON", size="S", revenue=100),
]

fr = Country(code="FR", stores=stores,population=75)

# > fr.stores[0]
# Store(code='PARIS', size='M', country=Country(code='FR'))


print(fr.stores[0])
# > <Store> Code: "PARIS" Country: "FR"

for store in fr.stores:
    print(store.code,store.country.code,store.country.population)
    # > PARIS FR 75
    # > LYON FR 75

# Gotchas? Lack of type validation; not necessarily obvious which dunder methods it actually creates
