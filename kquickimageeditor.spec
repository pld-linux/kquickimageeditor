#
# Conditional build:
%bcond_with	tests		# build with tests
#
# TODO:
# - runtime Requires if any

%define		qtver		5.15.2
%define		kfname		kquickimageditor
Summary:	kquick image editor
Name:		kquickimageeditor
Version:	0.6.0
Release:	1
License:	BSD 2 Clause/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/kquickimageeditor/%{name}-%{version}.tar.xz
# Source0-md5:	55b77ed06675e2c57f4a2317a998ce75
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= 5.15.10
BuildRequires:	Qt6Gui-devel >= 5.15.10
BuildRequires:	Qt6Network-devel >= 5.15.10
BuildRequires:	Qt6Qml-devel >= 5.15.10
BuildRequires:	Qt6Quick-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KQuickImageEditor is a set of QtQuick components providing basic image
editing capabilities.

%package devel
Summary:	Header files for %{name} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{name}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{name}.

%prep
%setup -q

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{_libdir}/libKQuickImageEditor.so.*.*
%ghost %{_libdir}/libKQuickImageEditor.so.1
%{_libdir}/qt6/qml/org/kde/kquickimageeditor

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKQuickImageEditor.so
%{_libdir}/cmake/KQuickImageEditor
%{_libdir}/qt6/mkspecs/modules/qt_KQuickImageEditor.pri
%{_includedir}/KQuickImageEditor
%{_includedir}/kquickimageeditor
