from dataclasses import dataclass


# This generates a full class complete with a few dunder methods (e.g __init__, __repr__, __eq___)  setup how you probably want them

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

# Doesn't have automatic type validation 
fr = Country(code="FR", population="75M")
print(fr)
# > Country(code='FR', population='75M')

# Nor type conversion
fr = Country(code="FR", population="75")
# > Country(code='FR', population="75")


@dataclass()
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


# TODO show compare = False
@dataclass(order=True)
class Country:
    code: str
    population: int = 0  # defaults


fr = Country(code="FR", population=75)
de = Country(code="DE", population=85)
it = Country(code="IT", population=60)
pt = Country(code="PT", population=10)
at = Country(code="AT", population=15)

emea = [fr, de, it, pt, at]

print(sorted(emea))
# > [
# > Country(code='AT', population=15),
# > Country(code='DE', population=85), 
# > Country(code='FR', population=75),
# > Country(code='IT', population=60), 
# > Country(code='PT', population=10)
# ]
# Pretty difficult to do on a normal class, there is a helper decorator in functools (total_ordering) but it doesn't check class


from dataclasses import field, fields


@dataclass(order=True)
class Country:
    code: str
    stores: field(repr=False, default_factory=list, compare=False)
    revenue: int = field(repr=False, metadata={"currency": "EUROS"})
    daily_revenue: int = field(init=False, repr=False, metadata={"currency": "EUROS"})
    population: int = 0 # default field moved to bottom


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
fr.add_store('BIARRITZ')
print(fr)
# > Country(code='FR', stores=['TOULON CENTRAL', 'TOULOUSE SOUTH'], population=75)

revenue_field = fields(fr)[2]
print(revenue_field.metadata["currency"])

print( [field.name for field in fields(fr)])
# > ['code', 'stores', 'revenue', 'daily_revenue', 'population']


# Subclassing / Inheritance '...is bad for you' according to attrs authors https://www.attrs.org/en/stable/examples.html

try:
    @dataclass
    class ApacCountry(Country):
        region : str
except TypeError as error:
    pass

# > Error - Non-default argument 'region' follows default argument



# Composition
from typing import List
from dataclasses import asdict


@dataclass
class Store:
    code : str
    size : str
    revenue : int


@dataclass
class Country:
    code: str
    stores : List[Store]


stores = [
    Store(code='PARIS',size='M',revenue=100),
    Store(code='LYON',size='S',revenue=100)

]
fr = Country(code='FR',stores=stores)
print(fr.stores)
# > [Store(code='PARIS', size='M', revenue=100), Store(code='LYON', size='S', revenue=100)]
print (asdict(fr))
# > {'code': 'FR', 'stores': ['TOULON CENTRAL', 'TOULOUSE SOUTH', 'BIRITTIZ'], 'revenue': 1000, 'daily_revenue': 2.73972602739726, 'population': 75}

import pandas as pd

stores += [
    Store(code='BREST',size='S',revenue=100),
    Store(code='CALAIS',size='M',revenue=100),
    Store(code='NANTES',size='S',revenue=100),
    Store(code='NICE',size='S',revenue=100),
    Store(code='BORDEAUX',size='S',revenue=100),
]

@dataclass
class Country:
    code: str
    stores : List[Store]

    def as_dataframe(self):
        return pd.DataFrame([{'country_code' : self.code} | asdict(store)  for store in self.stores])

fr = Country(code='FR',stores=stores)
print(fr.as_dataframe().head())

# >   country_code    code size  revenue
# > 0           FR   PARIS    M      100
# > 1           FR    LYON    S      100
# > 2           FR   BREST    S      100
# > 3           FR  CALAIS    M      100
# > 4           FR  NANTES    S      100




@dataclass
class Store:
    code : str
    size : str 
    revenue : int = field(repr=False)
    country : field(init=False) = None

    def get_size(self):
        return self.size

    def register_country(self,country):
        self.country = country

    def __str__(self):
        return f'<Store> Code: "{self.code}" Country: "{self.country.code}"'


@dataclass
class Country:
    code: str
    stores : List[Store] = field(repr=False)

    def __post_init__(self):
        for store in self.stores:
            store.register_country(self)

stores = [
    Store(code='PARIS',size='M',revenue=100),
    Store(code='LYON',size='S',revenue=100)

]

fr = Country(code='FR',stores=stores)

# > fr.stores[0]
# Store(code='PARIS', size='M', country=Country(code='FR'))

print(fr.stores[0])
# > <Store> Code: "PARIS" Country: "FR"
