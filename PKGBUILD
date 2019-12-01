# Maintainer: Your Name <youremail@domain.com>

pkgname=dbsync
pkgver=0
pkgrel=1
epoch=
pkgdesc="sync data in databases"
arch=(any)
url="http://github.com/gcd0318/dbsync"
license=('GPL')
groups=()
depends=('python-mysql-connector')
makedepends=()
checkdepends=()
optdepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=()
#install=$pkgname.install
#changelog=$pkgname.changelog
source=('pkg.tar.xz')
md5sums=('SKIP')

noextract=()
validpgpkeys=()

srcdir='build'
pkgdir="build/$pkgname-$pkgver"

prepare() {
    cd "$srcdir"
#	patch -p1 -i "$srcdir/$pkgname-$pkgver.patch"
}

build() {
	cd "$srcdir"
}

check() {
	cd "$srcdir"
#	make -k check
}

package() {
	cd "$pkgdir"
#	make DESTDIR="$pkgdir/" install
#	install -m=775 dbconf.conf "${pkgdir}/etc"
}
