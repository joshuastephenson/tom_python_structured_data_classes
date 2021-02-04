from dataclasses import dataclass
from dataclasses_json import dataclass_json
from marshmallow.exceptions import ValidationError
from pprint import pprint


@dataclass_json
@dataclass
class Country:
    code: str
    population: int


fr = Country("FR", 1)
print(fr)
# > Country(code='FR', population=1)

fr2 = Country("FR", "1")
print(fr2)
# > Country(code='FR', population='1')

fr3 = Country(code="FR", population="ONE")
print(fr3)
# > Country('FR','ONE')


fr = Country.schema().load({"code": "FR", "population": 1})
print(fr)
# > Country(code='FR', population=1)

fr2 = Country.schema().load({"code": "FR", "population": "1"})
print(fr2)
# > Country(code='FR', population=1)
# Type conversion!


try:
    fr3 = Country.schema().load({"code": "FR", "population": "ONE"})
except ValidationError as e:
    print(e)
    # > {'population': ['Not a valid integer.']}
# Type validation!

# Same with schema.dump() which transforms back to a dict

print([fr.to_json(), fr.to_dict()])
# > ['{"code": "FR", "population": 1}', {'code': 'FR', 'population': 1}]


# Gotcha?
# - Not at all obvious to load / dump via schema
# - Conversion not v intuitive - True will not --> 1
# - No apparent way of using the full Marshmellow functionality (e.g field must be email)
# - Not a lot of GH activity