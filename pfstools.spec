%define name     pfstools
%define version  1.5
%define release %mkrel 1

%define lib_name_orig libpfs
%define lib_major 1.2
%define lib_name %mklibname pfs %{lib_major}

%define octave_version %(octave --version | head -n 1 | awk '{print $4}')

Summary: High Dynamic Range Images and Video manipulation tools
Name:           %{name}
Version:        %{version}
Release:        %{release}
License: GPL/LGPL
Group: Graphics
Source: http://prdownloads.sourceforge.net/pfstools/%{name}-%{version}.tar.bz2
URL: http://www.mpi-inf.mpg.de/resources/pfstools/
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: blas-devel
BuildRequires: lapack-devel
BuildRequires: octave
BuildRequires: OpenEXR-devel
BuildRequires: netpbm-devel
BuildRequires: libtiff-devel
BuildRequires: qt3-devel
BuildRequires: hdf5-devel
BuildRequires: fftw3-devel
Requires: octave = %octave_version

%description
pfstools package is a set of command line (and one GUI) programs for reading,
writing, manipulating and viewing high-dynamic range (HDR) images and video
frames. All programs in the package exchange data using a simple generic file
format (pfs) for HDR data. The concept of the pfstools is similar to netpbm
package for low-dynamic range images.

%package -n     %{lib_name}
Summary: 	Library for %name
Group: 		System/Libraries
%description -n %{lib_name}
This package contain the library needed to run programs linked 
with %lib_name.

%package -n     %{lib_name}-devel
Summary:	Headers for developing programs that will use %{lib_name}
Group:		Development/C++
Requires:       %{lib_name} = %{version}
Provides:       %{lib_name_orig}-devel = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
This package contains the headers that programmers will need to develop 
application which will use %lib_name_orig

%prep
%setup -q

%build
export PATH="$QTDIR/bin:$PATH"
export CXX="g++ %optflags -fPIC"
export LDFLAGS="-L$QTDIR/%{_lib}"
# force dynamic qt linking
perl -pi -e 's|QT_IS_STATIC=\`ls \$QTDIR/lib/\*\.a 2> /dev/null\`||' configure
# fix QTDIR && QTLIBDIR 
perl -pi -e "s,DIR/lib,DIR/%_lib," configure
%configure
%make

%install
%makeinstall_std

chmod 644 %{buildroot}/%_datadir/octave/%octave_version/site/m/pfstools/*.m
chmod 644 %{buildroot}/%{_libdir}/*.la

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README TODO
%{_bindir}/*
%{_libdir}/octave/%octave_version/site/oct/%_target_platform/pfstools
%_datadir/octave/%octave_version/site/m/pfstools
%{_mandir}/man?/*

%files -n %{lib_name}
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%{_includedir}/pfs-%lib_major
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la
