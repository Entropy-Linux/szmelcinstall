# SzmelcInstall
> ### *Archinstall fork for Entropy Linux*
> ## Version: 12

---

# Screenshots
> ### **Main TUI layout**
> <img width="329" height="403" alt="image" src="https://github.com/user-attachments/assets/4a7d14e7-fba5-4cd4-91b7-2f9416413a78" />
> 
> ---
> ### **"Install from ISO" types**
> <img width="199" height="99" alt="image" src="https://github.com/user-attachments/assets/2339e4c5-c65c-4348-8119-f393ccafd97e" />
> 
> ---
> ### **Extended Error Handling**
> <img width="475" height="250" alt="image" src="https://github.com/user-attachments/assets/742a5323-1aa5-45d5-8e62-61f254ab0592" />
> 
> ---

---

# Features (what you get)
- Install-from-ISO is now one toggle with a submenu of checkboxes: **Configs**, **Desktop**, **Session Cache** (defaults: Configs+Desktop on, Session Cache off). Unified config lives in `config/install_from_iso.json` with per-group includes/excludes and package-to-path mappings; `/etc/skel` is always copied and the live ISO package set is reapplied to the target.
- Entropy Tweaks: Install-from-ISO selector and Szmelc AUR repo toggle (Optional/TrustAll, `packages.szmelc.com`).
- Custom script hook (toggle in Entropy Tweaks): runs `custom.sh` stages before/after major steps. Edit `archinstall/custom.sh`; commented or missing stages are skipped.
- Arch Tweaks: yay (from Chaotic AUR via pacman) and Chaotic AUR repo setup with interactive retry/force/skip/stop.
- Pacstrap conflict/missing handlers (remove/choose/force/skip, manual rename, strip version) with confirmation prompts.
- TUI niceties: Entropy-branded header, Ctrl+h help, Ctrl+i info (`INFO.md`), Entropy/Arch Tweaks pinned to the top.

---

# How to use (brief)
1) Boot the Entropy live ISO, run `sudo python -m archinstall`.
2) Configure language, disks, profile, network, users, etc.
3) Open **Entropy Tweaks**:
   - **Install from ISO**: Space toggles enable/disable; Enter opens the submenu. Check **Configs** (dotfiles, skel, core configs), **Desktop** (WM/DE configs, themes/icons/fonts), **Session Cache** (browser/app caches; still skips machine IDs and system state). Edit `config/install_from_iso.json` to adjust includes/excludes or package mappings.
   - **Szmelc AUR**: leave on to add the repo automatically.
   - **Custom script**: enable to run `custom.sh` stages. Each stage (1–10) corresponds to before/after initialization, user config, pre-install, installation, and post-install. Commands run with `stage` env set to the stage name.
4) Open **Arch Tweaks**:
   - **Install yay**: installs yay from Chaotic AUR.
   - **Chaotic AUR**: adds keys/keyring/mirrorlist with interactive error handling.
5) Continue the guided install. The installer will:
   - Pacstrap base + your profile, handling conflicts/missing packages interactively.
   - Copy live user/root homes per your mode, copy `/etc/skel`, and fix ownership.
   - Reinstall the live ISO package set on the target system.

---

# Tips
- Enable **Session Cache** if you want browser/app caches and most live-session state; it still skips machine IDs, NetworkManager state, pacman local DB, and known problematic profiles.
- Tune `config/install_from_iso.json` to add/remove paths or map packages to paths. Excludes are globbed recursively.
- Ctrl+h/Ctrl+i popups stay until Esc; put your own info in `INFO.md`.
- If any step fails (pacstrap/repos), prompts let you retry, force, skip, or stop with a clear “Chosen: … Continue? Y/n” confirmation.
