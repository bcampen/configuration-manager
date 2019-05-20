from __future__ import annotations

from pathlib import Path
from typing import List

from dotfile_manager.command import Command
from dotfile_manager.json_class import JsonSerializable


class Script(JsonSerializable):
    def __init__(self, target: str, file: str, commands_before: List[Command], commands_after: List[Command],
                 verbose: bool = False):
        self.target = target
        self.file = file
        self.commands_before = commands_before
        self.commands_after = commands_after

        super().__init__(verbose)

    def to_dict(self):
        return {
            "target": self.target,
            "file": self.file,
            "commands_before": [command.to_dict() for command in self.commands_before],
            "commands_after": [command.to_dict() for command in self.commands_after],
        }

    @staticmethod
    def from_dict(json_dict: dict, verbose: bool = False) -> Script:
        keys = ("target", "file", "commands_before", "commands_after")

        if not JsonSerializable.keys_are_valid(keys, json_dict):
            raise InvalidScriptJsonObject(
                "Invalid script json object: {}".format(json_dict)
            )

        return Script(
            target=json_dict["target"],
            file=json_dict["file"],
            commands_before=[Command.from_dict(command) for command in json_dict["commands_before"]],
            commands_after=[Command.from_dict(command) for command in json_dict["commands_after"]],
            verbose=verbose
        )

    @staticmethod
    def from_list(json_list: List[dict], verbose: bool = False):
        return [Script.from_dict(script, verbose) for script in json_list]

    def build(self, configuration_path: Path):
        # todo: add logic
        pass


class InvalidScriptJsonObject(Exception):
    def __init__(self, message: str):
        self.message = message
