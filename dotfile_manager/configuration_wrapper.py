from __future__ import annotations

import json
import logging
import pathlib
from typing import List

from dotfile_manager.configuration import Configuration
from dotfile_manager.json_class import JsonSerializable


class ConfigurationWrapper(JsonSerializable):
    def __init__(self, configuration_path: str, configurations: List[Configuration]):
        self.configurations = configurations
        self.configuration_path = configuration_path
        logging.info("Finished loading configuration.")

    def to_dict(self):
        return [c.to_dict() for c in self.configurations]

    @staticmethod
    def from_dict(json_dict: dict) -> ConfigurationWrapper:
        keys = ("configuration_path", "configurations")

        if not JsonSerializable.keys_are_valid(keys, json_dict) or not isinstance(
                json_dict["configurations"], list):
            raise InvalidConfigurationWrapperJsonObject(
                "Invalid configuration wrapper json object {}".format(json_dict)
            )

        return ConfigurationWrapper(
            json_dict["configuration_path"],
            Configuration.from_list(json_dict["configurations"])
        )

    @staticmethod
    def from_list(json_list: List[dict]):
        return [ConfigurationWrapper.from_dict(wrapper) for wrapper in json_list]

    @staticmethod
    def from_json_file(file: str):
        file_path = pathlib.Path(file)

        if not file_path.is_file():
            raise FileNotFoundError(file_path.as_posix())

        with open(file_path.absolute()) as loaded_file:
            return ConfigurationWrapper.from_dict(json.load(loaded_file))

    def build(self, configuration_path: str = None, dry_run: bool = False):
        """Builds all configurations."""

        if not configuration_path:
            configuration_path = self.configuration_path

        for config in self.configurations:
            config.build(configuration_path, dry_run)


class InvalidConfigurationWrapperJsonObject(Exception):
    def __init__(self, message: str):
        self.message = message
