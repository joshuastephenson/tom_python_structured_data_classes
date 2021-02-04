from collections import namedtuple

# "used to create tuple-like objects that have fields accessible by attribute lookup as well as being indexable and iterable"
# https://docs.python.org/3/library/collections.html#collections.namedtuple

Country = namedtuple("Country", ["code", "population"], defaults=[None, 0])


france = Country("FR", 75)
japan = Country(code="JP", population=120)

print(france[0])
# > "FR"
fr_code = france.code
# > "FR"
code, population = france
print(len(france))
# > 2

for attribute in france:
    print(attribute)

# > 'FR'
# > 75

for fr, jp in zip(france, japan):
    print(fr, jp)

# > FR JP
# > 75 120


try:
    france.population = 76
except AttributeError:
    pass


Country = namedtuple("Country", ["code", "population"], defaults=[None, 0])
it = Country(code="IT")

print(it)
# > Country(code='IT', population=0)


from typing import NamedTuple

Country = NamedTuple("Country", [("code", str), ("population", int)])

fr = Country("FR", "60")
print(fr)

# > Country(code='FR', population='60')
# No type conversion / validation

Country = namedtuple("Country", ["code", "population"], defaults=[None, 0])
EmeaCountry = namedtuple("EmeaCountry", ["code", "population"], defaults=[None, 0])

# The underlying datastructure is a tuple. Which can lead to some - arguably - unexpected behavour such as different namedtuples being equal

fr = Country("FR", 60)
fr2 = Country("FR", 60)
fr3 = EmeaCountry("FR", 60)

print(fr == fr2 == fr3)
# > True
print(fr is fr2)
# > False

# You can't add methods without subclassing

