Entropy Linux Installer (szmelcinstall)

This installer is an Entropy-focused fork of archinstall.

Based on upstream archinstall 4.4 (Textual TUI).

Controls:
- F1: help panel (key bindings)
- Ctrl+q: quit

Notes:
- Entropy Tweaks and Arch Tweaks let you toggle distro-specific options (Install from ISO, Szmelc AUR, yay, Chaotic AUR).
- Package failures halt the install and prompt instead of exiting: keep one side of a conflict, keep neither, drop a package,
  overwrite conflicting files, resolve it by hand in a shell, or exit (optionally saving your configuration).
- Prompts auto-select the safe option after 60s; when no option is safe, the installer waits for you.
