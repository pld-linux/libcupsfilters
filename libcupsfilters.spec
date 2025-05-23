#
# Conditional build:
%bcond_with	static_libs	# static libraries
#
Summary:	Library for developing printing filters
Name:		libcupsfilters
Version:	2.1.1
Release:	1
License:	Apache v2.0 with GPL v2 LGPL v2 Exception
Group:		Libraries
Source0:	https://github.com/OpenPrinting/libcupsfilters/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	1e3144c242e7ddcee112d41c79266885
URL:		https://github.com/OpenPrinting/libcupsfilters
BuildRequires:	cups-devel
BuildRequires:	dbus-devel
BuildRequires:	fontconfig-devel >= 2.0.0
BuildRequires:	lcms2-devel
BuildRequires:	libexif-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	libtiff-devel
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	poppler-cpp-devel >= 0.19
BuildRequires:	qpdf-devel >= 11.0.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Suggests:	cups-clients
Requires:	fontconfig-libs >= 2.0.0
Suggests:	ghostscript
Suggests:	mupdf
Requires:	qpdf-libs >= 11.0.0
Obsoletes:	cups-filters-libs < 2.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libcupsfilters provides a library, which implements common functions
used in cups-browsed daemon and printing filters, and additional files
as banner templates and character sets. The filters are used in CUPS
daemon and in printer applications.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	cups-filters-devel < 2.0.1

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	cups-filters-static < 2.0.1

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--enable-dbus \
	--with-gs-path=/usr/bin/gs \
	--with-ippfind-path=/usr/bin/ippfind \
	--with-mutool-path=/usr/bin/mutool

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Remove .la pollution
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/libcupsfilters

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES.md LICENSE NEWS NOTICE README.md
%attr(755,root,root) %{_libdir}/libcupsfilters.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcupsfilters.so.2
%dir %{_datadir}/cups/banners
%{_datadir}/cups/banners/*
%dir %{_datadir}/cups/charsets
%{_datadir}/cups/charsets/pdf.utf-8*
%dir %{_datadir}/cups/data
%{_datadir}/cups/data/*.odt
%{_datadir}/cups/data/*.pdf
%{_datadir}/cups/data/testprint

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%{_includedir}/cupsfilters
%{_pkgconfigdir}/libcupsfilters.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/%{name}.a
%endif
