#!/usr/bin/env python3
"""Validate the fail-closed Flyto2 Flow/Cloud repository sync contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


MANIFEST_NAME = "FLOW_CLOUD_SYNC.json"
EXPECTED_SCHEMA = "flyto.flow-cloud-sync.v2"
EXPECTED_FLOW_REPOSITORY = "flytohub/flyto-flow"
EXPECTED_CLOUD_REPOSITORY = "flytohub/flyto-cloud"
EXPECTED_MODE = "guarded-bidirectional-pull-request"
EXPECTED_CONTRACT = {
    "version": 2,
    "manifest_policy": "byte-identical",
    "source_ref_policy": "immutable-commit-sha",
    "target_ref_policy": "immutable-commit-sha",
    "path_policy": "exact-file-allowlist",
    "candidate_diff_policy": "exact-selected-paths",
    "change_unit": "pull-request",
    "conflict_policy": "fail-closed",
    "provenance_fields": [
        "source_repository",
        "source_sha",
        "source_manifest_sha256",
        "target_repository",
        "target_sha",
        "contract_version",
    ],
}
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


class ContractError(ValueError):
    """Raised when repository synchronization input violates the contract."""


def _string_list(value: Any, field: str, failures: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        failures.append(f"{field} must be a non-empty list")
        return []
    if not all(isinstance(item, str) and item for item in value):
        failures.append(f"{field} must contain only non-empty strings")
        return []
    if len(value) != len(set(value)):
        failures.append(f"{field} contains duplicate values")
    return value


def _safe_relative_path(value: str) -> bool:
    if "\\" in value:
        return False
    candidate = PurePosixPath(value)
    return (
        bool(value)
        and not candidate.is_absolute()
        and value == candidate.as_posix()
        and "." not in candidate.parts
        and ".." not in candidate.parts
    )


def _read_path_list(path: Path, field: str) -> list[str]:
    try:
        values = [line for line in path.read_text(encoding="utf-8").splitlines() if line]
    except OSError as exc:
        raise ContractError(f"cannot read {field}: {exc}") from exc
    failures: list[str] = []
    if len(values) != len(set(values)):
        failures.append(f"{field} contains duplicate paths")
    for value in values:
        if not _safe_relative_path(value):
            failures.append(f"{field} contains unsafe path: {value}")
    if failures:
        raise ContractError("\n".join(failures))
    return values


def _read_manifest(root: Path) -> tuple[Path, bytes, dict[str, Any]]:
    root = root.resolve()
    manifest_path = root / MANIFEST_NAME
    try:
        raw = manifest_path.read_bytes()
        manifest = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{MANIFEST_NAME} is unreadable or invalid: {exc}") from exc
    if not isinstance(manifest, dict):
        raise ContractError(f"{MANIFEST_NAME} must contain a JSON object")
    return root, raw, manifest


def _validate_manifest_identity(manifest: dict[str, Any], failures: list[str]) -> None:
    if manifest.get("schema") != EXPECTED_SCHEMA:
        failures.append(f"schema must be {EXPECTED_SCHEMA}")
    if manifest.get("flow_repository") != EXPECTED_FLOW_REPOSITORY:
        failures.append(f"flow_repository must be {EXPECTED_FLOW_REPOSITORY}")
    if manifest.get("cloud_repository") != EXPECTED_CLOUD_REPOSITORY:
        failures.append(f"cloud_repository must be {EXPECTED_CLOUD_REPOSITORY}")
    if manifest.get("mode") != EXPECTED_MODE:
        failures.append(f"mode must be {EXPECTED_MODE}")
    if manifest.get("canonical_baseline") != EXPECTED_FLOW_REPOSITORY:
        failures.append("Flyto2 Flow must remain the canonical shared baseline")
    if manifest.get("cloud_backports") != "allowlisted-shared-files-only":
        failures.append("Cloud backports must remain allowlisted shared files only")
    if manifest.get("contract") != EXPECTED_CONTRACT:
        failures.append("contract policy does not match the supported v2 protocol")


def _validate_shared_paths(
    root: Path,
    manifest: dict[str, Any],
    failures: list[str],
) -> list[str]:
    shared_paths = _string_list(manifest.get("shared_paths"), "shared_paths", failures)
    if shared_paths:
        if shared_paths[0] != MANIFEST_NAME:
            failures.append(f"shared_paths must start with {MANIFEST_NAME}")
        for value in shared_paths:
            if not _safe_relative_path(value):
                failures.append(f"unsafe shared path: {value}")
            elif not (root / value).is_file():
                failures.append(f"missing shared path: {value}")
    return shared_paths


def _validate_markers(manifest: dict[str, Any], failures: list[str]) -> None:
    markers = _string_list(
        manifest.get("forbidden_cloud_to_flow_markers"),
        "forbidden_cloud_to_flow_markers",
        failures,
    )
    if markers and markers != sorted(markers):
        failures.append("forbidden_cloud_to_flow_markers must be sorted")
    if any(marker != marker.lower() for marker in markers):
        failures.append("forbidden_cloud_to_flow_markers must be lowercase")


def _validate_required_gates(manifest: dict[str, Any], failures: list[str]) -> None:
    required_gates = manifest.get("required_gates")
    if not isinstance(required_gates, dict):
        failures.append("required_gates must be an object")
    else:
        _string_list(required_gates.get("flow"), "required_gates.flow", failures)
        _string_list(required_gates.get("cloud"), "required_gates.cloud", failures)


def _validate_license_policy(manifest: dict[str, Any], failures: list[str]) -> None:
    license_policy = manifest.get("license_policy")
    if not isinstance(license_policy, dict):
        failures.append("license_policy must be an object")
        return
    if license_policy.get("flow") != "PolyForm-Shield-1.0.0":
        failures.append("Flow license policy must remain PolyForm-Shield-1.0.0")
    if license_policy.get("cloud") != "Flyto2-Source-Available-1.1":
        failures.append("Cloud license policy must remain Flyto2-Source-Available-1.1")
    if not COMMIT_SHA.fullmatch(str(license_policy.get("historical_flow_boundary", ""))):
        failures.append("historical_flow_boundary must be a full commit SHA")


def _load_local(root: Path) -> dict[str, Any]:
    root, raw, manifest = _read_manifest(root)
    failures: list[str] = []
    _validate_manifest_identity(manifest, failures)
    shared_paths = _validate_shared_paths(root, manifest, failures)
    _validate_markers(manifest, failures)
    _validate_required_gates(manifest, failures)
    _validate_license_policy(manifest, failures)
    if failures:
        raise ContractError("\n".join(failures))
    return {
        "root": root,
        "raw": raw,
        "manifest": manifest,
        "manifest_sha256": hashlib.sha256(raw).hexdigest(),
        "shared_paths": shared_paths,
    }


def _validate_peer(snapshot: dict[str, Any], peer_root: Path | None) -> None:
    if peer_root is None:
        return
    peer = _load_local(peer_root)
    if snapshot["raw"] != peer["raw"]:
        raise ContractError("Flow and Cloud manifests must be byte-identical")


def _validate_source_identity(
    manifest: dict[str, Any],
    source_repository: str | None,
    source_sha: str | None,
) -> None:
    if (source_repository is None) != (source_sha is None):
        raise ContractError("source_repository and source_sha must be provided together")
    if source_repository is None:
        return
    allowed_repositories = {
        manifest["flow_repository"],
        manifest["cloud_repository"],
    }
    if source_repository not in allowed_repositories:
        raise ContractError(f"source_repository is not part of the contract: {source_repository}")
    if not COMMIT_SHA.fullmatch(source_sha or ""):
        raise ContractError("source_sha must be a full lowercase commit SHA")


def _validate_manifest_digest(
    snapshot: dict[str, Any],
    expected_manifest_sha256: str | None,
) -> None:
    if expected_manifest_sha256 is None:
        return
    if not SHA256.fullmatch(expected_manifest_sha256):
        raise ContractError("expected_manifest_sha256 must be a lowercase SHA-256 digest")
    if expected_manifest_sha256 != snapshot["manifest_sha256"]:
        raise ContractError("source manifest SHA-256 does not match the dispatched digest")


def _validate_contract_version(
    manifest: dict[str, Any],
    expected_contract_version: int | None,
) -> int:
    contract_version = manifest["contract"]["version"]
    if expected_contract_version is not None and expected_contract_version != contract_version:
        raise ContractError(
            f"contract version mismatch: expected {expected_contract_version}, found {contract_version}"
        )
    return contract_version


def _validate_candidate_paths(
    snapshot: dict[str, Any],
    candidate_paths: Path | None,
    expected_paths: Path | None,
) -> list[str]:
    selected_paths: list[str] = []
    if candidate_paths is not None:
        selected_paths = _read_path_list(candidate_paths, "candidate_paths")
        allowlist = set(snapshot["shared_paths"])
        unexpected = sorted(set(selected_paths) - allowlist)
        if unexpected:
            raise ContractError(f"candidate paths are outside the allowlist: {', '.join(unexpected)}")
    if expected_paths is None:
        return selected_paths
    if candidate_paths is None:
        raise ContractError("expected_paths requires candidate_paths")
    expected = _read_path_list(expected_paths, "expected_paths")
    if set(selected_paths) != set(expected):
        raise ContractError("candidate paths do not exactly match the selected paths")
    return selected_paths


def validate_contract(
    root: Path,
    *,
    peer_root: Path | None = None,
    source_repository: str | None = None,
    source_sha: str | None = None,
    expected_manifest_sha256: str | None = None,
    expected_contract_version: int | None = None,
    candidate_paths: Path | None = None,
    expected_paths: Path | None = None,
) -> dict[str, Any]:
    """Validate local, peer, provenance, and candidate-diff invariants."""
    snapshot = _load_local(root)
    manifest = snapshot["manifest"]
    _validate_peer(snapshot, peer_root)
    _validate_source_identity(manifest, source_repository, source_sha)
    _validate_manifest_digest(snapshot, expected_manifest_sha256)
    contract_version = _validate_contract_version(manifest, expected_contract_version)
    selected_paths = _validate_candidate_paths(snapshot, candidate_paths, expected_paths)

    return {
        "ok": True,
        "schema": manifest["schema"],
        "contractVersion": contract_version,
        "manifestSha256": snapshot["manifest_sha256"],
        "sharedPathCount": len(snapshot["shared_paths"]),
        "candidatePathCount": len(selected_paths),
        "sourceRepository": source_repository,
        "sourceSha": source_sha,
    }


def _write_github_output(path: Path, result: dict[str, Any]) -> None:
    values = {
        "contract_version": result["contractVersion"],
        "manifest_sha256": result["manifestSha256"],
        "shared_path_count": result["sharedPathCount"],
        "candidate_path_count": result["candidatePathCount"],
    }
    with path.open("a", encoding="utf-8") as output:
        for key, value in values.items():
            output.write(f"{key}={value}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--peer-root", type=Path)
    parser.add_argument("--source-repository")
    parser.add_argument("--source-sha")
    parser.add_argument("--expected-manifest-sha256")
    parser.add_argument("--expected-contract-version", type=int)
    parser.add_argument("--candidate-paths", type=Path)
    parser.add_argument("--expected-paths", type=Path)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    try:
        result = validate_contract(
            args.root,
            peer_root=args.peer_root,
            source_repository=args.source_repository,
            source_sha=args.source_sha,
            expected_manifest_sha256=args.expected_manifest_sha256,
            expected_contract_version=args.expected_contract_version,
            candidate_paths=args.candidate_paths,
            expected_paths=args.expected_paths,
        )
        if args.github_output is not None:
            _write_github_output(args.github_output, result)
    except ContractError as exc:
        print("Flow/Cloud synchronization contract failed:", file=sys.stderr)
        for failure in str(exc).splitlines():
            print(f" - {failure}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
