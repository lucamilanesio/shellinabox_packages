Native packages for ShellInABox project
=======================================
This project contains the spec files for packaging ShellInAbox including the 
fix for Issue [#275]: https://code.google.com/p/shellinabox/issues/detail?id=275 

In order to build the packages, you need to have rpmbuild installed and 
the ShellInABox build dependencies:
- make
- gcc
- openssl-devel
- zlib-devel
- rpm-build
- wget

To install those dependencies before build:
   
    $ yum install make gcc openssl-devel zlib-devel rpm-build wget

To build all packages:

    $ make

