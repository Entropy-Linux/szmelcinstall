from __future__ import annotations

from collections.abc import Callable

from archinstall.lib.output import warn
from archinstall.lib.pacman import Pacman
from archinstall.lib.translationhandler import tr
from archinstall.tui.curses_menu import SelectMenu
from archinstall.tui.menu_item import MenuItem, MenuItemGroup
from archinstall.tui.result import ResultType
from archinstall.tui.types import FrameProperties, PreviewStyle

from .catalog import EntropyComponent, load_asset_packs, load_config_packs, load_kits


def _component_menu(
	loader: Callable[[], list[EntropyComponent]],
	current: list[str],
	title: str,
) -> list[str]:
	components = loader()
	if not components:
		warn(tr('No entries available for {}').format(title))
		return current

	items = []
	for comp in components:
		def _preview(item: MenuItem, c: EntropyComponent = comp) -> str | None:  # noqa: B023
			lines = []
			if c.description:
				lines.append(c.description)
			if preview := c.preview():
				lines.append(preview)
			return '\n'.join(lines) if lines else None

		items.append(MenuItem(comp.name, value=comp.id, preview_action=_preview))

	group = MenuItemGroup(items, checkmarks=True, sort_items=True, sort_case_sensitive=False)
	group.set_selected_by_value(current)

	result = SelectMenu[str](
		group,
		multi=True,
		allow_skip=True,
		preview_style=PreviewStyle.RIGHT,
		preview_size='auto',
		preview_frame=FrameProperties.max(tr('Info')),
		header=title,
	).run()

	match result.type_:
		case ResultType.Skip:
			return current
		case ResultType.Selection:
			return result.get_values()
		case ResultType.Reset:
			return []

	return current


def select_kits(current: list[str]) -> list[str]:
	return _component_menu(load_kits, current, tr('Entropy Kits'))


def select_config_packs(current: list[str]) -> list[str]:
	return _component_menu(load_config_packs, current, tr('Szmelc Config Packs'))


def select_asset_packs(current: list[str]) -> list[str]:
	return _component_menu(load_asset_packs, current, tr('Szmelc Asset Packs'))


def list_szmelc_packages() -> list[str]:
	try:
		output = Pacman.run('-Sl szmelc').decode(strip=False).splitlines()
	except Exception as err:
		warn(f'Unable to list Szmelc packages: {err}')
		return []

	packages = set()
	for line in output:
		parts = line.split()
		if len(parts) >= 2:
			packages.add(parts[1])

	return sorted(packages)


def select_szmelc_packages(current: list[str]) -> list[str]:
	packages = list_szmelc_packages()
	if not packages:
		warn(tr('No Szmelc packages available'))
		return current

	items = [MenuItem(pkg, value=pkg) for pkg in packages]
	group = MenuItemGroup(items, checkmarks=True, sort_items=True, sort_case_sensitive=False)
	group.set_selected_by_value(current)

	result = SelectMenu[str](
		group,
		multi=True,
		allow_skip=True,
		header=tr('Szmelc packages'),
		preview_style=PreviewStyle.NONE,
		preview_size='auto',
	).run()

	match result.type_:
		case ResultType.Skip:
			return current
		case ResultType.Selection:
			return result.get_values()
		case ResultType.Reset:
			return []

	return current
