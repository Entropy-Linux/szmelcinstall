# SzmelcInstall
> ### *Archinstall fork for Entropy Linux*
> ## Version: 10

---

# Features:
- Install-from-ISO workflow now offers modes: **Configs** (default include/exclude in `config/install_from_iso.json`) or **Configs + Live Cache** (more permissive set in `config/install_from_iso_cache.json`). Both copy curated dotfiles, themes/icons/fonts, selected .local paths, /etc/skel, and install the live ISO package set while skipping machine IDs and known bad profiles.
- Szmelc AUR repository toggle (default on).
- Arch Tweaks: yay installer (now via Chaotic AUR pacman package) and Chaotic AUR repository setup (both default on) with interactive error handling.
- Interactive pacstrap handling for conflicts and missing packages (retry/choose/skip/force with confirmations).

---

# Screenshots:
<img width="529" height="603" alt="image" src="https://github.com/user-attachments/assets/aacda0c4-2193-4593-b59e-a340045822cf" />
