#!/bin/bash

echo koji build --arch-override=x86_64 --scratch --nowait rawhide ~/dev/packages/SRPM/boost-my.src.rpm

