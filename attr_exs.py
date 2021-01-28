import attr


# Validators

def less_than_population(instance, attribute, value):
    if value > instance.population:
        raise ValueError(f"{attribute} must be under population")


@attr.s
class Country:
    code = attr.ib(validator=attr.validators.instance_of(str))
    population = attr.ib(validator=attr.validators.instance_of(int))
    customers = attr.ib(validator=[attr.validators.instance_of(int), less_than_population], default=0)


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

However they also come with several possibly surprising gotchas:"

    - You can't add attributes post init
    - Combining with non-slotted gets tricky
    - You can't monkeypatch
    - ...


"Sub-classing is bad for you"