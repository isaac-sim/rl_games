import builtins
import importlib
import sys

import pytest


def test_true():
    assert True


def test_vecenv_import_does_not_require_ray(monkeypatch):
    original_import = builtins.__import__

    def import_without_ray(name, *args, **kwargs):
        if name == "ray":
            raise ModuleNotFoundError("No module named 'ray'")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", import_without_ray)
    sys.modules.pop("rl_games.common.vecenv", None)

    vecenv = importlib.import_module("rl_games.common.vecenv")

    with pytest.raises(ImportError, match=r"install rl-games\[ray\]"):
        vecenv.RayVecEnv("unused", 1)
