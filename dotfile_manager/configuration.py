from __future__ import annotations

from pathlib import Path
from typing import List

from dotfile_manager.dotfile import Dotfile
from dotfile_manager.json_class import JsonSerializable
from dotfile_manager.messages import info
from dotfile_manager.script import Script


class Configuration(JsonSerializable):
    def __init__(self, name: str, dotfiles: List[Dotfile], scripts: List[Script], verbose: bool = False):
        self.name = name
        self.dotfiles = dotfiles
        self.scripts = scripts

        super().__init__(verbose)

        if verbose:
            info("Loaded configuration `{}`.".format(name))

    def to_dict(self):
        return {
            "name": self.name,
            "dotfiles": JsonSerializable.to_list(self.dotfiles),
            "scripts": JsonSerializable.to_list(self.scripts)
        }

    @staticmethod
    def from_dict(dictionary: dict, verbose: bool = False) -> Configuration:
        keys = ("name", "dotfiles", "scripts")

        if not JsonSerializable.keys_are_valid(keys, dictionary):
            raise InvalidConfigurationJsonObject(
                "Invalid configuration json object: {}".format(dictionary)
            )

        return Configuration(
            name=dictionary["name"],
            dotfiles=Dotfile.from_list(dictionary["dotfiles"], verbose),
            scripts=Script.from_list(dictionary["scripts"], verbose),
            verbose=verbose
        )

    @staticmethod
    def from_list(json_list: List[dict], verbose: bool = False):
        return [Configuration.from_dict(config, verbose) for config in json_list]

    def build(self, configuration_path: Path):
        # todo: check if config directory exists

        # build dotfiles
        for dotfile in self.dotfiles:
            if dotfile.active:
                dotfile.build(configuration_path)
            elif self.verbose:
                info("Skipping dotfile `{}`.".format(dotfile.target))

        # build scripts
        for script in self.scripts:
            script.build(configuration_path)


class InvalidConfigurationJsonObject(Exception):
    def __init__(self, message: str):
        self.message = message
