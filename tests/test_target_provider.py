from pathlib import Path

import pytest

from dsts.impl.target_selector import TargetProvider  # type: ignore


def test_from_path(missing_path: Path, develop_collection_path: Path, develop_target_path: Path) -> None:
    with pytest.raises(IOError):
        TargetProvider.from_path(missing_path)

    with pytest.raises(IOError):
        TargetProvider.from_path(develop_collection_path)

    develop_target = TargetProvider.from_path(develop_target_path)

    assert 'project' in develop_target
    assert all(key in ('title', 'version', 'dependencies#0', 'dependencies#1', 'dependencies#2', 'dependencies#3') for key in develop_target['project'])

    assert 'bootstrap' in develop_target
    assert all(key in ('main_collection',) for key in develop_target['bootstrap'])
