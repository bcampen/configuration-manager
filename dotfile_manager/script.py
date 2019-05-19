from __future__ import annotations

from typing import List

from dotfile_manager.command import Command
from dotfile_manager.json_class import JsonSerializable


class Script(JsonSerializable):
    def __init__(self, target: str, file: str, commands_before: List[Command], commands_after: List[Command]):
        self.target = target
        self.file = file
        self.commands_before = commands_before
        self.commands_after = commands_after

    def to_dict(self):
        return {
            "target": self.target,
            "file": self.file,
            "commands_before": [command.to_dict() for command in self.commands_before],
            "commands_after": [command.to_dict() for command in self.commands_after],
        }

    @staticmethod
    def from_dict(json_dict: dict) -> Script:
        keys = ("target", "file", "commands_before", "commands_after")

        if not JsonSerializable.keys_are_valid(keys, json_dict):
            raise InvalidScriptJsonObject(
                "Invalid script json object: {}".format(json_dict)
            )

        return Script(
            target=json_dict["target"],
            file=json_dict["file"],
            commands_before=[command.from_dict() for command in json_dict["commands_before"]],
            commands_after=[command.from_dict() for command in json_dict["commands_after"]]
        )

    @staticmethod
    def from_list(json_list: List[dict]):
        return [Script.from_dict(script) for script in json_list]

    def build(self, configuration_path: str, dry_run: bool = False):
        pass


class InvalidScriptJsonObject(Exception):
    def __init__(self, message: str):
        self.message = message
