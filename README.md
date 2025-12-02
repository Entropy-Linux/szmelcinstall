# SzmelcInstall
> ### *Archinstall fork for Entropy Linux*
> ## Version: 9

---

# Features:
- Install-from-ISO workflow uses configurable include/exclude lists (see config/install_from_iso.json) to copy curated dotfiles (zsh/bash/profile, configs, icons/themes, selected .local paths), skip noisy/stateful data (cache, pulse, zinit, machine-ids, etc.), copy /etc/skel, and install the live package set on the target (toggle in Entropy Tweaks).
- Szmelc AUR repository toggle (default on).
- Arch Tweaks: yay installer (now via Chaotic AUR pacman package) and Chaotic AUR repository setup (both default on) with interactive error handling.
- Interactive pacstrap handling for conflicts and missing packages (retry/choose/skip/force with confirmations).

---

# Screenshots:
<img width="529" height="603" alt="image" src="https://github.com/user-attachments/assets/aacda0c4-2193-4593-b59e-a340045822cf" />
