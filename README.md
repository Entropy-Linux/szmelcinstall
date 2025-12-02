# SzmelcInstall
> ### *Archinstall fork for Entropy Linux*
> ## Version: 10.3

---

# Features (what you get)
- Install-from-ISO with two modes: **Configs** (safe, curated includes/excludes) or **Configs + Live Cache** (bring almost everything from the live session). Configs live in `config/install_from_iso.json` and `config/install_from_iso_cache.json`. Both modes copy dotfiles, themes/icons/fonts, `/etc/skel`, and reinstall the live ISO package set while skipping machine IDs and other bad state.
- Entropy Tweaks: Install-from-ISO mode selector and Szmelc AUR repo toggle (Optional/TrustAll, `packages.szmelc.com`).
- Arch Tweaks: yay (from Chaotic AUR via pacman) and Chaotic AUR repo setup with interactive retry/force/skip/stop.
- Pacstrap conflict/missing handlers (remove/choose/force/skip, manual rename, strip version) with confirmation prompts.
- TUI niceties: Entropy-branded header, Ctrl+h help, Ctrl+i info (`INFO.md`), Entropy/Arch Tweaks pinned to the top.

---

# How to use (brief)
1) Boot the Entropy live ISO, run `sudo python -m archinstall`.
2) Configure language, disks, profile, network, users, etc.
3) Open **Entropy Tweaks**:
   - **Install from ISO**: pick **Configs** (default) or **Configs + Live Cache**; pick **Disabled** to skip. Edit the JSON files if you want different include/exclude lists.
   - **Szmelc AUR**: leave on to add the repo automatically.
4) Open **Arch Tweaks**:
   - **Install yay**: installs yay from Chaotic AUR.
   - **Chaotic AUR**: adds keys/keyring/mirrorlist with interactive error handling.
5) Continue the guided install. The installer will:
   - Pacstrap base + your profile, handling conflicts/missing packages interactively.
   - Copy live user/root homes per your mode, copy `/etc/skel`, and fix ownership.
   - Reinstall the live ISO package set on the target system.

---

# Tips
- Use **Configs + Live Cache** if you want browser caches and most live-session state; it still skips machine IDs, NetworkManager state, pacman local DB, and known problematic profiles.
- Tune the JSON configs to add/remove paths. Excludes are globbed recursively.
- Ctrl+h/Ctrl+i popups stay until Esc; put your own info in `INFO.md`.
- If any step fails (pacstrap/repos), prompts let you retry, force, skip, or stop with a clear “Chosen: … Continue? Y/n” confirmation.
