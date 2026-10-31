"""Method registry — add a new exploit by dropping a module here."""
from .base import Method, Registry
from .checkm8 import Checkm8
from .usbliter8 import Usbliter8
from .session import Session

REGISTRY = Registry()
REGISTRY.add(Checkm8())
REGISTRY.add(Usbliter8())
REGISTRY.add(Session())

def all_methods():
    return REGISTRY.all()
