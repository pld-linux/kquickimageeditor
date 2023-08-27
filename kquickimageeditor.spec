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
Version:	0.2.0
Release:	1
License:	BSD 2 Clause/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/kquickimageeditor/%{name}-%{version}.tar.xz
# Source0-md5:	f563a679f2d4ac590108dffe3073cbc5
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= 5.15.10
BuildRequires:	Qt5Gui-devel >= 5.15.10
BuildRequires:	Qt5Network-devel >= 5.15.10
BuildRequires:	Qt5Qml-devel >= 5.15.10
BuildRequires:	Qt5Quick-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
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
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/qt5/qml/org/kde/kquickimageeditor
%{_libdir}/qt5/qml/org/kde/kquickimageeditor/BasicResizeHandle.qml
%{_libdir}/qt5/qml/org/kde/kquickimageeditor/CropBackground.qml
%{_libdir}/qt5/qml/org/kde/kquickimageeditor/RectangleCutout.qml
%{_libdir}/qt5/qml/org/kde/kquickimageeditor/SelectionBackground.qml
%{_libdir}/qt5/qml/org/kde/kquickimageeditor/SelectionHandle.qml
%{_libdir}/qt5/qml/org/kde/kquickimageeditor/SelectionTool.qml
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/kquickimageeditor/libkquickimageeditorplugin.so
%{_libdir}/qt5/qml/org/kde/kquickimageeditor/plugins.qmltypes
%{_libdir}/qt5/qml/org/kde/kquickimageeditor/qmldir
%{_libdir}/qt5/qml/org/kde/kquickimageeditor/qmldir.license

%files devel
%defattr(644,root,root,755)
%{_libdir}/cmake/KQuickImageEditor
%{_libdir}/qt5/mkspecs/modules/qt_KQuickImageEditor.pri
