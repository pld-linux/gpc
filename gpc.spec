%define GPC_VERSION	20030830
%define GCC_VERSION	3.2.1

Summary:	GNU Pascal Compiler
Summary(pl):	Kompilator Pascala GNU
Name:		gpc
Version:	%{GPC_VERSION}
Release:	4
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{GCC_VERSION}/gcc-%{GCC_VERSION}.tar.gz
# Source0-md5:	82c26f362a6df7d2ba5b967606bd7d9a
Source1:	http://www.gnu-pascal.de/alpha/%{name}-%{version}.tar.gz
# Source1-md5:	e418c30e9cbf71f82f7a9cd246c13ac5
URL:		http://www.gnu-pascal.de/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Pascal compiler based on the gcc %{GCC_VERSION} compiler.

GNU Pascal is part of the GNU compiler family, GNU CC or GCC. It
combines a Pascal front-end with the proven GNU C back-end for code
generation and optimization. Unlike utilities such as p2c, this is a
true compiler, not just a converter.

%description -l pl
Kompilator Pascala oparty o wersj� %{GCC_VERSION} kompilatora gcc.

GNU Pascal stanowi cz�� rodziny kompilator�w GNU, GNU CC lub GCC.
��czy on w sobie nak�adk� pascalow� ze sprawdzonym w GNU C wewn�trznym
mechanizmem generacji kodu i optymalizacji. W odr�nieniu od narz�dzi
takich jak p2c, jest to prawdziwy kompilator, a nie tylko konwerter.

%prep
%setup -q -n gcc-%{GCC_VERSION} -a 1
mv gpc-*/p gcc/.
cd gcc
patch -s -p1 < p/diffs/gcc-%{GCC_VERSION}.diff

%build
cp -f /usr/share/automake/config.sub .
cp -f /usr/share/automake/config.sub boehm-gc
cd gcc
#%{__autoconf}
cd ..
rm -rf obj-%{_target_platform}
install -d obj-%{_target_platform} && cd obj-%{_target_platform}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false ../configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--infodir=%{_infodir} \
	--enable-shared \
%ifarch amd64
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

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
#%doc gcc/p/README p/COPYING gcc/p/COPYING.LIB gcc/p/ChangeLog
#%doc gcc/p/FAQ p/INSTALL gcc/p/doc/TODO
#%doc gcc/p/doc/manual.texi.tar.gz
#%doc gcc/p/demos gcc/p/test
%attr(755, root, root) %{_bindir}/gpc*
%dir %{_libdir}/gcc-lib/%{_target_cpu}*/*
%attr(755,root,root) %{_libdir}/gcc-lib/%{_target_cpu}*/*/gpc*
%attr(755,root,root) %{_libdir}/gcc-lib/%{_target_cpu}*/*/crt*.o
%attr(755,root,root) %{_libdir}/gcc-lib/%{_target_cpu}*/*/collect2
%{_libdir}/gcc-lib/%{_target_cpu}*/*/units
%{_libdir}/gcc-lib/%{_target_cpu}*/*/include
%{_libdir}/gcc-lib/%{_target_cpu}*/*/libg?c.a
#%{_libdir}/gcc-lib/%{_target_cpu}*/*/SYSCALLS.c.X
%{_infodir}/gpc*
%{_mandir}/man?/gpc*
#%attr(0755, root, root) %{_libdir}/gcc-lib/%{_target_cpu}-redhat-linux/egcs-*/gpc-cpp
#%attr(0755, root, root) %{_libdir}/gcc-lib/%{_target_cpu}-redhat-linux/egcs-*/gpc1
#%{_libdir}/gcc-lib/%{_target_cpu}-redhat-linux/egcs-*/libgpc.a
#%{_libdir}/gcc-lib/%{_target_cpu}-redhat-linux/egcs-*/units
