import attr
"""
attrs is the Python package that will bring back the joy of writing classes by relieving you from the drudgery of implementing object protocols (aka dunder methods).

Its main goal is to help you to write concise and correct software without slowing down your code.
https://www.attrs.org/en/stable/
"""


# Validators 

def less_than_population(instance, attribute, value):
    if value > instance.population:
        raise ValueError(f"{attribute} must be under population")


@attr.s
class Country:
    code = attr.ib(validator=attr.validators.instance_of(str))
    population = attr.ib(validator=attr.validators.instance_of(int))
    customers = attr.ib(validator=[attr.validators.instance_of(int), less_than_population], default=0)

    # Options for validators include....
    #   matches_re
    #   in
    #   deep_iterable
    #   is_callable


fr = Country(code="FR", population=100)
print(fr.code)
# 'FR'

try:
    fr = Country(code="FR", population="75M")
except TypeError as e:
    print(e)
    
# population must be <class 'int'>
try:
    fr = Country(code="FR", population=75,customers = 100)
except ValueError as e:
    print(e)
# ...<function less_than_population at ...


# Sometimes attrs feels a little less slick than the others...
print(attr.asdict(fr,filter=attr.filters.exclude(attr.fields(Country).customers)))
# > {'code': 'FR', 'population': 100}


# Converters

@attr.s
class Country:
    code = attr.ib(validator=attr.validators.instance_of(str))
    population = attr.ib(converter=int,validator=attr.validators.instance_of(int))

fr = Country(code="FR", population="75")
print(fr.population)
# 75

try:
    fr = Country(code="FR", population="75M")
except ValueError as e:
    print(e)
    # invalid literal for int()...

# Slots


@attr.s(slots=True)
class Country:
    code = attr.ib(validator=attr.validators.instance_of(str))
    population = attr.ib(converter=int,validator=attr.validators.instance_of(int))

"""

"Their main advantage is that they use less memory on CPython 1 and are slightly faster.

However, they also come with several possibly surprising gotchas:"

    - You can't add attributes post init
    - Combining with non-slotted gets tricky
    - You can't monkeypatch
    - ...

"""

# Has the same conversion to dict / duple and frozen options as we've seen