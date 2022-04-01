from pathlib import Path

import pytest


def _d_example_path() -> Path:
    return Path('example')


def _d_base_targets_path() -> Path:
    return Path(_d_example_path(), 'base_targets')


def _d_bootstrap_path() -> Path:
    return Path(_d_example_path(), 'bootstrap')


def _develop_target_path() -> Path:
    return Path(_d_example_path(), 'develop.target')


@pytest.fixture
def missing_path() -> Path:
    return Path(_d_example_path(), 'missing.target')


@pytest.fixture
def core_base_target_path() -> Path:
    return Path(_d_base_targets_path(), 'core.base_target')


@pytest.fixture
def debug_base_target_path() -> Path:
    return Path(_d_base_targets_path(), 'debug.base_target')


@pytest.fixture
def develop_collection_path() -> Path:
    return Path(_d_bootstrap_path(), 'develop.collection')


@pytest.fixture
def release_collection_path() -> Path:
    return Path(_d_bootstrap_path(), 'release.collection')


@pytest.fixture
def develop_target_path() -> Path:
    return _develop_target_path()


@pytest.fixture
def release_target_path() -> Path:
    return Path(_d_example_path(), 'release.target')
