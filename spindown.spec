Summary:    Daemon that can spin idle disks down
Name:       spindown
Version:    0.4.0
Release:    5
License:    GPLv3+
Group:      System/Servers
Url:        http://code.google.com/p/spindown
Source0:    http://spindown.googlecode.com/files/spindown-%{version}.tar.gz
Source1:    spindown.service
Source2:    01spindown

Patch0: spindown-0.4.0-Makefile.patch
Patch1: spindown-0.4.0-iniparser.patch
Patch2: spindown-0.4.0-iniparser-3.0-1.patch
Patch3: spindown-0.4.0-bz1037334.patch

Requires(preun): systemd-units

BuildRequires: iniparser-devel
BuildRequires: systemd-units

%description
Spindown is a daemon that can spin idle disks down and thus save energy and
improve disk lifetime. It periodically checks for read or written blocks. When
no blocks are read or written the disk is idle. When a disk stays idle long
enough, spindown uses custom command like sg_start or hdparm to spin it down.
It also works with USB disks and hot-swappable disks because it doesn't watch
the device name (hda, sdb, ...), but the device ID. This means that it doesn't
matter if the disk is swapped while the daemon is running.

%prep
%setup -q
rm -rf src/ininiparser3.0b
cp -pf %{SOURCE1} spindown.service
cp -pf %{SOURCE2} 01spindown
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%make OPT="%{optflags}"

%install
make DESTDIR="%{buildroot}" install
mkdir -p %{buildroot}/%{_libdir}/pm-utils/sleep.d
mkdir -p %{buildroot}/%{_unitdir}
install -p -m 755 01spindown %{buildroot}/%{_libdir}/pm-utils/sleep.d/01spindown
install -p -m 755 spindown.service %{buildroot}/%{_unitdir}/spindown.service

%post
%systemd_post spindown.service

%preun
%systemd_preun spindown.service

%files
%defattr(-,root,root,-)
%doc COPYING CHANGELOG README
%{_unitdir}/spindown.service
%{_sbindir}/spindownd
%{_libdir}/pm-utils/sleep.d/01spindown
%config(noreplace) %{_sysconfdir}/spindown.conf

