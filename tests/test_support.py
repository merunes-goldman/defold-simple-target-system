from configparser import ConfigParser
from functools import partial
from pathlib import Path

import pytest

from dsts.impl.target_selector import Support  # type: ignore


def test_ensure_file(missing_path: Path, core_base_target_path: Path) -> None:
    with pytest.raises(IOError):
        Support.ensure_file(missing_path)

    assert Support.ensure_file(core_base_target_path) == core_base_target_path


def test_path_to_base_path(missing_path: Path, core_base_target_path: Path, debug_base_target_path: Path) -> None:
    assert Support.path_to_base_path(missing_path) is None
    assert Support.path_to_base_path(core_base_target_path) is None
    assert Support.path_to_base_path(debug_base_target_path) is not None


def test_path_to_config(missing_path: Path, develop_collection_path: Path, core_base_target_path: Path, debug_base_target_path: Path) -> None:
    with pytest.raises(IOError):
        Support.path_to_config(missing_path)

    with pytest.raises(IOError):
        Support.path_to_config(develop_collection_path)

    core_config = Support.path_to_config(core_base_target_path)

    assert 'project' in core_config
    assert all(key in ('title', 'version') for key in core_config['project'])

    debug_config = Support.path_to_config(debug_base_target_path)

    assert 'project' in debug_config
    assert all(key in ('dependencies#0', 'dependencies#1') for key in debug_config['project'])


def test_config_to_project(core_base_target_path: Path, release_target_path: Path) -> None:
    core_config = Support.path_to_config(core_base_target_path)

    assert Support.config_to_project(core_config) is not None

    release_config = Support.path_to_config(release_target_path)

    assert Support.config_to_project(release_config) is None


def test_config_to_dependencies(core_base_target_path: Path, debug_base_target_path: Path) -> None:
    core_config = Support.path_to_config(core_base_target_path)

    assert len(list(Support.config_to_dependencies(core_config))) == 0

    debug_config = Support.path_to_config(debug_base_target_path)

    assert len(list(Support.config_to_dependencies(debug_config))) == 2


def test_copy_config(core_base_target_path: Path, debug_base_target_path: Path) -> None:
    empty_config_provider = partial(ConfigParser, allow_no_value=True)

    core_config = Support.path_to_config(core_base_target_path)

    assert Support.copy_config(core_config, empty_config_provider) == core_config
    assert Support.copy_config(core_config, empty_config_provider, exclude=('project',)) != core_config
    assert Support.copy_config(core_config, empty_config_provider, exclude=('title',)) != core_config
    assert Support.copy_config(core_config, empty_config_provider, exclude=('version',)) != core_config

    debug_config = Support.path_to_config(debug_base_target_path)

    assert Support.copy_config(debug_config, empty_config_provider) == debug_config
    assert Support.copy_config(debug_config, empty_config_provider, exclude=('project',)) != debug_config
    assert Support.copy_config(debug_config, empty_config_provider, exclude=('dependencies#',)) != debug_config


def test_merge_configs(core_base_target_path: Path, debug_base_target_path: Path) -> None:
    empty_config_provider = partial(ConfigParser, allow_no_value=True)

    core_config = Support.path_to_config(core_base_target_path)

    assert Support.merge_configs(core_config, empty_config_provider()) == core_config
    assert Support.merge_configs(core_config, empty_config_provider(), exclude=('project',)) != core_config
    assert Support.merge_configs(core_config, empty_config_provider(), exclude=('title',)) != core_config
    assert Support.merge_configs(core_config, empty_config_provider(), exclude=('version',)) != core_config

    debug_config = Support.path_to_config(debug_base_target_path)

    assert Support.merge_configs(debug_config, empty_config_provider()) == debug_config
    assert Support.merge_configs(debug_config, empty_config_provider(), exclude=('project',)) != debug_config
    assert Support.merge_configs(debug_config, empty_config_provider(), exclude=('dependencies#',)) != debug_config
