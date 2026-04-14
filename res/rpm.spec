Name:       outerd
Version:    1.4.6
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://outerd.com
Vendor:     outerd <info@outerd.com>
Requires:   gtk3 libxcb libXfixes alsa-lib libva2 pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/outerd/
mkdir -p %{buildroot}/usr/share/outerd/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/outerd %{buildroot}/usr/bin/outerd
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/outerd/libsciter-gtk.so
install $HBB/res/outerd.service %{buildroot}/usr/share/outerd/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/outerd.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/outerd.svg
install $HBB/res/outerd.desktop %{buildroot}/usr/share/outerd/files/
install $HBB/res/outerd-link.desktop %{buildroot}/usr/share/outerd/files/

%files
/usr/bin/outerd
/usr/share/outerd/libsciter-gtk.so
/usr/share/outerd/files/outerd.service
/usr/share/icons/hicolor/256x256/apps/outerd.png
/usr/share/icons/hicolor/scalable/apps/outerd.svg
/usr/share/outerd/files/outerd.desktop
/usr/share/outerd/files/outerd-link.desktop
/usr/share/outerd/files/__pycache__/*

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop outerd || true
  ;;
esac

%post
cp /usr/share/outerd/files/outerd.service /etc/systemd/system/outerd.service
cp /usr/share/outerd/files/outerd.desktop /usr/share/applications/
cp /usr/share/outerd/files/outerd-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable outerd
systemctl start outerd
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop outerd || true
    systemctl disable outerd || true
    rm /etc/systemd/system/outerd.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/outerd.desktop || true
    rm /usr/share/applications/outerd-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
