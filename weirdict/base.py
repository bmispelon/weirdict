from abc import abstractproperty
from collections import MutableMapping, Mapping
from .decorators import apply_keyfunc
from functools import total_ordering
from itertools import repeat, izip


_SENTINEL = object()


@total_ordering
class AbstractNormalizedDict(MutableMapping):
    """A dictionary where keys are normalized through a given function
    before being inserted in the dict.
    
    """
    @abstractproperty
    def keyfunc(self):
        pass

    def __init__(self, map_or_seq=_SENTINEL, **kwargs):
        """Normalize the keys before delegating to the parent's constructor.
        The signature is (hopefully) the same as the one for dict.
        
        """
        if map_or_seq is _SENTINEL:
            args = []
        elif isinstance(map_or_seq, Mapping):
            args = [((self.keyfunc(k), v) for k, v in map_or_seq.items())]
        else: # sequence of two-tuples
            args = [((self.keyfunc(k), v) for k, v in map_or_seq)]

        kwargs = {self.keyfunc(k): v for k, v in kwargs.iteritems()}
        self._dict = dict(*args, **kwargs)

    def copy(self):
        return type(self)(self.iteritems())

    @apply_keyfunc
    def __getitem__(self, key):
        return self._dict[key]

    @apply_keyfunc
    def __setitem__(self, key, value):
        self._dict[key] = value

    @apply_keyfunc
    def __delitem__(self, key):
        del self._dict[key]

    @apply_keyfunc
    def has_key(self, key):
        return self._dict.has_key(key)

    def __len__(self):
        return len(self._dict)

    def __iter__(self):
        return iter(self._dict)

    def viewitems(self):
        return self._dict.viewitems()

    def viewkeys(self):
        return self._dict.viewkeys()

    def viewvalues(self):
        return self._dict.viewvalues()

    @classmethod
    def fromkeys(cls, seq, value=None):
        return type(self)(izip(seq, repeat(value)))

    def __cmp__(self, other):
        return cmp(self._dict, other)

    def __lt__(self, other):
        return self._dict < other