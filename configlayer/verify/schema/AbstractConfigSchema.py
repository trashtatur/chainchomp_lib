import abc

from schema import Schema


class AbstractConfigSchema(abc.ABC):

    def __init__(self):
        self.schema = self.init_schema()

    @abc.abstractmethod
    def init_schema(self) -> Schema:
        pass

    @classmethod
    @abc.abstractmethod
    def get_schema_dict(cls) -> dict:
        pass

