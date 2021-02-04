# Structured Data Type in Python

## Why use any of these?

- Compared to dicts / lists they add structure, readability
- They are quicker to create than normal classes and have 'quality by default'

## A Few of the Options

- **NamedTuple**: tuples with names (and types if you want)
- **Attrs**: "the Python package that will bring back the joy of writing classes by relieving you from the drudgery of implementing object protocols (aka dunder methods)"; powerful but not especially intuitive or pretty
- **Dataclasses**: a friendlier version of attrs with some of the functionality removed, most notably validators including type checkers, converters and slots
- **DataclassesJSON**: an add-on to dataclasses which uses marshmellow to add json based functionality including type validation
- **Pydantic** Models: part of the Pydantic package which uses type annotations to bring type validation to Python

-----------------------------------

| Option          | Power    |  Intuitiveness   |
| --------------- | -------- | ---------------- |
| Named Tuples    |   3      |      8   |
| Attrs           |   10     |      7   |
| Dataclasses     |   6      |      10  |
| DataclassesJSON |   7      |      7   |
| Pydantic Models |   9      |      9   |
