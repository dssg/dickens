"""Dickens

Additional decorators implementing the descriptor interface.

"""
import functools
import types


__version__ = '2.1.1'


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


class cachedproperty:
    """Non-data descriptor decorator implementing a read-only property
    which overrides itself on the instance with an entry in the
    instance's data dictionary, caching the result of the decorated
    property method.

    For example:

        class ClassyClass:

            @cachedproperty
            def once_per_instance(self):
                return self.a + self.b

            @cachedproperty.static
            def o_n_c_e__per_instance():
                return 2 ** 1_000

            once__p_e_r__instance = cachedproperty.static(expensive_func)

    The instance's cache may be cleared by simply deleting the instance
    attribute --

        classy = ClassyClass()

        classy.o_n_c_e__per_instance

        delattr(classy, 'o_n_c_e__per_instance')

    -- or by directly manipulating the instance's __dict__:

        del classy.__dict__['o_n_c_e__per_instance']

    """
    @classonlymethod
    def static(cls, func):
        @functools.wraps(func)
        def wrapper(_instance):
            return func()

        return cls(wrapper)

    def __init__(self, func):
        self.__func__ = func
        self.__doc__ = func.__doc__
        self.name = None

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name
            return

        if self.name != name:
            raise TypeError(
                f"cannot assign the same {self.__class__.__name__} to two different "
                f"names on {owner.__name__} ({self.name!r} and {name!r})"
            )

    @property
    def __name__(self):
        if self.name is None:
            return self.__func__.__name__

        return self.name

    def __get__(self, instance, _owner=None):
        if instance is None:
            return self

        try:
            cache = instance.__dict__
        except AttributeError:
            # not all objects have __dict__ (e.g. class defines slots)
            raise TypeError(
                f"instance of type {instance.__class__.__name__} does not define "
                f"'__dict__' with which to cache property {self.__name__}"
            ) from None

        value = self.__func__(instance)

        try:
            cache[self.__name__] = value
        except TypeError:
            raise TypeError(
                f"'__dict__' of instance of type {instance.__class__.__name__} does "
                f"not support item assignment for cache of property {self.__name__}"
            ) from None

        return value


# Conditional to support Python 3.8
if hasattr(types, 'GenericAlias'):
    cachedproperty.__class_getitem__ = classmethod(types.GenericAlias)
