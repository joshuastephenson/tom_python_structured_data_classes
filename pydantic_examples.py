import pprint

from pydantic import (
    constr,
    conint,
    conlist,
    PositiveInt,
    StrictInt,
    validator,
    ValidationError,
)
from pydantic.dataclasses import dataclass

# "Data validation and settings management using python type annotations. pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.
# https://pydantic-docs.helpmanual.io/


@dataclass
class Country:

    population: PositiveInt
    code: constr(min_length=2, max_length=2)

    @validator("code")
    def all_uppercase_letters(cls, v):
        if v.upper() != v or not v.isalpha():
            raise ValueError("Code must be all uppercase letters")
        return v

    # PositiveInt and constr an example of a constrained type
    # Other includes...
    #   NegativeFloat etc
    #   conint
    #   conlist

    # The default types will attempt best effort conversion
    # There are also strict types such as StrictInt, StrictInt
    # which will not


# Conversion happens when possible
fr = Country(population="123", code="FR")

# Equality check works just like a dataclass
fr2 = Country(population=123, code="FR")
print(fr == fr2)
# > True

try:
    fr = Country(population=123, code="F1")
except ValidationError:
    pass
    # > Code must be alphanumeric (type=value_error)


# Pydantic validators are pretty flexible
import dataclasses

CURRENCIES = {"US": "$", "GB": "£"}


@dataclass
class Country:

    code: constr(min_length=2, max_length=2)
    revenue: conint(multiple_of=1000)
    cost: conint(multiple_of=1000)
    population: conint(multiple_of=1000000) = 0
    # You can still bring in elements from standard dataclasses
    stores: conlist(str, min_items=0, max_items=10) = dataclasses.field(
        default_factory=list
    )

    @validator("stores", each_item=True)
    def as_code(cls, v):
        assert v.upper() == v and " " not in v
        return v

    @validator(
        "revenue", "cost", pre=True
    )  # pre means we run this prior to other validation on these fields
    def remove_currency(cls, v, values):
        country_code = values["code"]
        if isinstance(v, str) and v.startswith(CURRENCIES[country_code]) and len(v) > 1:
            return v[1:]
        return v


us = Country(code="US", revenue=1000, cost="$1000")
us = Country(code="US", revenue=1000, cost="$1000", stores=["NEW_YORK"])
try:
    us = Country(code="US", revenue=1000, cost="$1000", stores=["NEW YORK"])
except ValidationError:
    pass

# Other nice things include post_init_post_parse which happens after validation


pprint.pprint(fr.__pydantic_model__.schema())
# {'properties': {'code': {'maxLength': 2,
#                          'minLength': 2,
#                          'title': 'Code',
#                          'type': 'string'},
#                 'cost': {'multipleOf': 1000,
#                          'title': 'Cost',
#                          'type': 'integer'},
#                 'population': {'default': 0,
#                                'multipleOf': 1000,
#                                'title': 'Population',
#                                'type': 'integer'},
#                 'revenue': {'multipleOf': 1000,
#                             'title': 'Revenue',
#                             'type': 'integer'},
#                 'stores': {'default': [],
#                            'items': {'type': 'string'},
#                            'maxItems': 10,
#                            'minItems': 0,
#                            'title': 'Stores',
#                            'type': 'array'}},
#  'required': ['code', 'revenue', 'cost'],
#  'title': 'Country',
#  'type': 'object'}

# Also has email and name types - handy for API's 

# Gotchas? ....