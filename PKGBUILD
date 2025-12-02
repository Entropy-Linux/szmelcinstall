# Maintainer: sx66 <serainox@gmail.com>
# For Entropy Linux
# Forked from upstream archinstall PKGBUILD

pkgname=archinstall-entropy
pkgver=12
pkgrel=1
pkgdesc="Entropy Linux installer (archinstall fork) with Entropy/Szmelc customizations"
arch=(any)
url="https://github.com/Entropy-Linux/szmelcinstall"
license=(GPL-3.0-only)
depends=(
  'arch-install-scripts'
  'btrfs-progs'
  'coreutils'
  'cryptsetup'
  'dosfstools'
  'e2fsprogs'
  'glibc'
  'kbd'
  'libcrypt.so'
  'libxcrypt'
  'pciutils'
  'procps-ng'
  'python'
  'python-cryptography'
  'python-pydantic'
  'python-pyparted'
  'python-textual'
  'systemd'
  'util-linux'
  'xfsprogs'
  'lvm2'
  'f2fs-tools'
  'ntfs-3g'
)
makedepends=(
  'python-build'
  'python-installer'
  'python-setuptools'
  'python-sphinx'
  'python-wheel'
  'python-sphinx_rtd_theme'
  'python-pylint'
  'ruff'
)
optdepends=(
  'python-systemd: Adds journald logging'
)
provides=(archinstall-entropy archinstall install-entropy szmelcinstall python-archinstall)
conflicts=(archinstall archinstall-git)
replaces=(archinstall archinstall-git)
_gitname=szmelcinstall
_srcdir=${_gitname}-main
source=(
  $pkgname-$pkgver.tar.gz::$url/archive/refs/heads/main.tar.gz
)
sha512sums=('SKIP')
b2sums=('SKIP')

check() {
  echo "Skipping check() for archinstall-entropy (default nocheck mode)."
  return 0

  # Original check() kept below for reference (never executed):
  # cd "$srcdir/szmelcinstall-main"
  # python -m ruff check archinstall || true
  # pytest || true
}

build() {
  cd "$_srcdir"

  python -m build --wheel --no-isolation
  PYTHONDONTWRITEBYTECODE=1 make man -C docs
}

package() {
  cd "$_srcdir"

  python -m installer --destdir="$pkgdir" dist/*.whl
  install -vDm 644 docs/_build/man/archinstall.1 -t "$pkgdir/usr/share/man/man1/"
}
