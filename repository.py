from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')
ID = TypeVar('ID')


class Repository(ABC, Generic[T, ID]):
    @abstractmethod
    def get_by_id(self, id: ID) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def add(self, entity: T) -> T:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, id: ID) -> None:
        pass


class InMemoryRepository(Repository[T, ID]):
    def __init__(self):
        self._entities: dict[ID, T] = {}
        self._next_id: int = 1

    def get_by_id(self, id: ID) -> Optional[T]:
        return self._entities.get(id)

    def get_all(self) -> List[T]:
        return list(self._entities.values())

    def add(self, entity: T) -> T:
        entity.id = self._next_id
        self._entities[self._next_id] = entity
        self._next_id += 1
        return entity

    def update(self, entity: T) -> T:
        self._entities[entity.id] = entity
        return entity

    def delete(self, id: ID) -> None:
        self._entities.pop(id, None)
