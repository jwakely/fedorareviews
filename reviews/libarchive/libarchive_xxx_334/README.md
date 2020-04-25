`libarchive3.4` on RedHat/CentOS 8
==================================

# Overview
Newer versions of `libarchive` are required, for instance for newer versions
of CMake (_e.g._, 3.17, like on Fedora Rawhide or 33).
I indeed intend to package CMake3.17 for EPEL 8.

On RHEL/CentOS 8, `libarchive` version is `3.3.2`.
For both versions of `libarchive`, the SO version is `13`.

This directory gives the RPM specification file to package `libarchive3.4`.
It is however not possible to install the resulting RPM binary packages,
because of a conflict on the shared library: the SO version is the same
for both versions of `libarchive`, more specifically `libarchive.so.13`.

## See also
* [Bugzilla #18227927](https://bugzilla.redhat.com/show_bug.cgi?id=1827927),
  upgrade request for `libarchive` from `3.3.2` to `3.4.2`.
* [Spec file for `libarchive3.4`](https://github.com/fedorapackaging/fedorareviews/blob/master/reviews/libarchive/libarchive_xxx_334/libarchive3.4.spec)
* [Source RPM](https://kojipkgs.fedoraproject.org//work/tasks/5794/43775794/libarchive3.4-3.4.2-1.el8.src.rpm)
* [Successful build](https://koji.fedoraproject.org/koji/taskinfo?taskID=43775785)
* [Supporting content](https://github.com/fedorapackaging/fedorareviews/blob/master/reviews/libarchive/libarchive_xxx_334/)


# Steps

## Build on Koji
* Launch a build on Koji:
```bash
$ koji build --arch-override=x86_64 --scratch --nowait epel8 ~/dev/packages/SRPMS/libarchive3.4-3.4.2-1.el8.src.rpm 
Uploading srpm: /home/build/dev/packages/SRPMS/libarchive3.4-3.4.2-1.el8.src.rpm
[====================================] 100% 00:00:14   6.66 MiB 462.74 KiB/sec
Created task: 43775785
Task info: https://koji.fedoraproject.org/koji/taskinfo?taskID=43775785
```

* Resulting build: https://koji.fedoraproject.org/koji/taskinfo?taskID=43775785


