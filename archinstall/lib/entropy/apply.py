import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from archinstall.lib.entropy.catalog import EntropyPayload, EntropySpec
from archinstall.lib.log import debug, info, warn

if TYPE_CHECKING:
	from archinstall.lib.installer import Installer


def _copy_spec(target_root: Path, spec: EntropySpec) -> None:
	if not spec.src.exists():
		warn(f'Skipping missing config source: {spec.src}')
		return

	dest = target_root / spec.dest.relative_to('/')
	dest.parent.mkdir(parents=True, exist_ok=True)

	debug(f'Copying {spec.src} -> {dest}')
	shutil.copy2(spec.src, dest)


def apply_payload(installation: Installer, payload: EntropyPayload) -> None:
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
