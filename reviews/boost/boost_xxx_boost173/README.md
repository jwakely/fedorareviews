Boost 1.73 on RedHat/CentOS 8
=============================

# Overview

This directory gives the RPM specification file to package `boost1.73`.

## See also
* [Bugzilla #XXX - Boost1.73](https://bugzilla.redhat.com/show_bug.cgi?id=),
* [Spec file for `boost1.73`](https://github.com/fedorapackaging/fedorareviews/blob/master/reviews/boost/boost_xxx_boost173/boost1.73.spec)
* [Source RPM](https://kojipkgs.fedoraproject.org//work/tasks/2933/43782933/boost-1.73.0-0.1.fc33.src.rpm)
* [Successful build fpr Rawhide](ihttps://koji.fedoraproject.org/koji/taskinfo?taskID=43782815)
* [Successful build for EPEL 8](https://koji.fedoraproject.org/koji/taskinfo?taskID=43783760)
* [Supporting content](https://github.com/fedorapackaging/fedorareviews/blob/master/reviews/boost/boost_xxx_boost173/)


# Steps

## Build locally
* Retrieve the sources:
```bash
$ wget https://dl.bintray.com/boostorg/master/boost_1_73_0-snapshot.tar.gz -O ~/dev/packages/SOURCES/boost_1_73_0_rc1.tar.gz
```

* Copy the sources (patches) to `~/dev/packages/SOURCES/`:
```bash
$ cp boost1.73.spec ~/dev/packages/SPECS/boost1.73-1.73.0-1.spec
$ cp *.patch *.so ~/dev/packages/SOURCES/
$ pushd ~/dev/packages/SPECS/
$ ln -sf boost1.73-1.73.0-1.spec boost1.73.spec
$ popd
```

* Launch the build:
```bash
$ pushd ~/dev/packages/SPECS/
$ rpmbuild -bs boost1.73.spec
$ rpmbuild -ba boost1.73.spec
$ popd
```

## Build on Koji
* Launch a build on Koji:
```bash
$ koji build --arch-override=x86_64 --scratch --nowait epel8 ~/dev/packages/SRPMS/boost-1.73.0-0.1.el8.src.rpm
Uploading srpm: ~/dev/packages/SRPMS/boost-1.73.0-0.1.el8.src.rpm
[====================================] 100% 00:00:14   6.66 MiB 462.74 KiB/sec
Created task: 43783760
Task info: https://koji.fedoraproject.org/koji/taskinfo?taskID=43783760
```

* Resulting build: https://koji.fedoraproject.org/koji/taskinfo?taskID=43783760


