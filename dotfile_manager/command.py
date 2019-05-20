from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List

from dotfile_manager.json_class import JsonSerializable
from dotfile_manager.messages import info


class Command(JsonSerializable):
    def __init__(self, command: str, parameters: List[str], verbose: bool = False):
        self.command = command
        self.parameters = parameters

        super().__init__(verbose)

        if verbose:
            info("Loaded command `{} {}`".format(self.command, " ".join(self.parameters)))

    def to_dict(self):
        return {
            "command": self.command,
            "parameters": self.parameters
        }

    @staticmethod
    def from_dict(dictionary: dict, verbose: bool = False):
        keys = ("command", "parameters")

        if not JsonSerializable.keys_are_valid(keys, dictionary):
            raise InvalidCommandJsonObject(
                "Invalid command json object: {}".format(dictionary)
            )

        return Command(
            command=dictionary["command"],
            parameters=dictionary["parameters"],
            verbose=verbose
        )

    @staticmethod
    def from_list(object_list: List[dict], verbose: bool = False):
        return [Command.from_dict(command, verbose) for command in object_list]

    def build(self, configuration_path: Path = None):
        if self.verbose:
            info("Executing command `{} {}`.".format(self.command, " ".join(self.parameters)))

        subprocess.run([self.command] + self.parameters)

    @staticmethod
    def build_list(commands: List[Command]):
        for command in commands:
            command.build()


class InvalidCommandJsonObject(Exception):
    def __init__(self, message: str):
        self.message = message
