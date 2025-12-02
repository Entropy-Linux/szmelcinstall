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


class IsoInstallSubMenu(AbstractSubMenu[None]):
	def __init__(self, config: ArchConfig):
		self._config = config
		items = [
			MenuItem(
				text=tr('Configs'),
				value=config.iso_copy_configs,
				action=_toggle_bool,
				preview_action=lambda item: tr('Enabled') if item.value else tr('Disabled'),
				key='iso_copy_configs',
			),
			MenuItem(
				text=tr('Desktop'),
				value=config.iso_copy_desktop,
				action=_toggle_bool,
				preview_action=lambda item: tr('Enabled') if item.value else tr('Disabled'),
				key='iso_copy_desktop',
			),
			MenuItem(
				text=tr('Session Cache'),
				value=config.iso_copy_cache,
				action=_toggle_bool,
				preview_action=lambda item: tr('Enabled') if item.value else tr('Disabled'),
				key='iso_copy_cache',
			),
		]

		group = MenuItemGroup(items, checkmarks=True)
		super().__init__(group, config=config)


class EntropyTweaksMenu(AbstractSubMenu[None]):
	def __init__(self, config: ArchConfig):
		self._config = config

		def _open_iso_submenu(current: bool | None) -> bool:
			if not self._config.install_from_iso_enabled:
				self._config.install_from_iso_enabled = True
			IsoInstallSubMenu(self._config).run()
			return self._config.install_from_iso_enabled

		def _preview_install_from_iso(item: MenuItem) -> str:
			if not self._config.install_from_iso_enabled:
				return tr('Disabled')

			parts = []
			if self._config.iso_copy_configs:
				parts.append(tr('Configs'))
			if self._config.iso_copy_desktop:
				parts.append(tr('Desktop'))
			if self._config.iso_copy_cache:
				parts.append(tr('Session Cache'))
			return ', '.join(parts) if parts else tr('Enabled')

		items = [
			MenuItem(
				text=tr('Install from ISO'),
				value=config.install_from_iso_enabled,
				action=_open_iso_submenu,
				preview_action=_preview_install_from_iso,
				key='install_from_iso_enabled',
			),
			MenuItem(
				text=tr('Custom script (custom.sh)'),
				value=config.custom_script,
				action=_toggle_bool,
				preview_action=lambda item: tr('Enabled') if item.value else tr('Disabled'),
				key='custom_script',
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
