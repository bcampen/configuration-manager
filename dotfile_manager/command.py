from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List

from dotfile_manager.json_class import JsonSerializable


class Command(JsonSerializable):
    def __init__(self, command: str, parameters: List[str]):
        self.command = command
        self.parameters = parameters

    def to_dict(self):
        return {
            "command": self.command,
            "parameters": self.parameters
        }

    @staticmethod
    def from_dict(dictionary: dict):
        keys = ("command", "parameters")

        if not JsonSerializable.keys_are_valid(keys, dictionary):
            raise InvalidCommandJsonObject(
                "Invalid command json object: {}".format(dictionary)
            )

        return Command(
            command=dictionary["command"],
            parameters=dictionary["parameters"]
        )

    @staticmethod
    def from_list(object_list: List[dict]):
        return [Command.from_dict(command) for command in object_list]

    def build(self, source_path: Path, dry_run: bool = False):
        subprocess.run([self.command] + self.parameters)


class InvalidCommandJsonObject(Exception):
    def __init__(self, message: str):
        self.message = message
