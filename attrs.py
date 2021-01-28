import attr

@attr.s
class Country:
    code : str
    population : int


fr = Country('FR',100)
print(fr)

breakpoint()



p


"Sub-classing is bad for you"