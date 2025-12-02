from __future__ import annotations

import shutil
from pathlib import Path

from archinstall.lib.output import debug, info, warn

from .catalog import EntropyPayload, EntropySpec


def _copy_spec(target_root: Path, spec: EntropySpec) -> None:
	if not spec.src.exists():
		warn(f'Skipping missing config source: {spec.src}')
		return

	dest = target_root / spec.dest.relative_to('/')
	dest.parent.mkdir(parents=True, exist_ok=True)

	debug(f'Copying {spec.src} -> {dest}')
	shutil.copy2(spec.src, dest)


def apply_payload(installation: 'Installer', payload: EntropyPayload) -> None:  # type: ignore[name-defined]
	"""
	Apply packages/configs/commands described by a payload against an installation session.
	"""
	if payload.include_packages:
		info(f'Applying Entropy selections: {len(payload.include_packages)} package(s)')
		installation.add_additional_packages(payload.include_packages)

	for spec in payload.configs:
		_copy_spec(installation.target, spec)

	for cmd in payload.post_commands:
		info(f'Running Entropy command: {cmd}')
		installation.arch_chroot(cmd, peek_output=True)
