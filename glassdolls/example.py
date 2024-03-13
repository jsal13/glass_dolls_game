from collections.abc import Generator
from typing import Any


# Note: See here for args, kwargs typing.
# https://peps.python.org/pep-0484/#arbitrary-argument-lists-and-default-argument-values
def function_with_pep484_type_annotations(
    param1: int, param2: str, param3: str | None = None, *args: str, **kwargs: int
) -> bool:
    """Example function with PEP 484 type annotations.

    Args:
        param1: The first parameter.
        param2: The second parameter.
        param3 (str, optional): The second parameter. Defaults to None.
            Second line of description should be indented.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        bool: True if successful, False otherwise.

        The return type is optional and may be specified at the beginning of
        the ``Returns`` section followed by a colon.

        The ``Returns`` section may span multiple lines and paragraphs.
        Following lines should be indented to match the first line.

        The ``Returns`` section supports any reStructuredText formatting,
        including literal blocks::

            {
                'param1': param1,
                'param2': param2
            }

    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        ValueError: If `param2` is equal to `param1`.
    """
    if str(param1) == param2:
        err = "param1 may not be equal to param2"
        raise ValueError(err)
    return True


def example_generator(n: int) -> Generator[int, None, None]:
    """Generators have a ``Yields`` section instead of a ``Returns`` section.

    See https://docs.python.org/3.8/library/typing.html#typing.Generator
    for the ``Generator`` type reference.


    Args:
        n (int): The upper limit of the range to generate, from 0 to `n` - 1.

    Yields:
        int: The next number in the range of 0 to `n` - 1.

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> print([i for i in example_generator(4)])
        [0, 1, 2, 3]

    """
    yield from range(n)


class ExampleClass:
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (int), optional): Description of `attr2`.
        ...

    """

    def __init__(self, param1: str, param2: int, param3: list[str]):
        """Example of docstring on the __init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1 (str): Description of `param1`.
            param2 (int): Description of `param2`. Multiple
                lines are supported.
            param3 (list[str]): Description of `param3`.
        """
        self.attr1 = param1
        self.attr2 = param2
        self.attr3 = param3  #: Doc comment *inline* with attribute

        #: list of str: Doc comment *before* attribute, with type specified
        self.attr4 = ["attr4"]

        self.attr5 = None
        """str: Docstring *after* attribute, with type specified."""

    @property
    def readonly_property(self) -> str:
        """str: Properties should be documented in their getter method."""
        return "readonly_property"

    def example_method(self, param1: Any, param2: Any) -> bool:
        """Class methods are similar to regular functions.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1 (Any): The first parameter.
            param2 (Any): The second parameter.

        Returns:
            bool: True if successful, False otherwise.

        """
        return True

    def __special_without_docstring__(self) -> None:
        pass

    def _private_without_docstring(self) -> None:
        pass
