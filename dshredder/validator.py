import os
from abc import ABC, abstractmethod
from .error import UnsupportedFileFormatError, DirectoryDoesNotExistError


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


class FileFormatValidator(BaseValidator):

    def __init__(self, allowed_formats: list[str]):
        self.allowed_formats = allowed_formats

    def validate(self, value):
        if value not in self.allowed_formats:
            raise UnsupportedFileFormatError(value, self.allowed_formats)


class DirectoryPathValidator(BaseValidator):

    def validate(self, value):
        if not os.path.isdir(value):
            raise DirectoryDoesNotExistError(value)
