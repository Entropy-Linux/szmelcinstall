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
	INSTALL_FROM_ISO_MODES = {
		'configs': tr('Configs'),
		'configs_cache': tr('Configs + Live Cache'),
	}

	def __init__(self, config: ArchConfig):
		self._config = config

		def _select_install_from_iso_mode(current: str | None) -> str | None:
			current_mode = self._config.install_from_iso_mode or 'configs'
			options = [
				MenuItem(tr('Disabled'), value='off'),
				MenuItem(self.INSTALL_FROM_ISO_MODES['configs'], value='configs'),
				MenuItem(self.INSTALL_FROM_ISO_MODES['configs_cache'], value='configs_cache'),
			]
			group = MenuItemGroup(options, checkmarks=False)
			group.set_focus_by_value('configs' if not self._config.install_from_iso else current_mode)

			result = SelectMenu[str](
				group,
				header=tr('Install from ISO mode'),
				alignment=Alignment.CENTER,
				columns=1,
				orientation=Orientation.VERTICAL,
				search_enabled=False,
				allow_skip=False,
			).run()

			if result.type_ != ResultType.Selection:
				return current

			choice = result.item().value
			if choice == 'off':
				self._config.install_from_iso = False
				return current_mode

			self._config.install_from_iso = True
			self._config.install_from_iso_mode = choice
			return choice

		def _preview_install_from_iso(item: MenuItem) -> str:
			if not self._config.install_from_iso:
				return tr('Disabled')

			mode = item.value or 'configs'
			return self.INSTALL_FROM_ISO_MODES.get(mode, tr('Configs'))

		items = [
			MenuItem(
				text=tr('Install from ISO'),
				value=config.install_from_iso_mode,
				action=_select_install_from_iso_mode,
				preview_action=_preview_install_from_iso,
				key='install_from_iso_mode',
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
