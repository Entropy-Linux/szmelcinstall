from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from archinstall.lib.output import debug, warn


BASE_PATH = Path(__file__).resolve().parents[2] / 'config' / 'entropy'
FILES_PATH = BASE_PATH / 'files'


@dataclass
class EntropySpec:
	src: Path
	dest: Path


@dataclass
class EntropyComponent:
	id: str
	name: str
	include_packages: list[str] = field(default_factory=list)
	exclude_packages: list[str] = field(default_factory=list)
	configs: list[EntropySpec] = field(default_factory=list)
	post_commands: list[str] = field(default_factory=list)
	dependencies: list[str] = field(default_factory=list)
	description: str | None = None
	category: str = ''

	def preview(self) -> str:
		parts: list[str] = []

		if self.include_packages:
			parts.append(f'Packages: {", ".join(sorted(self.include_packages))}')
		if self.exclude_packages:
			parts.append(f'Exclude: {", ".join(sorted(self.exclude_packages))}')
		if self.configs:
			parts.append(f'Configs: {len(self.configs)} file(s)')
		if self.post_commands:
			parts.append(f'Commands: {len(self.post_commands)}')
		if self.dependencies:
			parts.append(f'Deps: {", ".join(self.dependencies)}')

		return '\n'.join(parts)


@dataclass
class EntropyPayload:
	include_packages: list[str] = field(default_factory=list)
	configs: list[EntropySpec] = field(default_factory=list)
	post_commands: list[str] = field(default_factory=list)


def _resolve_src(meta_path: Path, src: str) -> Path:
	src_path = Path(src)
	if src_path.is_absolute():
		return src_path

	# prefer alongside the metadata file, then fall back to global files/ tree
	local = meta_path.parent / src_path
	if local.exists():
		return local

	return FILES_PATH / src_path


def _resolve_dest(dest: str) -> Path:
	dest_path = Path(dest)
	if dest_path.is_absolute():
		return dest_path
	return Path('/') / dest_path


def _load_components(kind: str) -> list[EntropyComponent]:
	components: list[EntropyComponent] = []
	kind_dir = BASE_PATH / kind

	if not kind_dir.exists():
		warn(f'Entropy metadata folder missing: {kind_dir}')
		return components

	for file in sorted(kind_dir.glob('*.json')):
		try:
			data = json.loads(file.read_text())
		except Exception as err:
			warn(f'Could not parse {file}: {err}')
			continue

		config_specs = []
		for entry in data.get('configs', []):
			src_val = entry.get('src')
			dest_val = entry.get('dest')
			if not src_val or not dest_val:
				warn(f'Skipping config entry without src/dest in {file}')
				continue

			config_specs.append(
				EntropySpec(
					_resolve_src(file, src_val),
					_resolve_dest(dest_val),
				),
			)

		component = EntropyComponent(
			id=data.get('id', file.stem),
			name=data.get('name', file.stem.replace('_', ' ').title()),
			include_packages=data.get('include_packages', []),
			exclude_packages=data.get('exclude_packages', []),
			configs=config_specs,
			post_commands=data.get('post_commands', []),
			dependencies=data.get('dependencies', []),
			description=data.get('description'),
			category=kind,
		)
		components.append(component)

	debug(f'Loaded {len(components)} {kind} definitions')
	return components


def load_entropy_profiles() -> list[EntropyComponent]:
	return _load_components('profiles')


def load_kits() -> list[EntropyComponent]:
	return _load_components('kits')


def load_config_packs() -> list[EntropyComponent]:
	return _load_components('configs')


def load_asset_packs() -> list[EntropyComponent]:
	return _load_components('assets')


def resolve_dependencies(selected_ids: list[str], components: list[EntropyComponent]) -> list[EntropyComponent]:
	lookup = {c.id: c for c in components}
	ordered: list[EntropyComponent] = []
	seen: set[str] = set()

	def _add(comp_id: str) -> None:
		if comp_id in seen:
			return

		comp = lookup.get(comp_id)
		if not comp:
			warn(f'Unknown dependency: {comp_id}')
			return

		for dep in comp.dependencies:
			_add(dep)

		seen.add(comp_id)
		ordered.append(comp)

	for item_id in selected_ids:
		_add(item_id)

	return ordered


def build_payload(components: Iterable[EntropyComponent]) -> EntropyPayload:
	include: set[str] = set()
	exclude: set[str] = set()
	configs: list[EntropySpec] = []
	post_commands: list[str] = []

	for comp in components:
		include.update(comp.include_packages)
		exclude.update(comp.exclude_packages)
		configs.extend(comp.configs)
		post_commands.extend(comp.post_commands)

	final_packages = sorted(include - exclude)
	return EntropyPayload(final_packages, configs, post_commands)
