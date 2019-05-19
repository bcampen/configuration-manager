from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class JsonSerializable(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        """Serializes this object to a json encodable python dictionary."""
        pass

    @staticmethod
    def to_list(object_list: List[JsonSerializable]):
        return [obj.to_dict() for obj in object_list]

    @staticmethod
    @abstractmethod
    def from_dict(dictionary: dict):
        """Deserialize a json dict to an object of this class."""
        pass

    @staticmethod
    @abstractmethod
    def from_list(object_list: List[dict]):
        """Deserialize a list of json dicts to a list of objects of this class."""
        pass

    @staticmethod
    def keys_are_valid(keys: tuple, json_dict: dict) -> bool:
        return all(key in json_dict for key in keys)

    @abstractmethod
    def build(self, source_path: Path, dry_run: bool = False):
        pass
