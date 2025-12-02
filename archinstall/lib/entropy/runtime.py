from __future__ import annotations

from collections.abc import Callable

from archinstall.lib.args import ArchConfig

from .catalog import (
	EntropyComponent,
	EntropyPayload,
	build_payload,
	load_asset_packs,
	load_config_packs,
	load_kits,
	resolve_dependencies,
)


def _selected_components(ids: list[str], loader: Callable[[], list[EntropyComponent]]) -> list[EntropyComponent]:
	if not ids:
		return []

	components = loader()
	return resolve_dependencies(ids, components)


def payload_from_config(config: ArchConfig) -> EntropyPayload:
	components: list[EntropyComponent] = []
	components += _selected_components(config.entropy_kits, load_kits)
	components += _selected_components(config.entropy_config_packs, load_config_packs)
	components += _selected_components(config.entropy_asset_packs, load_asset_packs)

	payload = build_payload(components)

	if config.entropy_szmelc_packages:
		merged = set(payload.include_packages)
		merged.update(config.entropy_szmelc_packages)
		payload.include_packages = sorted(merged)

	return payload
