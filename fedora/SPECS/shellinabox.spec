%global commit 88822c1f4c030d5f05ced097eb7b6668ff3d7c6f
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global username shellinabox

%if 0%{?rhel} == 5
%define _sharedstatedir /var/lib
%endif

Name:           shellinabox
Version:        2.14
Release:        28.git%{shortcommit}%{?dist}
Summary:        Web based AJAX terminal emulator
Group:          System Environment/Daemons
License:        GPLv2
URL:            https://github.com/pythonanywhere/shellinabox_fork
Source0:        https://github.com/pythonanywhere/shellinabox_fork/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source1:        shellinaboxd.sysconfig
Source2:        shellinaboxd.service
Source3:        shellinaboxd.init
Patch0:         %{name}-ssh-options.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
Requires:       openssl
Requires(pre):  shadow-utils

%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%endif

%if 0%{?rhel} == 5 || 0%{?rhel} == 6
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service
Requires(postun):   /sbin/service
%endif

%description
Shell In A Box implements a web server that can export arbitrary command line
tools to a web based terminal emulator. This emulator is accessible to any
JavaScript and CSS enabled web browser and does not require any additional
browser plugins.

%prep
%setup -qn %{name}_fork-%{commit}
%patch0 -p1

%build
%configure --disable-runtime-loading
make %{?_smp_mflags}
chmod 644 %{name}/*

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
install -p -m 755 -D shellinaboxd %{buildroot}%{_sbindir}/shellinaboxd
install -p -m 644 -D shellinaboxd.1 %{buildroot}%{_mandir}/man1/shellinaboxd.1
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/shellinaboxd

mkdir -p %{buildroot}%{_datadir}/%{name}
install -p -m 644 shellinabox/white-on-black.css %{buildroot}%{_datadir}/%{name}
install -p -m 644 shellinabox/color.css %{buildroot}%{_datadir}/%{name}
install -p -m 644 shellinabox/monochrome.css %{buildroot}%{_datadir}/%{name}

%if 0%{?fedora} || 0%{?rhel} >= 7

# Systemd unit files
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_unitdir}/shellinaboxd.service

%else

# Initscripts
install -p -m 755 -D %{SOURCE3} %{buildroot}%{_initrddir}/shellinaboxd

%endif

%clean
rm -rf %{buildroot}


%pre
getent group %username >/dev/null || groupadd -r %username &>/dev/null || :
getent passwd %username >/dev/null || useradd -r -s /sbin/nologin \
    -d %{_sharedstatedir}/shellinabox -M -c 'Shellinabox' -g %username %username &>/dev/null || :
exit 0

%if 0%{?fedora} || 0%{?rhel} >= 7

%post
%systemd_post shellinaboxd.service

%preun
%systemd_preun shellinaboxd.service

%postun
%systemd_postun_with_restart shellinaboxd.service

%endif

%if 0%{?rhel} == 6 || 0%{?rhel} == 5

%post
/sbin/chkconfig --add shellinaboxd

%preun
if [ "$1" = 0 ]; then
        /sbin/service shellinaboxd stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del shellinaboxd
fi

%postun
if [ "$1" -ge "1" ]; then
        /sbin/service shellinaboxd condrestart >/dev/null 2>&1 || :
fi

%endif

%files
%doc AUTHORS NEWS README README.Fedora GPL-2 COPYING
%doc shellinabox/styles.css shellinabox/print-styles.css
%doc shellinabox/shell_in_a_box.js
%config(noreplace) %{_sysconfdir}/sysconfig/shellinaboxd
%{_mandir}/man1/shellinaboxd.1.*
%{_datadir}/%{name}
%{_sbindir}/shellinaboxd
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/shellinaboxd.service
%else
%{_initrddir}/shellinaboxd
%endif
%attr(750,%{username},%{username}) %{_sharedstatedir}/%{name}

%changelog
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-28.git88822c1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 11 2014 Simone Caronni <negativo17@gmail.com> - 2.14-27.git88822c1
- Add additional ssh option ProxyCommand=none (#1013974).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-26.git88822c1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 06 2013 Simone Caronni <negativo17@gmail.com> - 2.14-25.git88822c1
- Add systemd to BuildRequires; not default on Fedora 20+.
- Remove Fedora 17 conditionals, distribution EOL.
- Remove systemd-sysv dependency as per new packaging guidelines.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-25.git88822c1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Simone Caronni <negativo17@gmail.com> - 2.14-24.git88822c1
- Fix SSL support (#973058).
- SPEC file cleanup.

* Sat May 11 2013 Simone Caronni <negativo17@gmail.com> - 2.14-22.git88822c1
- Kill daemon by pid on EPEL (#962069).
- Change restart policy in service files and fix service dependencies.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-21.git88822c1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Simone Caronni <negativo17@gmail.com> - 2.14-20.git88822c1
- Added define for RHEL 5 (rhbz#894903).
- Updated spec to new packaging guidelines for github sources.

* Wed Jan 09 2013 Simone Caronni <negativo17@gmail.com> - 2.14-19.git88822c1f
- Fix SysV init scripts.

* Wed Jan 09 2013 Simone Caronni <negativo17@gmail.com> - 2.14-18.git88822c1f
- Updated init script according to Fedora template (#893129)
  https://fedoraproject.org/wiki/Packaging:SysVInitScript?rd=Packaging/SysVInitScript

* Fri Dec 14 2012 Simone Caronni <negativo17@gmail.com> - 2.14-17.git88822c1f
- Fix the commit / dist tags order in the revision.

* Fri Dec 14 2012 Simone Caronni <negativo17@gmail.com> - 2.14-16.git88822c1f
- Move source from the original unmantained content to the github fork.

* Wed Oct 17 2012 Simone Caronni <negativo17@gmail.com> - 2.14-15
- Fix fedpkg checks. Requires fedpkg > 1.10:
  http://git.fedorahosted.org/cgit/fedpkg.git/commit/?id=11c46c06a3c9cc2f58d68aea964dd37dc028e349
- Change systemd requirements as per new package guidelines.

* Mon Oct 01 2012 Simone Caronni <negativo17@gmail.com> - 2.14-14
- Move user directory and data under /var/lib.

* Wed Sep 26 2012 Joel Young <jdy@cryregarder.com> - 2.14-13
- Fix variable expansions in init script and service file.

* Tue Sep 25 2012 Simone Caronni <negativo17@gmail.com> - 2.14-12
- Really add WorkingDirectory to service files.
- Remove postun user deletion leftovers.
- Add static files to be customized (as referenced by the man page) in the doc directory.

* Mon Sep 24 2012 Simone Caronni <negativo17@gmail.com> - 2.14-11
- Fix RHEL 5 rpm macro.

* Thu Sep 13 2012 Simone Caronni <negativo17@gmail.com> - 2.14-10
- Fixes from (Joel Young <jdy@cryregarder.com>):
    Install supplied css files.
    Set menu item to turn off ssl as disabled by default.
    Do not remove user on uninstall.
- Simplified spec file.
- Split options in the daemon config file.

* Wed Sep 12 2012 Simone Caronni <negativo17@gmail.com> - 2.14-9
- Added user/group and confined directory for certificates, based on work from Joel Young.

* Tue Sep 11 2012 Joel Young <jdy@cryregarder.com> - 2.14-8
- Fixed bug with firefox 15+ ignored key:
  http://code.google.com/p/shellinabox/issues/detail?id=202&q=key%20work

* Wed Sep 05 2012 Simone Caronni <negativo17@gmail.com> - 2.14-7
- Add Fedora 18 systemd macros.
- Remove isa'ed BuildRequires.

* Thu Aug 30 2012 Simone Caronni <negativo17@gmail.com> - 2.14-6
- Add nss-lookup.target requirement and Documentation tag in service file.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 29 2012 Simone Caronni <negativo17@gmail.com> - 2.14-4
- Move systemd-units BR to proper place.

* Tue May 29 2012 Simone Caronni <negativo17@gmail.com> - 2.14-3
- Spec file changes (changelog, formatting).
- Added license files to doc section.

* Wed May 09 2012 Simone Caronni <negativo17@gmail.com> - 2.14-2
- Tags for RHEL building.

* Wed May 09 2012 Simone Caronni <negativo17@gmail.com> - 2.14-1
- First build.
