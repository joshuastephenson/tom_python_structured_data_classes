"""

- defaults
- mutability
- converters
- validation
- slotted


What do these do?

- Structure a group of values which need to be passed around

Why? 

- They provide some (very varying) level of validation
- Readability

FastApi + Pydantic as an example

Why not just use classes?

- Reduces boilerplate
- Quality by default

"""

from collections import namedtuple

# "used to create tuple-like objects that have fields accessible by attribute lookup as well as being indexable and iterable"
# https://docs.python.org/3/library/collections.html#collections.namedtuple

Country = namedtuple("Country", ["code", "population"], defaults=[None, 0])


france = Country("FR", 75)
japan = Country(code="JP", population=120)

fr_code = france[0]
fr_code = france.code
code, population = france
print(len(france))
# 2

for attrib in france:
    print(attrib)

# 'FR'
#  75

#france.population = 76

# AttributeError: can't see attribute

for fr, jp in zip(france, japan):
    print(fr, jp)

# FR JP
# 75 120

Country = namedtuple("Country", ["code", "population"], defaults=[None, 0])
it = Country(code="IT")

print(it)
# Country(code='IT', population=0)


from typing import NamedTuple

Country = NamedTuple("Country", [("code", str), ("population", int)])

fr = Country("FR", "60")
print(fr)

# No type conversion / validation
# Country(code='FR', population='60')

Country = namedtuple("Country", ["code", "population"], defaults=[None, 0])
EmeaCountry = namedtuple("EmeaCountry", ["code", "population"], defaults=[None, 0])

# The underlying datastructure is a tuple. Which can lead to some - arguably - unexpected behavour such as differnt naemdtuples being equal

fr = Country("FR", 60)
fr2 = Country("FR", 60)
fr3 = EmeaCountry("FR", 60)

print(fr == fr2 == fr3)
# True
print(fr is fr2)
# False

breakpoint()

# You can't add methods without subclassing
