import pprint

from pydantic import (
    BaseModel,
    constr,
    conint,
    conlist,
    PositiveInt,
    StrictInt,
    validator,
    ValidationError,

)

from pydantic.dataclasses import dataclass

"""

"Data validation and settings management using python type annotations. pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.
https://pydantic-docs.helpmanual.io/
"""


class Country(BaseModel):

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
    #   constr


    # The default types will attempt best effort conversion
    # There are also strict types such as StrictInt, StrictInt
    # which will not


# Conversion happens when possible
fr = Country(population="123", code="FR")

# Equality check works like a dataclass 
fr = Country(population=123, code="FR")
fr2 = Country(population=123, code="FR")
print(fr == fr2)
# > True


try:
    fr = Country(population=123, code="F1")
except ValidationError:
    pass
    # > Code must be alphanumeric (type=value_error)


pprint.pprint(fr.schema())
# {'properties': {'code': {'maxLength': 2,
#                          'minLength': 2,
#                          'title': 'Code',
#                          'type': 'string'},
#                 'population': {'exclusiveMinimum': 0,
#                                'title': 'Population',
#                                'type': 'integer'}},
#  'required': ['population', 'code'],
#  'title': 'Country',
#  'type': 'object'}

as_dict = fr.dict()

fr3 = Country.parse_obj(as_dict)


class Store(BaseModel):
    code: constr(min_length=4) # Also accepts regex
    revenue: conint(multiple_of=100)


class Country(BaseModel):
    code: constr(min_length=2, max_length=2)
    population: conint(multiple_of=1000)
    stores: conlist(Store, min_items=1, max_items=100)


fr_as_dict = {
    "code": "FR",
    "population": 1000,
    "stores": [
        {"code": "TOULON", "revenue": 100},
        {"code": "MONTPELLIER", "revenue": 100},
    ],
}

fr = Country.parse_obj(fr_as_dict)
# Country(code='FR', population=1000, stores=[Store(code='TOULON', revenue=100), Store(code='MONTPELLIER', revenue=100)])
fr_as_json = fr.json()
fr = Country.parse_raw(fr_as_json)

# Gotchas? ....