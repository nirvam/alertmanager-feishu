# Maintainer: Nirvam <nirvam@example.com>
pkgname=alertmanager-feishu
pkgver=0.1.0
pkgrel=1
pkgdesc="Alertmanager to Feishu webhook service"
arch=('any')
url="https://github.com/nirvam/alertmanager-feishu"
license=('MIT')
depends=('python' 'python-fastapi' 'python-uvicorn' 'python-httpx' 'python-pydantic-settings' 'python-typer' 'python-jinja2')
source=("${pkgname}-${pkgver}.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$srcdir/$pkgname-$pkgver"
    install -Dm644 alertmanager-feishu.service "$pkgdir/usr/lib/systemd/system/alertmanager-feishu.service"
    mkdir -p "$pkgdir/opt/alertmanager-feishu"
    cp -r src/ "$pkgdir/opt/alertmanager-feishu/"
}
