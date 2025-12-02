from archinstall.lib.translationhandler import tr
from archinstall.tui.curses_menu import SelectMenu
from archinstall.tui.menu_item import MenuItem, MenuItemGroup
from archinstall.tui.result import ResultType
from archinstall.tui.types import Alignment, Orientation

from ..args import ArchConfig
from ..menu.abstract_menu import AbstractSubMenu


def _toggle_bool(current: bool | None) -> bool:
	if current is None:
		return True
	return not current


class EntropyTweaksMenu(AbstractSubMenu[None]):
	def __init__(self, config: ArchConfig):
		self._config = config
		items = [
			MenuItem(
				text=tr('Install from ISO'),
				value=config.install_from_iso,
				action=_toggle_bool,
				preview_action=lambda item: tr('Enabled') if item.value else tr('Disabled'),
				key='install_from_iso',
			),
			MenuItem(
				text=tr('Szmelc AUR'),
				value=config.szmelc_aur,
				action=_toggle_bool,
				preview_action=lambda item: tr('Enabled') if item.value else tr('Disabled'),
				key='szmelc_aur',
			),
		]

		group = MenuItemGroup(items, checkmarks=True)
		super().__init__(group, config=config)


class ArchTweaksMenu(AbstractSubMenu[None]):
	def __init__(self, config: ArchConfig):
		self._config = config
		items = [
			MenuItem(
				text=tr('Install yay'),
				value=config.install_yay,
				action=_toggle_bool,
				preview_action=lambda item: tr('Enabled') if item.value else tr('Disabled'),
				key='install_yay',
			),
			MenuItem(
				text=tr('Chaotic AUR'),
				value=config.chaotic_aur,
				action=_toggle_bool,
				preview_action=lambda item: tr('Enabled') if item.value else tr('Disabled'),
				key='chaotic_aur',
			),
		]

		group = MenuItemGroup(items, checkmarks=True)
		super().__init__(group, config=config)
