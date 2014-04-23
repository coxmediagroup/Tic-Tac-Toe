
Background
==============


Installation
=================

Installation instructions, and specific notes as needed.


MacOS X
-------------

Installing Pillow on MacOS X 10.9 with XCode 5.1 fails with:

    clang: unknown argument: '-mno-fused-madd'

To fix this, the environment was adjusted thus:

    ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future

when running pip on Darwin.

