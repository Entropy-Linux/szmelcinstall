# SzmelcInstall
> ### *Archinstall fork for Entropy Linux*
> ## Version: 13
> Rebased onto upstream **archinstall 4.4** (Textual TUI).

---

# Screenshots
> *Captured before the 4.4 Textual rewrite — the layout differs, the features do not.*
>
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
- Install-from-ISO with two modes: **Configs** (safe, curated includes/excludes) or **Configs + Live Cache** (bring almost everything from the live session). Configs live in `config/install_from_iso.json` and `config/install_from_iso_cache.json`. Both modes copy dotfiles, themes/icons/fonts, `/etc/skel`, and reinstall the live ISO package set while skipping machine IDs and other bad state.
- Entropy Tweaks: Install-from-ISO mode selector and Szmelc AUR repo toggle (Optional/TrustAll, `packages.szmelc.com`).
- Custom script hook (toggle in Entropy Tweaks): runs `custom.sh` stages before/after major steps. Edit `archinstall/custom.sh` to add per-stage commands; missing or commented stages are skipped.
- Entropy profile family (Baseline, Server, Desktop PRO/LITE) with JSON metadata in `config/entropy/profiles` and runner `default_profiles/entropy-profiles.py`.
- JSON-driven Entropy kits, Szmelc config packs, asset packs, and Szmelc package picker under Entropy Tweaks (merges include/exclude packages, config copies, and post-commands).
- Arch Tweaks: yay (from Chaotic AUR via pacman) and Chaotic AUR repo setup with interactive retry/force/skip/stop.
- Halt-and-ask error recovery instead of aborting the install: package conflicts, missing targets, file conflicts and
  unsatisfiable dependencies each pause with numbered choices (keep one, keep neither, drop a package, overwrite files),
  plus **Resolve manually in a shell** and **Exit** on every prompt. Unanswered prompts fall back to the safe choice after
  60 seconds; where nothing is safe to pick, the installer waits instead of guessing. Everything skipped is re-listed at the end.
- TUI: Entropy-branded header, Entropy/Arch Tweaks pinned to the top of the main menu, F1 help panel (upstream 4.4 Textual TUI).

---

# How to use (brief)
1) Boot the Entropy live ISO, run `sudo python -m archinstall`.
2) Configure language, disks, profile, network, users, etc.
3) Open **Entropy Tweaks**:
   - **Install from ISO**: pick **Configs** (default) or **Configs + Live Cache**; pick **Disabled** to skip. Edit the JSON files if you want different include/exclude lists.
   - **Szmelc AUR**: leave on to add the repo automatically.
   - **Custom script**: enable to run `custom.sh` stages. Each stage (1–10) corresponds to before/after initialization, user config, pre-install, installation, and post-install. Commands run with `stage` env set to the stage name.
   - **Entropy kits**: select JSON-defined kits (dev, network, creator, gaming) from `config/entropy/kits`.
   - **Szmelc packages/configs/assets**: pick packages from the Szmelc repo plus optional config and asset packs (`config/entropy/configs`, `config/entropy/assets`).
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
- Press F1 for the key-binding help panel; `INFO.md` documents the fork itself.
- When a package step fails, the installer halts and prints numbered options. Option "Resolve manually in a shell" drops you to
  `$SHELL` with the installation paused, and asks whether to resume once you leave it. "Exit" offers to save your configuration first.
- Leave a prompt unanswered for 60 seconds and it takes the safe option so an unattended install keeps moving.

---

# TO-DO
> - Improve "Install from ISO" feature for more granular control \
> - Add feature to install without previously formatting partition (install on top of old system) \
> - Add "Repair", "Reinstall", "Backup" hooks \
> - Add "Clone drive/part" feature, to clone partitions \
> - Add feature to install from squashed fs and hook to squash partition \
> - Add extensive backup features, to and from URL or file. 
