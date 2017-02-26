from django.db import models
from django.core.validators import MinValueValidator

def UnsignedIntField(*args, **kwargs):
    kwargs.setdefault('default', 0)
    kwargs.setdefault('validators', [MinValueValidator(0)])
    return models.IntegerField(*args, **kwargs)

def UnsignedBigIntField(*args, **kwargs):
    kwargs.setdefault('default', 0)
    kwargs.setdefault('validators', [MinValueValidator(0)])
    return models.BigIntegerField(*args, **kwargs)

def IntField(*args, **kwargs):
    kwargs.setdefault('default', 0)
    return models.IntegerField(*args, **kwargs)

def BigIntField(*args, **kwargs):
    kwargs.setdefault('default', 0)
    return models.BigIntegerField(*args, **kwargs)

