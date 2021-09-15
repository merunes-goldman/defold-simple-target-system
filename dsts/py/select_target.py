from argparse import ArgumentParser
from collections import OrderedDict
from configparser import ConfigParser, DEFAULTSECT
from itertools import chain
from pathlib import Path
from typing import Iterable, Optional, Union


def _ensure_path(path: Union[str, Path]) -> Path:
    path = Path(path)

    if not path.exists():
        raise IOError(f"File does not exist at: {path.absolute()}")

    return path


def _parse_parent_path(path: Path) -> Optional[Path]:
    with open(path, 'r') as target_file:
        parent_source = target_file.readline()

    if parent_source[0] != ';':
        return None

    return Path(path.parent, parent_source[1:].strip())


def _provide_dependencies(config: ConfigParser) -> Iterable[str]:
    for section in config:
        if section == DEFAULTSECT:
            continue

        for key in config[section]:
            if section == 'project' and 'dependencies#' in key:
                yield config[section][key]


def _inner_merge_configs(left: ConfigParser, right: ConfigParser) -> ConfigParser:
    merged = ConfigParser(allow_no_value=True)

    def merge_(source_: ConfigParser) -> None:
        for section_ in source_:
            if section_ == DEFAULTSECT:
                continue

            if not merged.has_section(section_):
                merged.add_section(section_)

            for key_ in source_[section_]:
                if section_ == 'project' and 'dependencies#' in key_:
                    continue

                merged[section_][key_] = source_[section_][key_]

    merge_(left)
    merge_(right)

    return merged


def _provide_config(path: Path) -> ConfigParser:
    config = ConfigParser(allow_no_value=True)
    config.read(path)

    parent_path = _parse_parent_path(path)

    if parent_path is not None:
        parent_config = _provide_config(_ensure_path(parent_path))
        merged_config = _inner_merge_configs(parent_config, config)

        if not merged_config.has_section('project'):
            merged_config.add_section('project')

        dependencies = OrderedDict.fromkeys(chain(_provide_dependencies(parent_config), _provide_dependencies(config)))

        for number, dependency in enumerate(dependencies.keys()):
            merged_config['project'][f"dependencies#{number}"] = dependency

        return merged_config

    return config


def _main() -> None:
    args_parser = ArgumentParser()
    args_parser.add_argument('target_path', type=str)
    args = args_parser.parse_args()

    target_config = _provide_config(_ensure_path(args.target_path))

    project_path = Path('game.project')
    project_path.unlink(missing_ok=True)

    with open(project_path, 'w') as project_file:
        target_config.write(project_file)


if __name__ == '__main__':
    _main()
