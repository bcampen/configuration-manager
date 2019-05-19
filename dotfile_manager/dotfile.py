from __future__ import annotations

import logging
from typing import List
from pathlib import Path
from dotfile_manager.command import Command
from dotfile_manager.json_class import JsonSerializable
from dotfile_manager.messages import error


class Dotfile(JsonSerializable):
    def __init__(self, name: str, target: str, commands_before: List[Command], commands_after: List[Command],
                 parts: List[str], active: bool = True):
        self.name = name
        self.target = target
        self.commands_before = commands_before
        self.commands_after = commands_after
        self.parts = parts
        self.active = active

        for part in parts:
            logging.info("Loaded dotfile part `{}` of dotfile `{}`.".format(part, name))

        logging.info("Finished loading dotfile `{}`.".format(self.name))

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "target": self.target,
            "commands_before": [command.to_dict() for command in self.commands_before],
            "commands_after": [command.to_dict() for command in self.commands_after],
            "parts": self.parts,
            "active": self.active
        }

    @staticmethod
    def from_dict(json_dict: dict) -> Dotfile:
        keys = ("name", "target", "commands_before", "commands_after", "parts", "active")

        if not all(k in json_dict for k in keys):
            raise InvalidDotfileJsonObject(
                "Invalid dotfile json object: {}".format(json_dict)
            )

        return Dotfile(
            name=json_dict["name"],
            target=json_dict["target"],
            commands_before=Command.from_list(json_dict["commands_before"]),
            commands_after=Command.from_list(json_dict["commands_after"]),
            parts=json_dict["parts"],
            active=json_dict["active"]
        )

    @staticmethod
    def from_list(json_list: List[dict]):
        return [Dotfile.from_dict(dotfile) for dotfile in json_list]

    def build(self, configuration_path: str, dry_run: bool = False):
        target_path = Path(self.target)

        with open(target_path.expanduser(), "w", encoding="utf-8") as file:
            # merge all parts together to the dotfile
            for part in self.parts:
                part_file_path = Path(part)

                if not part_file_path.is_file():
                    error("Dotfile part {} not found.".format(part_file_path.expanduser()))

                # todo: add logic


class InvalidDotfileJsonObject(Exception):
    def __init__(self, message: str):
        self.message = message
