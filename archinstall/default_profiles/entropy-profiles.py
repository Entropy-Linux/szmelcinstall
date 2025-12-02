from __future__ import annotations

from typing import TYPE_CHECKING, override

from archinstall.default_profiles.profile import Profile, ProfileType, SelectResult
from archinstall.lib.entropy.apply import apply_payload
from archinstall.lib.entropy.catalog import EntropyComponent, build_payload, load_entropy_profiles
from archinstall.lib.output import info
from archinstall.lib.translationhandler import tr
from archinstall.tui.curses_menu import SelectMenu
from archinstall.tui.menu_item import MenuItem, MenuItemGroup
from archinstall.tui.result import ResultType
from archinstall.tui.types import FrameProperties, PreviewStyle

if TYPE_CHECKING:
	from archinstall.lib.installer import Installer


class EntropyProfileVariant(Profile):
	def __init__(self, component: EntropyComponent):
		super().__init__(
			component.name,
			ProfileType.EntropyVariant,
			packages=component.include_packages,
			support_gfx_driver=True,
			support_greeter=True,
		)
		self.component = component

	@override
	def install(self, install_session: 'Installer') -> None:
		info(f'Installing Entropy profile: {self.name}')
		payload = build_payload([self.component])
		apply_payload(install_session, payload)

	@override
	def preview_text(self) -> str:
		lines = []
		if self.component.description:
			lines.append(self.component.description)
		if preview := self.component.preview():
			lines.append(preview)
		return '\n'.join(lines)


class EntropyProfile(Profile):
	def __init__(self, current_selection: list[EntropyProfileVariant] | None = None) -> None:
		self._variants = [EntropyProfileVariant(comp) for comp in load_entropy_profiles()]

		super().__init__(
			'Entropy',
			ProfileType.Entropy,
			current_selection=current_selection or [],
			support_gfx_driver=True,
			support_greeter=True,
		)

	def _menu_items(self) -> MenuItemGroup:
		items = [
			MenuItem(
				profile.name,
				value=profile,
				preview_action=lambda item: item.value.preview_text(),
			)
			for profile in self._variants
		]

		group = MenuItemGroup(items, checkmarks=True, sort_items=True)
		group.set_selected_by_value(self.current_selection)
		if self.current_selection:
			group.focus_item = self.current_selection[0]
		return group

	@override
	def do_on_select(self) -> SelectResult:
		group = self._menu_items()

		result = SelectMenu[EntropyProfileVariant](
			group,
			multi=True,
			allow_reset=True,
			allow_skip=True,
			preview_style=PreviewStyle.RIGHT,
			preview_size='auto',
			preview_frame=FrameProperties.max(tr('Info')),
		).run()

		match result.type_:
			case ResultType.Skip:
				return SelectResult.SameSelection
			case ResultType.Reset:
				self.current_selection = []
				return SelectResult.ResetCurrent
			case ResultType.Selection:
				self.current_selection = result.get_values()
				return SelectResult.NewSelection

		return SelectResult.SameSelection

	@override
	def install(self, install_session: 'Installer') -> None:
		if not self.current_selection:
			return

		components = [profile.component for profile in self.current_selection]
		info(f'Applying Entropy profiles: {", ".join([p.name for p in self.current_selection])}')
		payload = build_payload(components)
		apply_payload(install_session, payload)


# Hide internal helper profile from automatic discovery
EntropyProfileVariant.__module__ = 'archinstall.default_profiles.entropy_internal'
