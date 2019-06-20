from __future__ import annotations

from os import chmod
from pathlib import Path
from shutil import copyfile
from typing import List

from dotfile_manager.command import Command
from dotfile_manager.json_class import JsonSerializable
from dotfile_manager.messages import error, info


class Script(JsonSerializable):
    def __init__(self, target: str, file: str, commands_before: List[Command], commands_after: List[Command],
                 execute_flag: bool = False, verbose: bool = False):
        # todo: store the target path as Path object instead of a string
        self.target = target
        self.file = file
        self.commands_before = commands_before
        self.commands_after = commands_after
        self.execute_flag = execute_flag

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
        keys = ("target", "file", "commands_before", "commands_after", "execute_flag")

        if not JsonSerializable.keys_are_valid(keys, json_dict):
            raise InvalidScriptJsonObject(
                "Invalid script json object: {}".format(json_dict)
            )

        return Script(
            target=json_dict["target"],
            file=json_dict["file"],
            commands_before=[Command.from_dict(command) for command in json_dict["commands_before"]],
            commands_after=[Command.from_dict(command) for command in json_dict["commands_after"]],
            execute_flag=json_dict["execute_flag"],
            verbose=verbose
        )

    @staticmethod
    def from_list(json_list: List[dict], verbose: bool = False):
        return [Script.from_dict(script, verbose) for script in json_list]

    def build(self, configuration_path: Path):
        file_path = configuration_path / "scripts" / self.file

        # check if the given script file exists
        if not file_path.exists():
            error("{} does not exists".format(file_path), True)

        # execute before commands
        Command.build_list(self.commands_before)

        # create the directory tree
        target_path = Path(self.target).expanduser()
        target_path.parent.expanduser().mkdir(parents=True, exist_ok=True)

        # copy the script file
        dest = copyfile(str(file_path), str(target_path.expanduser()))

        if self.verbose:
            info("Copied script {} to {}.".format(file_path, dest))

        if self.execute_flag:
            chmod(target_path, 0o755)

        Command.build_list(self.commands_after)


class InvalidScriptJsonObject(Exception):
    def __init__(self, message: str):
        self.message = message
