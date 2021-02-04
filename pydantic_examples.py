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


class Country(BaseModel):

    population: PositiveInt  # StrictInt means that the value passed would have to be an int
    code: constr(min_length=2, max_length=2)

    @validator("code")
    def is_alphanumeric(cls, v):
        if not v.isalpha():
            raise ValueError("Code must be alphanumeric")
        return v


fr = Country(population="123", code="FR")
fr = Country(population=123, code="FR")
fr2 = Country(population=123, code="FR")

# This isn't a dataclass but it behaves a lot like one
print(fr == fr2)

try:
    fr = Country(population=123, code="F1")
except ValidationError as e:
    print(e)
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
    code: constr(min_length=4)
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

# Gotchas? TBC