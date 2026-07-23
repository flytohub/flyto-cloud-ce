from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "check_docs.py"
SPEC = importlib.util.spec_from_file_location("check_docs", SCRIPT)
assert SPEC and SPEC.loader
check_docs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_docs)


def test_repository_documentation_contract() -> None:
    assert check_docs.check_repository(ROOT) == []


def test_broken_local_link_is_reported(tmp_path: Path) -> None:
    source = tmp_path / "README.md"
    source.write_text("[missing](docs/missing.md)\n", encoding="utf-8")

    errors = check_docs.check_markdown_links(tmp_path)

    assert errors == ["broken local link in README.md: docs/missing.md"]


def test_non_flyto2_email_domain_is_reported(tmp_path: Path) -> None:
    source = tmp_path / "README.md"
    source.write_text("Contact person@example.org\n", encoding="utf-8")

    errors = check_docs.check_email_domains(tmp_path)

    assert errors == ["non-Flyto2 email domain in README.md: person@example.org"]


def test_generated_dependency_docs_are_ignored(tmp_path: Path) -> None:
    dependency_readme = tmp_path / "node_modules" / "package" / "README.md"
    dependency_readme.parent.mkdir(parents=True)
    dependency_readme.write_text(
        "Contact person@example.org and see [missing](missing.md)\n",
        encoding="utf-8",
    )

    assert check_docs.check_markdown_links(tmp_path) == []
    assert check_docs.check_email_domains(tmp_path) == []
