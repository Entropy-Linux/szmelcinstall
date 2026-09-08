from typing import TYPE_CHECKING, Self, override

from archinstall.default_profiles.profile import Profile, ProfileType, SelectResult
from archinstall.lib.entropy.apply import apply_payload
from archinstall.lib.entropy.catalog import EntropyComponent, build_payload, load_entropy_profiles
from archinstall.lib.log import info
from archinstall.lib.menu.helpers import Selection
from archinstall.tui.menu_item import MenuItem, MenuItemGroup
from archinstall.tui.result import ResultType

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
	def install(self, install_session: Installer) -> None:
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
	def __init__(self, current_selection: list[Self] | None = None) -> None:
		self._variants = [EntropyProfileVariant(comp) for comp in load_entropy_profiles()]

		super().__init__(
			'Entropy',
			ProfileType.Entropy,
			current_selection=current_selection or [],
			support_gfx_driver=True,
			support_greeter=True,
		)

		self._selected_variants: list[EntropyProfileVariant] = self._resolve_variants()

	def _resolve_variants(self) -> list[EntropyProfileVariant]:
		selected_names = {profile.name for profile in self.current_selection}
		return [variant for variant in self._variants if variant.name in selected_names]

	def _menu_items(self) -> MenuItemGroup:
		items = [
			MenuItem(
				profile.name,
				value=profile,
				preview_action=lambda x: x.value.preview_text() if x.value else None,
			)
			for profile in self._variants
		]

		group = MenuItemGroup(items, checkmarks=True, sort_items=True)
		group.set_selected_by_value(self.current_selection)
		if self.current_selection:
			group.set_focus_by_value(self.current_selection[0])
		return group

	@override
	async def do_on_select(self) -> SelectResult:
		group = self._menu_items()

		result = await Selection[Self](
			group,
			multi=True,
			allow_reset=True,
			allow_skip=True,
			preview_location='right',
		).show()

		match result.type_:
			case ResultType.Skip:
				return SelectResult.SameSelection
			case ResultType.Reset:
				self.current_selection = []
				self._selected_variants = []
				return SelectResult.ResetCurrent
			case ResultType.Selection:
				self.current_selection = result.get_values()
				self._selected_variants = self._resolve_variants()
				return SelectResult.NewSelection

	@override
	def install(self, install_session: Installer) -> None:
		variants = self._selected_variants

		if not variants:
			return

		components = [variant.component for variant in variants]
		info(f'Applying Entropy profiles: {", ".join([v.name for v in variants])}')
		payload = build_payload(components)
		apply_payload(install_session, payload)


# Hide internal helper profile from automatic discovery
EntropyProfileVariant.__module__ = 'archinstall.default_profiles.entropy_internal'
