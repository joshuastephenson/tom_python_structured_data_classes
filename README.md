# Structured Data Classes in Python

## Why use any of these?

- Compared to dicts, lists etc they add structure, readability
- All have the option to add type annotations
- They are quicker to create than normal classes and have 'quality by default'

## A Few of the Options

- **NamedTuple**: tuples with names (and types if you want)
- **Attrs**: "the Python package that will bring back the joy of writing classes by relieving you from the drudgery of implementing object protocols (aka dunder methods)"; powerful but not especially intuitive or pretty
- **Dataclasses**: a friendlier version of attrs with some of the functionality removed, most notably validators including type checkers, converters and slots
- **DataclassesJSON**: an add-on to dataclasses which uses marshmellow to add json based functionality including type validation and conversion
- **Pydantic Dataclasses**: part of the Pydantic package which "enforces type hints at runtime, and provides user friendly errors when data is invalid"

-----------------------------------

| Option          | Power | Intuitiveness |
| --------------- | ----- | ------------- |
| Named Tuples    | 3     | 8             |
| Attrs           | 10    | 7             |
| Dataclasses     | 6     | 9            |
| DataclassesJSON | 7     | 7             |
| Pydantic Dataclasses | 9     | 9             |
