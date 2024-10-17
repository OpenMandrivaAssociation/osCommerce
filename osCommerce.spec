%define snap 20040510
%define teproot /var/www/html/%{name}
%define _requires_exceptions pear(includes/local/configure.php)

Summary:	E-commerce solution (aka. "tep")
Name:		osCommerce
Version:	2.2
Release:	%mkrel 1.%{snap}_MS3.6
License:	GPL
Group:		System/Servers
URL:		https://www.oscommerce.com/
#Source0:	http://telia.dl.sourceforge.net/sourceforge/tep/oscommerce-2.2ms1.tar.gz
#Source1:	http://telia.dl.sourceforge.net/sourceforge/tep/oscommerce-2.2ms1.tar.gz.sig
Source0:	oscommerce-2.2MS3-%{snap}.tar.bz2
#Source2:	tep-docs-20030218.tar.bz2
Requires:	mod_php
Requires:	php-mysql
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
osCommerce is an open source e-commerce solution under on going
development by the open source community. Its feature packed
out-of-the-box installation allows store owners to setup, run, and
maintain their online stores with minimum effort and with no costs
involved.

osCommerce combines open source solutions to provide a free and
open development platform, which includes the powerful PHP web
scripting language, the stable Apache web server, and the fast
MySQL database server.

With no restrictions or special requirements, osCommerce is able
to run on any PHP3 or PHP4 enabled web server, on any environment
that PHP and MySQL supports, which includes Linux, Solaris, BSD,
and Microsoft Windows environments

osCommerce is also known as "The Exchange Project".

%package	admin
Summary:	Administrative web interface for osCommerce
Group:		System/Servers
Requires:	%{name} = %{version}

%description	admin
Administrative web interface for osCommerce

%package	documentation
Summary:	The online documentation for osCommerce
Group:		System/Servers

%description	documentation
The online (and outdated!) documentation for osCommerce

%prep

%setup -q -n oscommerce-2.2MS3

%build

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# fix dir perms
find . -type d | xargs chmod 755

# fix file perms
find . -type f | xargs chmod 644

# don't ship win32 stuff
rm -rf catalog/extras/win32
rm -f tep-docs/documentation/install_win32.php

%install
rm -rf %{buildroot}

install -d %{buildroot}%{teproot}

cp -ar admin/admin %{buildroot}%{teproot}/
cp -ar catalog/catalog/* %{buildroot}%{teproot}/
cp -ar tep-docs/documentation %{buildroot}%{teproot}/

# fix admin docs
cp admin/INSTALL INSTALL.admin
cp admin/STANDARD STANDARD.admin
cp admin/TODO TODO.admin

# fix catalog docs
cp catalog/CHANGELOG CHANGELOG.catalog
cp catalog/FAQ FAQ.catalog
cp catalog/INSTALL INSTALL.catalog
cp catalog/README README.catalog
cp catalog/STANDARD STANDARD.catalog
cp catalog/TODO TODO.catalog
cp catalog/tep_database-pr2.2-CVS.pdf tep_database-pr2.2-CVS.pdf

# fix extras docs
cp -ar catalog/extras .

# make a silly link...
#ln -s default.php %{buildroot}%{teproot}/index.php

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc CHANGELOG.catalog FAQ.catalog INSTALL.catalog README.catalog STANDARD.catalog 
%doc TODO.catalog tep_database-pr2.2-CVS.pdf extras
%exclude %{teproot}/admin
#%exclude %{teproot}/includes/configure.php
%config(noreplace) %attr(0706,apache,apache) %{teproot}/includes/configure.php
%exclude %{teproot}/documentation
%{teproot}

%files		admin
%defattr(-, root, root)
%doc INSTALL.admin STANDARD.admin TODO.admin
#%exclude %{teproot}/admin/includes/configure.php
%config(noreplace) %attr(0706,apache,apache) %{teproot}/admin/includes/configure.php
%{teproot}/admin

%files		documentation
%defattr(-, root, root)
%{teproot}/documentation


