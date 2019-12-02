# Maintainer: gcd0318 <gcd0318@hotmail.com>

pkgname=dbsync
pkgver=1
pkgrel=1
epoch=
pkgdesc="sync data in databases"
arch=('any')
url="http://github.com/gcd0318/dbsync"
license=('GPL')
depends=('python-mysql-connector')
source=('pkg.tar.xz')
md5sums=('SKIP')
backup=('dbsync.conf')

srcdir='build/src'
pkgdir="build/$pkgname-$pkgver"

prepare() {
#    cd "$srcdir"
    pwd
    echo "$srcdir"
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
