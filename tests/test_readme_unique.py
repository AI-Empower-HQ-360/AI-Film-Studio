"""Regression test to ensure the README hero section exists once."""
from pathlib import Path


def test_readme_hero_section_is_unique():
    """Ensure the hero heading exists and is not duplicated."""
    repo_root = Path(__file__).resolve().parents[1]
    readme = repo_root / "README.md"
    heading = "🎬 AI Film Studio — End-to-End SDLC (AWS + DevOps + Cloud + AI)"

    content = readme.read_text(encoding="utf-8")

    assert heading in content, "Expected hero section heading missing from README.md"
    assert (
        content.count(heading) == 1
    ), "Hero section heading appears multiple times in README.md"
