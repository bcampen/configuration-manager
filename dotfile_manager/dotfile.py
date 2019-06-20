from __future__ import annotations

from pathlib import Path
from typing import List

from dotfile_manager.command import Command
from dotfile_manager.json_class import JsonSerializable
from dotfile_manager.messages import error, info


class Dotfile(JsonSerializable):
    def __init__(self, name: str, target: str, commands_before: List[Command], commands_after: List[Command],
                 parts: List[str], active: bool = True, verbose: bool = False):
        self.name = name
        self.target = target
        self.commands_before = commands_before
        self.commands_after = commands_after
        self.parts = parts
        self.active = active

        super().__init__(verbose)

        if verbose:
            info("Loaded dotfile `{}` with parts `{}`.".format(self.name, "`, `".join(parts)))

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
    def from_dict(json_dict: dict, verbose: bool = False) -> Dotfile:
        keys = ("name", "target", "commands_before", "commands_after", "parts", "active")

        if not all(k in json_dict for k in keys):
            raise InvalidDotfileJsonObject(
                "Invalid dotfile json object: {}".format(json_dict)
            )

        return Dotfile(
            name=json_dict["name"],
            target=json_dict["target"],
            commands_before=Command.from_list(json_dict["commands_before"], verbose),
            commands_after=Command.from_list(json_dict["commands_after"], verbose),
            parts=json_dict["parts"],
            active=json_dict["active"],
            verbose=verbose
        )

    @staticmethod
    def from_list(json_list: List[dict], verbose: bool = False):
        return [Dotfile.from_dict(dotfile, verbose) for dotfile in json_list]

    def build(self, configuration_path: Path):
        # execute commands before
        Command.build_list(self.commands_before)

        target_path = Path(self.target).expanduser()
        target_parent_directory = target_path.parent.expanduser()

        # create target directory tree (if not already done)
        if not target_parent_directory.is_dir():
            if self.verbose:
                info("Creating directory `{}`".format(target_parent_directory))

            target_parent_directory.mkdir(parents=True, exist_ok=True)

        with open(target_path, "w", encoding="utf-8") as file:
            parts_directory = configuration_path / "dotfiles" / Path(self.name)

            if not parts_directory.is_dir():
                error("`{}` is not a directory or does not exists.".format(parts_directory), True)

            # merge all parts together to the dotfile
            for part in self.parts:
                part_file_path = parts_directory.expanduser() / Path(part)

                if not part_file_path.is_file():
                    error("Dotfile part `{}` not found.".format(part_file_path.expanduser()), True)

                if self.verbose:
                    info("Merging `{}` into `{}`.".format(part_file_path, target_path))

                with open(part_file_path, encoding="utf-8") as part_file:
                    for line in part_file:
                        file.write("{}".format(line))

        # execute commands after
        Command.build_list(self.commands_after)


class InvalidDotfileJsonObject(Exception):
    def __init__(self, message: str):
        self.message = message
