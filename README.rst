=======
dickens
=======

Additional Python decorators implementing the descriptor interface.

Like the built-in decorator, ``property``, these classes are initialized by and wrap a function, generally within the context of a class, in order to modify its behavior.

cached property
---------------

This decorator functions much like a read-only ``property``, with the difference that, upon access, it records its result in the instance's object data dictionary, which reference takes precedence in look-ups, thereby replacing itself for that object::

    @cachedproperty
    def circumference(self):
        return 2 * math.pi * self.radius

class property
--------------

A read-only ``property`` for class methods::

    @classproperty
    def badpi(cls):
        return 22 / 7

cached class property
---------------------

A class ``property``, which caches its result in the data dictionary of the class from which it was invoked, (under another name, so as not to interfere with inheritance of the property)::

    @cachedclassproperty
    def badpi(cls):
        return 22 / 7
