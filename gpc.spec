%define GPC_VERSION	20030507
%define GCC_VERSION	3.2.1

Summary:	GNU Pascal
Name:		gpc
Version:	%{GPC_VERSION}
Release:	0.1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{GCC_VERSION}/gcc-%{GCC_VERSION}.tar.gz
# Source0-md5:	82c26f362a6df7d2ba5b967606bd7d9a
Source1:	http://www.gnu-pascal.de/alpha/%{name}-%{version}.tar.gz
# Source1-md5:	f63312c3fe961518bf63964705799e57
BuildRequires:	autoconf
URL:		http://www.free-pascal.de/
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Pascal compiler based on the gcc %{GCC_VERSION} compiler.

GNU Pascal is part of the GNU compiler family, GNU CC or GCC. It
combines a Pascal front-end with the proven GNU C back-end for code
generation and optimization. Unlike utilities such as p2c, this is a
true compiler, not just a converter.

%prep
%setup -q -n gcc-%{GCC_VERSION} -a 1
mv gpc-*/p gcc/.
cd gcc
patch -s -p1 < p/diffs/gcc-%{GCC_VERSION}.diff

%build
(cd gcc; autoconf)
rm -rf obj-%{_target_platform}
install -d obj-%{_target_platform} && cd obj-%{_target_platform}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false ../configure \
        --prefix=%{_prefix} \
        --infodir=%{_infodir} \
        --enable-shared \
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
touch  ../gcc/c-gperf.h

cd ..
%{__make} -C obj-%{_target_platform} bootstrap \
        LDFLAGS_FOR_TARGET="%{rpmldflags}" \
        mandir=%{_mandir} \
        infodir=%{_infodir}

%install
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/lib,%{_datadir}}

cd obj-%{_target_platform}
PATH=$PATH:/sbin:%{_sbindir}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%preun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
#%doc gcc/p/README p/COPYING gcc/p/COPYING.LIB gcc/p/ChangeLog
#%doc gcc/p/FAQ p/INSTALL gcc/p/doc/TODO
#%doc gcc/p/doc/manual.texi.tar.gz
#%doc gcc/p/demos gcc/p/test
%attr(0755, root, root) %{_bindir}/gpc*
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
