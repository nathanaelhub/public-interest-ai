from pathlib import Path


def test_readme_exists():
    assert (Path(__file__).parents[1] / "README.md").exists()
