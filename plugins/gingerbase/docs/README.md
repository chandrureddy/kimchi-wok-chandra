Ginger Base Plugin
==============

Ginger Base is an open source base host management plugin for Wok
(Webserver Originated from Kimchi), that provides an intuitive web panel with
common tools for configuring and managing the Linux systems.

Wok is a cherrypy-based web framework with HTML5 support that is extended by
plugins which expose functionality through REST APIs.

The current features of Base Host Management of Linux system include:
    + Shutdown, Restart, Connect
    + Basic Information
    + System Statistics
    + Software Updates
    + Repository Management
    + Debug Reports (SoS Reports)

Browser Support
===============

Desktop Browser Support:
-----------------------
* **Internet Explorer:** IE9+
* **Chrome:** Current-1 version
* **Firefox:** Current-1 version Firefox 24ESR
* **Safari:** Current-1 version
* **Opera:** Current-1 version

Mobile Browser Support:
-----------------------
* **Safari iOS:** Current-1 version
* **Android Browser** Current-1 version

Current-1 version denotes that we support the current stable version of the
browser and the version that preceded it. For example, if the current version of
a browser is 24.x, we support the 24.x and 23.x versions.This does not mean that
kimchi cannot be used in other browsers, however, functionality and appearance
may be diminished and we may not be able to provide support for any problems you
find.

Hypervisor Distro Support
=========================

Ginger Base and Wok might run on any GNU/Linux distribution that meets the conditions
described on the 'Getting Started' section below.

The Kimchi community makes an effort to test it with the latest versions of
Fedora, RHEL, OpenSuSe, and Ubuntu.

Getting Started
===============

Install Dependencies
--------------------

**For fedora and RHEL:**

     $ sudo yum install gcc make autoconf automake gettext-devel git \
                        python-cherrypy python-cheetah \
                        python-jsonschema rpm-build \
                        python-psutil sos python-lxml \
                        libxslt pyparted \
                        python-websockify python-configobj

     # If using RHEL, install the following additional packages:
     $ sudo yum install python-unittest2 python-ordereddict

     # Restart libvirt to allow configuration changes to take effect
     $ sudo service libvirtd restart

    Packages version requirement:
        python-psutil >= 0.6.0

    # These dependencies are only required if you want to run the tests:
    $ sudo yum install pyflakes python-pep8 python-requests

*Note for RHEL users*: Some of the above packages are located in the Red Hat
EPEL repositories.  See
[this FAQ](http://fedoraproject.org/wiki/EPEL#How_can_I_use_these_extra_packages.3F)
for more information on how to configure your system to access this repository.

And for RHEL7 systems, you also need to subscribe to the "RHEL Server Optional"
channel at RHN Classic or Red Hat Satellite.

**For debian:**

    $ sudo apt-get install gcc make autoconf automake gettext git \
                           python-cherrypy3 python-cheetah \
                           python-configobj python-jsonschema \
                           python-psutil sosreport \
                           python-lxml xsltproc \
                           python-parted websockify 

    Packages version requirement:
        python-jsonschema >= 1.3.0
        python-psutil >= 0.6.0

    # These dependencies are only required if you want to run the tests:
    $ sudo apt-get install pep8 pyflakes python-requests

**For openSUSE:**

    $ sudo zypper install gcc make autoconf automake gettext-tools git \
                          python-CherryPy python-Cheetah \
                          python-jsonschema rpm-build \
                          python-psutil python-lxml \
                          libxslt-tools python-xml python-parted \
                          python-configobj python-websockify 

    Packages version requirement:
        python-psutil >= 0.6.0

    # These dependencies are only required if you want to run the tests:
    $ sudo zypper install python-pyflakes python-pep8 python-requests

*Note for openSUSE users*: Some of the above packages are located in different
openSUSE repositories. See
[this FAQ](http://download.opensuse.org/repositories/home:GRNET:synnefo/) for
python-parted; And
[this FAQ](http://en.opensuse.org/SDB:Add_package_repositories) for more
information on how configure your system to access this repository.

Build and Install
-----------------

    Wok:
    $ ./autogen.sh --system

    $ make
    $ sudo make install   # Optional if running from the source tree


    Ginger Base:
    $ cd plugins/ginger-basae

    $ ./autogen.sh --system

    $ make
    $ sudo make install   # Optional if running from the source tree

Run
---

    $ systemctl start wokd
    

Test
----

    $ cd plugins/gingerbase
    $ make check-local # check for i18n and formatting errors
    $ sudo make check

After all tests are executed, a summary will be displayed containing any
errors/failures which might have occurred.

Usage
-----

Connect your browser to https://localhost:8001.  You should see a screen like:

![Wok Login Screen](docs/kimchi-login.png)

Wok uses PAM to authenticate users so you can log in with the same username
and password that you would use to log in to the machine itself.

![Ginger Base Host Screen](docs/gingerbase-host-tab.png)

Ginger Base Host tab provides the base host functionality like system information,
 system statistics, software updates, repositories and debug reports functionality.
 
Also Ginger Base provides shutdown, re-start and connect options.

Participating
-------------

All patches are sent through our mailing list hosted by oVirt.  More
information can be found at:

https://github.com/kimchi-project/kimchi/wiki/Communications

Patches should be sent using git-send-email to kimchi-devel@ovirt.org.
