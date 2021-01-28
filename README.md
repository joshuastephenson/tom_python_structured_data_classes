Dataclasses 

frozen
default
totuple
todoict
validators
converters
slotted
programmatic creation



Dataclasses (including, Pydantic Dataclasses v's Attrs v's NamedTuple v's TypedDict
'Structured Data Types'

Also referencing, Pydantic DataClasses, DataClassesJson + Marshmellow

-------------------------------------------------------------------

- https://www.revsys.com/tidbits/dataclasses-and-attrs-when-and-why/
- Useful overview of attr's + dataclasses

Referring to 'structured data types' listed above "the most useful purpose is adding a certain degree of formalization to a group of values that need to be passed around".

Has a nice example of how if you want to pass a object without ^^^ then the typing gets messy

Use type validation of data as the key reason to use attrs and added converting (e.g changing '-1' to False) and 'slotted classes'.

Both dataclasses and attrs can be frozen

https://www.attrs.org/en/stable/examples.html#slots
Slotted classes. This means that a class uses 'slots' rather than a 'dict' under the hood like most python objects. This is faster but new things can't be added as there aren't slots for them.

--------------------------------------------------------------------

https://jackmckew.dev/dataclasses-vs-attrs-vs-pydantic.html

Essentially attrs can do frozen, default, totuple, todoict, validators, converters, slotted, programmatic creation

Dataclasses can't do the last 4
Pydantic can't do the last 2

This is not great quality - gets repr wrong - but good example of programmatic creation of attrs

Pydantic dataclasses will automatically convert input to the correct type when they can

------------------------------------------------------------------

https://news.ycombinator.com/item?id=20907803

Written by attrs developer. On dataclasses 'it's a fine library and if it stops you from abusing named tuples that's a huge win'

----------------------------------------------------------------
https://www.attrs.org/en/stable/why.html#data-classes

Part of attrs.

Why Not dataclasses?

Same attrs has more features and dataclasses has nothing attrs doesn't have

Why Not NamedTuples?

    Essentially argument is that tuples are a tuple not a class

    "Other often surprising behaviors include:

    Since they are a subclass of tuples, namedtuples have a length and are both iterable and indexable. That’s not what you’d expect from a class and is likely to shadow subtle typo bugs.

    Iterability also implies that it’s easy to accidentally unpack a namedtuple which leads to hard-to-find bugs. 3

    namedtuples have their methods on your instances whether you like it or not. 2

    namedtuples are always immutable. Not only does that mean that you can’t decide for yourself whether your instances should be immutable or not, it also means that if you want to influence your class’ initialization (validation? default values?), you have to implement __new__() which is a particularly hacky and error-prone requirement for a very common problem. 4

    To attach methods to a namedtuple you have to subclass it. And if you follow the standard library documentation’s recommendation of:...
    
    If you want a tuple with names, by all means: go for a namedtuple. 5 But if you want a class with methods, you’re doing yourself a disservice by relying on a pile of hacks that requires you to employ even more hacks as your requirements expand."

Why Not Hand-Written classes?

    "If you don’t care and like typing, we’re not gonna stop you.

    However it takes a lot of bias and determined rationalization to claim that attrs raises the mental burden on a project given how difficult it is to find the important bits in a hand-written class and how annoying it is to ensure you’ve copy-pasted your code correctly over all your classes.

    In any case, if you ever get sick of the repetitiveness and drowning important code in a sea of boilerplate, attrs will be waiting for you."

Says you shouldn't be using inheritance

---------------------------------------------------------------------

https://www.youtube.com/watch?v=FcVCfGJrkUQ

Good example of how post_init can be used to update values etc
InitVar is a field value that 

https://www.youtube.com/watch?v=Udz4jjd46ho

NamedTuples can be unpacked
NamedTuple has a _replace method where you can create a duplicate with different variables
Agrees that these can lead to bug

Tuple == NamedTuple

Tuples of different types with same values will also be true

Says of cons are attrs - not OOWTDI, only one way to do it; steep learning curve for advanced features

Says it's not necessarily a good idea to use inheritance for dataclasses

-------------------------------------------------------------------------

https://www.youtube.com/watch?v=T-TwcmT6Rcw

You can pass orderable to dataclasses

Makes good point that dataclasses handle equality check in the way people *probably* want

Actually v nice around 20 - 30 mins. 'I think the win in terms of code saved being very minor, but the win of quality by default is a nice win'

30 mins - shows how the implementation of frozen means that you can have some parts of a class being frozen
37 mins - gets on to some complex stuff

Shows how you can exclude people from the hash (but I thought he said earlier that the hash was set to none?) and not include in repr. And how you can add metadata

40 mins this is really good
with field(hash=false,repr=False,metadata={'units': 'bitcoin'})

Also shows dataclases default factory, how you get around mutable default arguments

And how you can order and have only some fields incluced by (I think) adding hash=False or compare=False to the fields

You can introspect the fields with field(instance)[0] and it will have the meta data

Challenges:
- Adding slots hasn't been done yet and is hard
- An immutable parents don't work great

-------------------------------------------------------------------------


https://realpython.com/python-data-classes/


Dataclasses provide repr and eq whereas for a plain class you would need to write them yourself

"A data class is a regular Python class. The only thing that sets it apart is that it has basic data model methods like .__init__(), .__repr__(), and .__eq__() implemented for you."

You can use make_dataclass
