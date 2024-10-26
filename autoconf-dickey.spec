#
# Conditional build:
%bcond_with	tests	# do not perform "make check"

%define	snap	20240618
%define	rel	1

Summary:	Thomas Dickey's autoconf - source configuration tools
Summary(pl.UTF-8):	autoconf (wersja Thomasa Dickeya) - narzędzie do automatycznego konfigurowania źródeł
Name:		autoconf-dickey
Version:	2.52
Release:	0.%{snap}.%{rel}
License:	GPL v2+/v3+
Group:		Development/Building
# stable releases:
Source0:	http://ftp.debian.org:/debian/pool/main/a/autoconf-dickey/%{name}_%{version}+%{snap}.orig.tar.gz
# Source0-md5:	522ccfc6cb7cccca1f3b13745cca9c21
Patch0:		%{name}-info.patch
URL:		https://invisible-island.net/autoconf/
BuildRequires:	m4 >= 3:1.4.13
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.745
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo >= 4.2
BuildRequires:	xz
BuildConflicts:	m4 = 1.4o
Requires:	/bin/awk
Requires:	diffutils
Conflicts:	gettext < 0.10.38-3
Conflicts:	pkgconfig < 1:0.25-2
%requires_eq	m4
Requires:	mktemp
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if "%{_host_cpu}" == "x32"
%define	build_arch %{_target_platform}
%else
%define	build_arch %{_host}
%endif

%define		_libdir		%{_datadir}

%description
Autoconf (Thomas Dickey's version) is a tool for configuring source
code and Makefiles. Using Autoconf, programmers can create portable
and configurable packages, since the person building the package is
allowed to specify various configuration options.

You should install Autoconf if you are developing software and you'd
like to use it to create shell scripts which will configure your
source code packages.

Note that the Autoconf package is not required for the end user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not their
use.

%description -l pl.UTF-8
autoconf (wersja Thomasa Dickeya) jest narzędziem wykorzystywanym do
automatycznego konfigurowania kodów źródłowych pakietów programów oraz
do generowania na podstawie automatycznie rozpoznanego środowiska
plików Makefile i innych zależnych od zawartości systemu, w którym ma
przebiegać proces kompilacji. Pomaga programiście w konfigurowaniu i
tworzeniu oprogramowania dającego się przenieść na różne platformy.
Umożliwia wybór wielu opcji podczas procesu przygotowania do
kompilacji.

autoconf nie jest generalnie potrzebny końcowemu użytkownikowi, a
tylko podczas generowania samych skryptów autokonfiguracyjnych.

%prep
%setup -q -n autoconf-%{version}-%{snap}
%patch0 -p1

%build
%configure \
	--program-suffix=-dickey \
	--datadir=%{_datadir}/autoconf-dickey \
	--host=%{build_arch} \
	--build=%{build_arch}
%{__make} -j1

%{?with_tests:%{__make} -j1 check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# no need for duplicates
%{__rm} $RPM_BUILD_ROOT%{_infodir}/standards*.info

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README THANKS
%attr(755,root,root) %{_bindir}/auto*-dickey
%attr(755,root,root) %{_bindir}/ifnames-dickey
%{_libdir}/autoconf-dickey
%{_infodir}/autoconf-dickey.info*
%{_mandir}/man1/auto*-dickey.1*
%{_mandir}/man1/ifnames-dickey.1*
