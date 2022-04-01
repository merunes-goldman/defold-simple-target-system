import os
import sys
from argparse import ArgumentParser
from collections import OrderedDict
from configparser import ConfigParser, DEFAULTSECT, ParsingError, SectionProxy
from functools import partial
from itertools import chain
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Union, cast


class Support:
    @staticmethod
    def ensure_file(path: Union[str, Path]) -> Path:
        path = Path(path)

        if not path.is_file():
            raise IOError(f"File does not exist at: {path.absolute()}")

        return path

    @staticmethod
    def path_to_base_path(path: Path) -> Optional[Path]:
        try:
            path = Support.ensure_file(path)
        except IOError:
            return None

        with open(path, 'r') as file:
            base_path = file.readline()

        if len(base_path) > 0 and base_path[0] == ';':
            return Path(path.parent, base_path[1:].strip())

        return None

    @staticmethod
    def path_to_config(path: Path) -> ConfigParser:
        path = Support.ensure_file(path)
        config = ConfigParser(allow_no_value=True)

        try:
            if os.fspath(path) not in config.read(path):
                raise IOError(f"Config is not valid at: {path.absolute()}")
        except ParsingError as e:
            raise IOError(f"Config is not valid at: {path.absolute()}") from e

        return config

    @staticmethod
    def config_to_project(config: ConfigParser) -> Optional[SectionProxy]:
        if 'project' in config:
            return config['project']

        return None

    @staticmethod
    def config_to_dependencies(config: ConfigParser) -> Iterable[str]:
        project = Support.config_to_project(config)

        if project is not None:
            for key in project:
                if 'dependencies#' in key:
                    yield project[key]

    @staticmethod
    def copy_config(src: ConfigParser, dst_provider: Callable[[], ConfigParser], *, exclude: Iterable[str] = ()) -> ConfigParser:
        dst, exclude = dst_provider(), list(exclude)

        for section in src:
            if section == DEFAULTSECT:
                continue

            exclude_section = next((True for exclude_entry in exclude if exclude_entry in section), False)

            if exclude_section:
                continue

            if not dst.has_section(section):
                dst.add_section(section)

            for key in src[section]:
                exclude_key = next((True for exclude_entry in exclude if exclude_entry in key), False)

                if exclude_key:
                    continue

                dst[section][key] = src[section][key]

        return dst

    @staticmethod
    def merge_configs(left: ConfigParser, right: ConfigParser, *, exclude: Iterable[str] = ()) -> ConfigParser:
        exclude = list(exclude)

        empty_config_provider = partial(ConfigParser, allow_no_value=True)
        left_over_empty_config_provider = partial(Support.copy_config, left, empty_config_provider, exclude=exclude)
        right_over_left_over_empty_config_provider = partial(Support.copy_config, right, left_over_empty_config_provider, exclude=exclude)

        return right_over_left_over_empty_config_provider()


class TargetProvider:
    @staticmethod
    def from_path(path: Path) -> ConfigParser:
        config = Support.path_to_config(path)
        base_path = Support.path_to_base_path(path)

        if base_path is not None:
            base_config = TargetProvider.from_path(Support.ensure_file(base_path))

            merged_config = Support.merge_configs(base_config, config, exclude=('dependencies#',))
            merged_project = Support.config_to_project(merged_config)
            merged_dependencies = OrderedDict.fromkeys(chain(Support.config_to_dependencies(base_config), Support.config_to_dependencies(config)))

            if merged_project is None:
                merged_config.add_section('project')
                merged_project = merged_config['project']

            for number, dependency in enumerate(merged_dependencies.keys()):
                merged_project[f"dependencies#{number}"] = dependency

            return merged_config

        return config


def _provide_target_path(args: List[str]) -> str:
    args_parser = ArgumentParser()
    args_parser.add_argument('target_path', type=str)

    args_namespace = args_parser.parse_args(args)

    return cast(str, args_namespace.target_path)


def _provide_game_project_path() -> Path:
    return Path('game.project')


def main(args: List[str]) -> None:
    target_path = Support.ensure_file(_provide_target_path(args))
    target = TargetProvider.from_path(target_path)

    game_project_path = _provide_game_project_path()
    game_project_path.unlink(missing_ok=True)

    with open(game_project_path, 'w') as game_project_file:
        target.write(game_project_file)


if __name__ == '__main__':
    main(sys.argv[1:])
