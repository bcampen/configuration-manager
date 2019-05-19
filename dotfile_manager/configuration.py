from __future__ import annotations

import logging
from typing import List

from dotfile_manager.dotfile import Dotfile
from dotfile_manager.json_class import JsonSerializable
from dotfile_manager.script import Script


class Configuration(JsonSerializable):
    def __init__(self, name: str, dotfiles: List[Dotfile], scripts: List[Script]):
        self.name = name
        self.dotfiles = dotfiles
        self.scripts = scripts
        logging.info("Loaded configuration `{}`.".format(name))

    def to_dict(self):
        return {
            "name": self.name,
            "dotfiles": JsonSerializable.to_list(self.dotfiles),
            "scripts": JsonSerializable.to_list(self.scripts)
        }

    @staticmethod
    def from_dictionary(dictionary: dict) -> Configuration:
        keys = ("name", "dotfiles", "scripts")

        if not JsonSerializable.keys_are_valid(keys, dictionary):
            raise InvalidConfigurationJsonObject(
                "Invalid configuration json object: {}".format(dictionary)
            )

        return Configuration(
            name=dictionary["name"],
            dotfiles=Dotfile.from_json_list(dictionary["dotfiles"]),
            scripts=Script.from_json_list(dictionary["scripts"])
        )

    @staticmethod
    def from_list(json_list: List[dict]):
        return [Configuration.from_dictionary(config) for config in json_list]

    def build(self, configuration_path: str, dry_run: bool = False):
        # todo: check if config directory exists

        # build dotfiles
        for dotfile in self.dotfiles:
            dotfile.build(configuration_path, dry_run)

        # build scripts
        for script in self.scripts:
            script.build(configuration_path, dry_run)


class InvalidConfigurationJsonObject(Exception):
    def __init__(self, message: str):
        self.message = message
