%bcond_without check

%global version_suffix 3.4
%global version_enc 3_4_2
Name:           libarchive%{version_suffix}
%global real_name libarchive
Version:        3.4.2
%global sonamever 13
Release:        1%{?dist}
Summary:        A library for handling streaming archive formats

License:        BSD
URL:            https://www.libarchive.org/
Source0:        https://libarchive.org/downloads/%{real_name}-%{version}.tar.gz

BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  bzip2-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  gcc
BuildRequires:  libacl-devel
BuildRequires:  libattr-devel
BuildRequires:  libxml2-devel
BuildRequires:  libzstd-devel
BuildRequires:  lz4-devel
# According to libarchive maintainer, linking against liblzo violates
# LZO license.
# See https://github.com/libarchive/libarchive/releases/tag/v3.3.0
#BuildRequires:  lzo-devel
BuildRequires:  openssl-devel
BuildRequires:  sharutils
BuildRequires:  xz-devel
BuildRequires:  zlib-devel

%description
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants, several cpio
formats, and both BSD and GNU ar variants. It can also write shar archives and
read ISO9660 CDROM images and ZIP archives.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package manpages
Summary:        Man pages for %{name}
BuildArch:      noarch
Conflicts:      %{real_name}

%description manpages
Manual pages for %{name}. Do not install that package if %{real_name}
is already installed. The content is the same, just not for the same
version of %{real_name}.

%package -n bsdtar%{version_suffix}
Summary:        Manipulate tape archives
Requires:       %{name}%{?_isa} = %{version}-%{release}
Conflicts:      bsdtar%{?_isa}

%description -n bsdtar%{version_suffix}
The bsdtar package contains standalone bsdtar utility split off regular
libarchive packages.


%package -n bsdcpio%{version_suffix}
Summary:        Copy files to and from archives
Requires:       %{name}%{?_isa} = %{version}-%{release}
Conflicts:      bsdcpio%{?_isa}

%description -n bsdcpio%{version_suffix}
The bsdcpio package contains standalone bsdcpio utility split off regular
libarchive packages.


%package -n bsdcat%{version_suffix}
Summary:        Expand files to standard output
Requires:       %{name}%{?_isa} = %{version}-%{release}
Conflicts:      bsdcat%{?_isa}

%description -n bsdcat%{version_suffix}
The bsdcat program typically takes a filename as an argument or reads standard
input when used in a pipe.  In both cases decompressed data it written to
standard output.


%prep
%setup -qn %{real_name}-%{version} 


%build
%configure --disable-static LT_SYS_LIBRARY_PATH=%_libdir
%make_build


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# rhbz#1294252
replace ()
{
    filename=$1
    file=`basename "$filename"`
    binary=${file%%.*}
    pattern=${binary##bsd}

    awk "
        # replace the topic
        /^.Dt ${pattern^^} 1/ {
            print \".Dt ${binary^^} 1\";
            next;
        }
        # replace the first occurence of \"$pattern\" by \"$binary\"
        !stop && /^.Nm $pattern/ {
            print \".Nm $binary\" ;
            stop = 1 ;
            next;
        }
        # print remaining lines
        1;
    " "$filename" > "$filename.new"
    mv "$filename".new "$filename"
}

for manpage in bsdtar.1 bsdcpio.1
do
    installed_manpage=`find "$RPM_BUILD_ROOT" -name "$manpage"`
    replace "$installed_manpage"
done

# As the package is for a specific major version,
# the development files need to be moved in specific
# folders, as as to not overlap with the pristine
# libarchive package
mkdir -p $RPM_BUILD_ROOT{%{_includedir},%{_libdir}}/%{name}
mv -f $RPM_BUILD_ROOT%{_includedir}/archive*.h $RPM_BUILD_ROOT%{_includedir}/%{name}
mv -f $RPM_BUILD_ROOT%{_libdir}/{pkgconfig,%{name}}
for library in $RPM_BUILD_ROOT%{_libdir}/*.so
do
  rm -f $library
  ln -s ../$(basename $library).%{sonamever} $RPM_BUILD_ROOT%{_libdir}/%{name}/$(basename $library)
done


%check
%if %{with check}
logfiles ()
{
    find -name '*_test.log' -or -name test-suite.log
}

tempdirs ()
{
    cat `logfiles` \
        | awk "match(\$0, /[^[:space:]]*`date -I`[^[:space:]]*/) { print substr(\$0, RSTART, RLENGTH); }" \
        | sort | uniq
}

cat_logs ()
{
    for i in `logfiles`
    do
        echo "=== $i ==="
        cat "$i"
    done
}

run_testsuite ()
{
    rc=0
    %make_build check -j1 || {
        # error happened - try to extract in koji as much info as possible
        cat_logs

        for i in `tempdirs`; do
            if test -d "$i" ; then
                find $i -printf "%p\n    ~> a: %a\n    ~> c: %c\n    ~> t: %t\n    ~> %s B\n"
                cat $i/*.log
            fi
        done
        return 1
    }
    cat_logs
}

# On a ppc/ppc64 is some race condition causing 'make check' fail on ppc
# when both 32 and 64 builds are done in parallel on the same machine in
# koji.  Try to run once again if failed.
%ifarch ppc
run_testsuite || run_testsuite
%else
run_testsuite
%endif
%endif


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%{_libdir}/libarchive.so.%{sonamever}*

%files manpages
%{_mandir}/*/cpio.*
%{_mandir}/*/mtree.*
%{_mandir}/*/tar.*
%{_mandir}/*/archive*
%{_mandir}/*/libarchive*

%files devel
%{_includedir}/%{name}
%{_libdir}/%{name}

%files -n bsdtar%{version_suffix}
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%{_bindir}/bsdtar
%{_mandir}/*/bsdtar*

%files -n bsdcpio%{version_suffix}
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%{_bindir}/bsdcpio
%{_mandir}/*/bsdcpio*

%files -n bsdcat%{version_suffix}
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%{_bindir}/bsdcat
%{_mandir}/*/bsdcat*


%changelog
* Sat Apr 25 2020 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 3.4.2-1
- Initial on EPEL 8

