%define name     pfstools
%define version  1.7.0
%define release %mkrel 3

%define libname_orig	libpfs
%define major		1.2
%define libname		%mklibname pfs %{major}
%define develname	%mklibname pfs -d
%define octave_version %(rpm -q octave --queryformat %{VERSION})

Summary: High Dynamic Range Images and Video manipulation tools
Name:           %{name}
Version:        %{version}
Release:        %{release}
License: GPLv2+ and LGPLv2+
Group: Graphics
URL: https://www.mpi-inf.mpg.de/resources/pfstools/
Source: http://prdownloads.sourceforge.net/pfstools/%{name}-%{version}.tar.gz
Patch0: pfstools-1.6.5-fix-format-errors.patch
BuildRequires: blas-devel
BuildRequires: lapack-devel
BuildRequires: octave-devel
BuildRequires: OpenEXR-devel
BuildRequires: netpbm-devel
BuildRequires: libtiff-devel
BuildRequires: qt3-devel
BuildRequires: hdf5-devel
BuildRequires: fftw3-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
Requires:	octave = %octave_version
BuildRoot: %{_tmppath}/%{name}-%{version}

%description
pfstools package is a set of command line (and one GUI) programs for reading,
writing, manipulating and viewing high-dynamic range (HDR) images and video
frames. All programs in the package exchange data using a simple generic file
format (pfs) for HDR data. The concept of the pfstools is similar to netpbm
package for low-dynamic range images.

%package -n     %{libname}
Summary: 	Library for %name
Group: 		System/Libraries
%description -n %{libname}
This package contain the library needed to run programs linked 
with %libname.

%package -n     %{develname}
Summary:	Headers for developing programs that will use %{libname}
Group:		Development/C++
Requires:       %{libname} = %{version}
Provides:       %{libname_orig}-devel = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname pfs 1.2 -d}

%description -n %{develname}
This package contains the headers that programmers will need to develop 
application which will use %libname_orig

%prep
%setup -q
%patch0 -p 1

%build
export QTDIR="%{_prefix}/lib/qt3"
export PATH="$QTDIR/bin:$PATH"
export CXX="g++ %optflags -fPIC"
export LDFLAGS="-L$QTDIR/%{_lib}"
# force dynamic qt linking
perl -pi -e 's|QT_IS_STATIC=\`ls \$QTDIR/lib/\*\.a 2> /dev/null\`||' configure
# fix QTDIR && QTLIBDIR 
perl -pi -e "s,DIR/lib,DIR/%_lib," configure
%configure2_5x
make

%install
rm -rf %{buildroot}
%makeinstall_std

#chmod 644 %{buildroot}/%_datadir/octave/%octave_version/site/m/pfstools/*.m
chmod 644 %{buildroot}/%{_libdir}/*.la

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog INSTALL NEWS README TODO
%{_bindir}/*
%{_libdir}/octave/*/site/oct/%_target_platform/%name
%{_datadir}/octave/*/site/m/%name
%{_mandir}/man?/*

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{develname}
%{_includedir}/pfs-%major
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la
