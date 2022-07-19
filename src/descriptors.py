"""Dickens

Additional decorators implementing the descriptor interface.

"""
__version__ = '2.0.0'


class cachedproperty:
    """Non-data descriptor decorator implementing a read-only property
    which overrides itself on the instance with an entry in the
    instance's data dictionary, caching the result of the decorated
    property method.

    """
    def __init__(self, func):
        self.__func__ = func

    def __get__(self, instance, _type=None):
        if instance is None:
            return self

        setattr(instance, self.__func__.__name__, self.__func__(instance))

        # This descriptor is now overridden for this instance:
        return getattr(instance, self.__func__.__name__)


class classproperty:
    """Descriptor decorator implementing a class-level read-only
    property.

    """
    def __init__(self, func):
        self.__func__ = func

    def __get__(self, instance, cls=None):
        if cls is None:
            cls = type(instance)

        return self.__func__(cls)


class cachedclassproperty:
    """Descriptor decorator implementing a class-level, read-only
    property, which caches its results on the class(es) on which it
    operates.

    Inheritance is supported, insofar as the descriptor is never hidden
    by its cache; rather, it stores values under its access name with
    added underscores. For example, when wrapping getters named
    "choices", "choices_" or "_choices", each class's result is stored
    on the class at "_choices_"; decoration of a getter named
    "_choices_" would raise an exception.

    """
    class AliasConflict(ValueError):
        pass

    def __init__(self, func):
        self.__func__ = func
        self.__cache_name__ = '_{}_'.format(func.__name__.strip('_'))
        if self.__cache_name__ == func.__name__:
            raise self.AliasConflict(self.__cache_name__)

    def __get__(self, instance, cls=None):
        if cls is None:
            cls = type(instance)

        try:
            return vars(cls)[self.__cache_name__]
        except KeyError:
            result = self.__func__(cls)
            setattr(cls, self.__cache_name__, result)
            return result


class classonlymethod:
    """Descriptor decorator implementing a class method that cannot be
    accessed as an instance method.

    The resulting non-data descriptor may be overshadowed by instance
    data set under the same name.

    Otherwise, instance access raises AttributeError (and such that it
    is forwarded to and may be handled by the instance's __getattr__).

    """
    def __init__(self, func):
        self.__func__ = func

    def __get__(self, instance, owner):
        if instance is None:
            return self.__func__.__get__(owner)

        raise AttributeError(
            f"'{owner.__name__}' object has no such attribute "
            f"(method '{self.__func__.__qualname__}' is accessible "
            f"from '{owner.__name__}' class only)"
        )
