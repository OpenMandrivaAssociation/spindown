Summary:	Daemon for spindown idle disks
Name:		spindown
Version:	0.2.2
Release:	%mkrel 1
License:	GPLv3
Group:		System/Kernel and hardware
URL:		http://code.google.com/p/spindown/
Source0:	http://spindown.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1:	%{name}-initscript
Requires(pre):	rpm-helper
Requires:	sg3_utils
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Spindown is a daeemon I've written to spindown idle disks and so
saving energy and giving the disks a longer lifetime. It works by
checking how many blocks are read and written from the disks. When
no blocks are read or written the disk is idle. When a disk stays
idle long enough spindown uses sg_start to spin the disk down.
It also works with usb disks and hotswappable disks because it
doesn't watch the device name (hda, sdb, ...), but the device id.
This means that it doesn't matter if the disk is swapped while the
daemon is running.


%prep
%setup -q

%build
export CFLAGS="%{optflags} -pthread"

%make

%install
rm -fr %{buildroot}
%makeinstall_std

install -dm 755 %{buildroot}%{_sysconfdir}
install -dm 755 %{buildroot}%{_initrddir}
install -m 644 spindown.conf.example %{buildroot}%{_sysconfdir}/spindown.conf
install -m 744 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

# (tpg) really not needed
rm -fr %{buildroot}%{_sysconfdir}/rc?.d/*%{name}
rm -fr %{buildroot}%{_sysconfdir}/init.d/%{name}

%clean
rm -fr %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root)
%doc CHANGELOG README spindown.conf.example
%config(noreplace) %{_sysconfdir}/spindown.conf
%{_initrddir}/%{name}
/sbin/spindownd
