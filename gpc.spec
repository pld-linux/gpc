# TODO: update to 20060325 and switch to 4.0.3 after Ac (not ready for gcc 4.1 yet)
%define GPC_VERSION	20050331
%define GCC_VERSION	3.3.6

Summary:	GNU Pascal Compiler
Summary(pl.UTF-8):	Kompilator Pascala GNU
Name:		gpc
Version:	%{GPC_VERSION}
Release:	2
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{GCC_VERSION}/gcc-%{GCC_VERSION}.tar.bz2
# Source0-md5:	6936616a967da5a0b46f1e7424a06414
Source1:	http://www.gnu-pascal.de/alpha/%{name}-%{version}.tar.bz2
# Source1-md5:	cdc1460ba7b3cc099d404c5fa1202f8a
Patch0:		gcc-cmpi.patch
Patch1:		%{name}-info.patch
Patch2:		%{name}-range.patch
URL:		http://www.gnu-pascal.de/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	help2man
BuildRequires:	rpmbuild(macros) >= 1.213
#Requires:	gcc-dirs
Requires:	gcc = 5:%{GCC_VERSION}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Pascal compiler based on the gcc %{GCC_VERSION} compiler.

GNU Pascal is part of the GNU compiler family, GNU CC or GCC. It
combines a Pascal front-end with the proven GNU C back-end for code
generation and optimization. Unlike utilities such as p2c, this is a
true compiler, not just a converter.

%description -l pl.UTF-8
Kompilator Pascala oparty o wersję %{GCC_VERSION} kompilatora gcc.

GNU Pascal stanowi część rodziny kompilatorów GNU, GNU CC lub GCC.
Łączy on w sobie nakładkę pascalową ze sprawdzonym w GNU C wewnętrznym
mechanizmem generacji kodu i optymalizacji. W odróżnieniu od narzędzi
takich jak p2c, jest to prawdziwy kompilator, a nie tylko konwerter.

%prep
%setup -q -n gcc-%{GCC_VERSION} -a 1
%patch -P0 -p1
#patch -s -p0 < p/diffs/gcc-%{GCC_VERSION}.diff
patch -s -p0 < p/diffs/gcc-3.3.5.diff
mv p gcc
%patch -P1 -p1
%patch -P2 -p1

%build
cp -f /usr/share/automake/config.sub .
cp -f /usr/share/automake/config.sub boehm-gc
#cd gcc
#%{__autoconf}
#cd ..
rm -rf obj-%{_target_platform}
install -d obj-%{_target_platform}
cd obj-%{_target_platform}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--infodir=%{_infodir} \
	--enable-shared \
%ifarch %{x8664}
	--disable-multilib \
%endif
%ifnarch sparc sparc64
	--enable-threads=posix \
	--enable-haifa \
%endif
	--with-gnu-as \
	--with-gnu-ld \
	--disable-nls \
	--build=%{_target_platform} \
	--host=%{_target_platform} \
	--enable-languages=pascal

PATH=$PATH:/sbin:%{_sbindir}
touch ../gcc/c-gperf.h

cd ..
%{__make} -C obj-%{_target_platform} bootstrap \
	LDFLAGS_FOR_TARGET="%{rpmldflags}" \
	mandir=%{_mandir} \
	infodir=%{_infodir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/lib,%{_datadir}}

cd obj-%{_target_platform}
PATH=$PATH:/sbin:%{_sbindir}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	libexecdir=$RPM_BUILD_ROOT%{_libexecdir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc gcc/p/{AUTHORS,ChangeLog,FAQ,NEWS,README}
#%doc gcc/p/demos
%attr(755,root,root) %{_bindir}/binobj
%attr(755,root,root) %{_bindir}/gpc
%attr(755,root,root) %{_bindir}/gpc-run
%attr(755,root,root) %{_bindir}/gpidump
# common gcc stuff, not needed here if we use the same gcc version
#%dir %{_libdir}/gcc-lib/%{_target_cpu}*/*
#%attr(755,root,root) %{_libdir}/gcc-lib/%{_target_cpu}*/*/crt*.o
#%attr(755,root,root) %{_libdir}/gcc-lib/%{_target_cpu}*/*/collect2
#%dir %{_libdir}/gcc-lib/%{_target_cpu}*/*/include
#%{_libdir}/gcc-lib/%{_target_cpu}*/*/include/...
#%{_libdir}/gcc-lib/%{_target_cpu}*/*/libgcc.a
%attr(755,root,root) %{_libdir}/gcc-lib/%{_target_cpu}*/*/gpc*
%{_libdir}/gcc-lib/%{_target_cpu}*/*/include/gpc-in-c.h
%{_libdir}/gcc-lib/%{_target_cpu}*/*/units
%{_libdir}/gcc-lib/%{_target_cpu}*/*/libgpc.a
%{_infodir}/gpc.info*
%{_infodir}/gpcs.info*
%lang(de) %{_infodir}/gpcs-de.info*
%lang(es) %{_infodir}/gpcs-es.info*
%lang(hr) %{_infodir}/gpcs-hr.info*
%{_mandir}/man1/binobj.1*
%{_mandir}/man1/gpc.1*
%{_mandir}/man1/gpc-run.1*
%{_mandir}/man1/gpidump.1*
