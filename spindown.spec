Summary:	Daemon for spindown idle disks
Name:		spindown
Version:	0.4.0
Release:	%mkrel 2
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


%changelog
* Sat Apr 16 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.4.0-2mdv2011.0
+ Revision: 653314
- rebuild

* Tue Jun 09 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.4.0-1mdv2010.0
+ Revision: 384503
- update to new version 0.4.0

* Tue Feb 24 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.3.0-1mdv2009.1
+ Revision: 344335
- update to new version 0.3.0

* Tue Sep 09 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.2.2-1mdv2009.0
+ Revision: 283048
- update to new version 0.2.2

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 0.2.1-2mdv2009.0
+ Revision: 269345
- rebuild early 2009.0 package (before pixel changes)

* Tue Jun 03 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.2.1-1mdv2009.0
+ Revision: 214571
- update to new version 0.2.1

* Mon May 19 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.2-1mdv2009.0
+ Revision: 209101
- new version
- fix init script

* Tue Apr 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.1.3-2mdv2009.0
+ Revision: 198905
- fix init script

* Mon Apr 28 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.1.3-1mdv2009.0
+ Revision: 198036
- add requires on sg3_utils
- tune up CFLAGS
- add initscript
- correct the summary
- add source and spec files
- Created package structure for spindown.

