import pytest
from app.client import parse_repo_target

def test_parse_repo_target_simple():
    target = parse_repo_target("fastapi/fastapi")
    assert target.owner == "fastapi"
    assert target.repo == "fastapi"

def test_parse_repo_target_url():
    target = parse_repo_target("https://github.com/pallets/flask")
    assert target.owner == "pallets"
    assert target.repo == "flask"

def test_parse_repo_target_url_git_suffix():
    target = parse_repo_target("https://github.com/psf/requests.git")
    assert target.owner == "psf"
    assert target.repo == "requests"

def test_parse_repo_target_invalid():
    with pytest.raises(ValueError):
        parse_repo_target("invalid_target_without_slash")
