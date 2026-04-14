Name:       outerd
Version:    1.4.6
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://outerd.com
Vendor:     outerd <info@outerd.com>
Requires:   gtk3 libxcb libXfixes alsa-lib libva pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/outerd" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/outerd"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/outerd.service -t "%{buildroot}/usr/share/outerd/files"
install -Dm 644 $HBB/res/outerd.desktop -t "%{buildroot}/usr/share/outerd/files"
install -Dm 644 $HBB/res/outerd-link.desktop -t "%{buildroot}/usr/share/outerd/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/outerd.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/outerd.svg"

%files
/usr/share/outerd/*
/usr/share/outerd/files/outerd.service
/usr/share/icons/hicolor/256x256/apps/outerd.png
/usr/share/icons/hicolor/scalable/apps/outerd.svg
/usr/share/outerd/files/outerd.desktop
/usr/share/outerd/files/outerd-link.desktop

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
ln -sf /usr/share/outerd/outerd /usr/bin/outerd
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
    rm /usr/bin/outerd || true
    rmdir /usr/lib/outerd || true
    rmdir /usr/local/outerd || true
    rmdir /usr/share/outerd || true
    rm /usr/share/applications/outerd.desktop || true
    rm /usr/share/applications/outerd-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/outerd || true
    rmdir /usr/local/outerd || true
  ;;
esac
