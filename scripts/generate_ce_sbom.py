#!/usr/bin/env python3
"""Generate a deterministic CycloneDX SBOM for a Flyto2 Flow release tree."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

from packaging.utils import canonicalize_name

from audit_ce_dependencies import _load_overrides, _locked_requirements, _python_dependencies


SKIP_TREE_PARTS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "dist",
    "node_modules",
    "out",
}


def _release_tree_sha256(root: Path, output_path: Path) -> str:
    """Hash the stable release inputs without local caches or generated output."""
    digest = hashlib.sha256()
    files = sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.resolve() != output_path
        and not SKIP_TREE_PARTS.intersection(path.relative_to(root).parts)
    )
    for path in files:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        with path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                digest.update(chunk)
    return digest.hexdigest()


def _source_commit(root: Path, tree_sha256: str) -> str:
    """Resolve release provenance without any Cloud-export metadata."""
    github_sha = os.environ.get("GITHUB_SHA", "").strip()
    if re.fullmatch(r"[0-9a-fA-F]{40,64}", github_sha):
        return github_sha.lower()
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    commit = result.stdout.strip()
    if result.returncode == 0 and re.fullmatch(r"[0-9a-fA-F]{40,64}", commit):
        return commit.lower()
    return (tree_sha256 * 2)[:40]


def _npm_components(root: Path) -> list[dict]:
    lock = json.loads((root / "src/ui/web/frontend/package-lock.json").read_text(encoding="utf-8"))
    components = []
    for package_path, package in sorted(lock.get("packages", {}).items()):
        if not package_path:
            continue
        name = str(package.get("name") or package_path.rsplit("node_modules/", 1)[-1])
        version = str(package.get("version") or "unknown")
        component = {
            "type": "library",
            "bom-ref": f"pkg:npm/{quote(name, safe='@/')}@{quote(version, safe='')}",
            "name": name,
            "version": version,
            "purl": f"pkg:npm/{quote(name, safe='@/')}@{quote(version, safe='')}",
        }
        license_name = package.get("license")
        if license_name:
            component["licenses"] = [{"expression": str(license_name)}]
        integrity = str(package.get("integrity") or "")
        if integrity.startswith("sha512-"):
            try:
                digest = base64.b64decode(integrity[7:]).hex()
                component["hashes"] = [{"alg": "SHA-512", "content": digest}]
            except ValueError:
                pass
        components.append(component)
    return components


def _installed_python_components(root: Path) -> list[dict]:
    components = []
    for _, name, version, license_name in _python_dependencies(root, _load_overrides(root)):
        normalized = canonicalize_name(name)
        purl = f"pkg:pypi/{quote(normalized, safe='')}@{quote(version, safe='')}"
        components.append(
            {
                "type": "library",
                "bom-ref": purl,
                "name": name,
                "version": version,
                "purl": purl,
                "licenses": [{"expression": license_name}],
            }
        )
    return components


def _locked_python_component(requirement) -> dict:
    name = canonicalize_name(requirement.name)
    version = str(requirement.specifier).removeprefix("==") or "unresolved"
    purl = f"pkg:pypi/{quote(name, safe='')}@{quote(version, safe='')}"
    constraint = {"name": "flyto:declared_constraint", "value": str(requirement.specifier) or "*"}
    component = {
        "type": "library",
        "bom-ref": purl,
        "name": requirement.name,
        "version": version,
        "purl": purl,
    }
    component["properties"] = [constraint]
    return component


def _locked_python_components(root: Path) -> list[dict]:
    lock_path = root / "src/ui/web/backend/requirements-ce.lock"
    return [_locked_python_component(item) for item in _locked_requirements(lock_path)]


def _python_components(root: Path, *, installed_closure: bool) -> list[dict]:
    if installed_closure:
        return _installed_python_components(root)
    return _locked_python_components(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Flyto2 Flow release tree")
    parser.add_argument("--output", default="sbom.cdx.json")
    parser.add_argument(
        "--python-installed",
        action="store_true",
        help="include the installed transitive Python dependency closure",
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()
    boundary = json.loads((root / "FLOW_BOUNDARY.json").read_text(encoding="utf-8"))
    if boundary.get("schema") != "flyto.flow-boundary.v1":
        raise ValueError("FLOW_BOUNDARY.json has an unsupported schema")
    output_path = (root / args.output).resolve()
    tree_sha256 = _release_tree_sha256(root, output_path)
    source_commit = _source_commit(root, tree_sha256)
    components = _npm_components(root) + _python_components(
        root,
        installed_closure=args.python_installed,
    )
    components.sort(key=lambda item: item["bom-ref"])
    serial_seed = f"{source_commit}:{tree_sha256}".encode("utf-8")
    serial_hex = hashlib.sha256(serial_seed).hexdigest()[:32]
    serial = (
        f"urn:uuid:{serial_hex[:8]}-{serial_hex[8:12]}-4{serial_hex[13:16]}-a{serial_hex[17:20]}-{serial_hex[20:32]}"
    )
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": serial,
        "version": 1,
        "metadata": {
            "component": {
                "type": "application",
                "bom-ref": "pkg:github/flytohub/flyto-flow",
                "name": "flyto-flow",
                "version": source_commit[:12],
            },
            "properties": [
                {"name": "flyto:source_commit", "value": source_commit},
                {"name": "flyto:tree_sha256", "value": tree_sha256},
            ],
        },
        "components": components,
    }
    (root / args.output).write_text(json.dumps(sbom, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {args.output} with {len(components)} components")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
