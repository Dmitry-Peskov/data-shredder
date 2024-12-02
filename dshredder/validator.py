from typing import Optional
from abc import ABC, abstractmethod


class BaseValidator(ABC):
    """
    Базовый абстрактный класс валидатора, с реализованной функциональностью дескриптора (методы получения и изменения значения).
    Для реализации собственного валидатора, достаточно наследовать данный класс и реализовать метод validate.
    """
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        raise NotImplemented("Не реализован метод validate")