#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 17 December 2012 by Eiríkur Hallgrímsson
# Character geek: The 2nd and 3rd i in my name have diacriticals.
# If there is a file-encoding cookie, Python will accept this. (2.x, too)
# 18 December 2012 EH Added StrictDotDict which doesn't allow new keys.
# 28 March 2013 EH PEP-8 compliance, requested by RackSpace
"""Simple Library to hold the DotDict class."""


class DotDict(dict):
    """
    Enable use of Javascript/Coffeescript style object notation for dicts.
    The __missing__ method allows chaining creation of nested DotDicts:
    a = DotDict() ; a.foo.bar = 'content'
    Limitation: Expressing keys as attributes limits keys to valid Python
    identifiers.
    """
    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__

    def __setattr__(self, key, value):
        if hasattr(value, 'keys'):
            value = DotDict(value)
        self[key] = value

    def __missing__(self, key):
        self[key] = DotDict()
        return self[key]


class StrictDotDict(DotDict):
    """Strict form (subclass) of DotDict.  Does not allow new keys."""
    def __setattr__(self, key, value):
        if key in self:
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value
        else:
            raise KeyError

    # Fails PyLint for unused arguments, but this is the API.
    def __missing__(self, key):
        raise KeyError
