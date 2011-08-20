Summary: GNOME icon theme
Name: gnome-icon-theme
Version: 2.28.0
Release: 2%{?dist}
Source0: http://download.gnome.org/sources/gnome-icon-theme/2.28/%{name}-%{version}.tar.bz2
Source1: gnome-icon-theme-extra-device-icons-5.tar.bz2
Source2: legacy-icon-mapping.xml
Source3: window.png
Source4: gtk_print_icons.tar.bz2
License: GPL+
BuildArch: noarch
Group: User Interface/Desktops
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: icon-naming-utils >= 0.8.7
BuildRequires: pkgconfig
BuildRequires: gettext
BuildRequires: librsvg2
BuildRequires: intltool
Requires: hicolor-icon-theme
Requires: pkgconfig
Requires(post): gtk2 >= 2.6.2

# updated translations
# https://bugzilla.redhat.com/show_bug.cgi?id=589202
Patch0: gnome-icon-theme-translations.patch

%description
This package contains the default icon theme used by the GNOME desktop.

%prep
%setup -q
%patch0 -p1 -b .translations

%build
%configure --disable-hicolor-check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

## remove these bogus files
rm -rf $RPM_BUILD_ROOT/usr/share/locale/*

# create symlinks for gtk stock icons, these are not really 'legacy'
# this uses the legacy-icon-mapping.xml file in cvs
cd $RPM_BUILD_ROOT/usr/share/icons/gnome
for size in 8x8 16x16 22x22 24x24 32x32 48x48 scalable; do
  (
  cd $size
  for context in *; do
    if [ -d $context ]; then
      (
      cd $context
      INU_DATA_DIR=$RPM_SOURCE_DIR /usr/bin/icon-name-mapping -c $context
      )
    fi
  done
  )
done

tar xj -C $RPM_BUILD_ROOT/usr/share/icons/gnome -f %{SOURCE1}

cp %{SOURCE3} $RPM_BUILD_ROOT/usr/share/icons/gnome/16x16/apps

tar xj -C $RPM_BUILD_ROOT/usr/share/icons/gnome -f %{SOURCE4}

%clean
rm -rf $RPM_BUILD_ROOT

%post
for dir in /usr/share/icons/*; do
  if test -d "$dir"; then
    if test -f "$dir/index.theme"; then
      /usr/bin/gtk-update-icon-cache --quiet "$dir" || :
    fi
  fi
done

%files
%defattr(-,root,root)
%doc COPYING AUTHORS
%{_datadir}/icons/gnome
#%{_datadir}/icons/hicolor/*
%{_datadir}/pkgconfig/gnome-icon-theme.pc

%changelog
* Mon May 17 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.0-2
- Updated translations
Resolves: #589202

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Tue Aug 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.90-2
- Add gtk print icons.

* Fri Aug 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.90-1
- Update to 2.27.90

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-2
- Add a window icon so we don't show missing icons in window frames

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Sat Mar  7 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-3
- Add a 48x48 spinner back

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Feb 17 2009 David Zeuthen <davidz@redhat.com> - 2.24.0-3
- Update device icons

* Sun Nov 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Tweak summary and description

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Wed Jul 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3-2
- Re-add the symlinks for gtk stock icons again

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Fri Jun 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-2
- Re-add the symlinks for gtk stock icons, remove some other symlinks

* Tue Jun 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-1
- Update to 2.23.2

* Thu Apr 16 2008 David Zeuthen <davidz@redhat.com> - 2.22.0-6
- Refresh disc icons

* Tue Apr  1 2008 David Zeuthen <davidz@redhat.com> - 2.22.0-5
- Switch open and close padlock encrypted drives/media
- Replace the flash media icons with something that is compatible
  with the GPL that gnome-icon-theme is under (thanks Mike Langlie)

* Mon Mar 24 2008 David Zeuthen <davidz@redhat.com> - 2.22.0-4
- Rebuild

* Mon Mar 24 2008 David Zeuthen <davidz@redhat.com> - 2.22.0-3
- Switch media-encrypted and drive-encrypted

* Mon Mar 24 2008 David Zeuthen <davidz@redhat.com> - 2.22.0-2
- Add a bunch of device icons from Mike Langlie

* Tue Mar 11 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Tue Dec 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Tue Sep 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Rebuild with newer icon-naming-utils

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.91-1
- Update to 2.19.91

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-1
- Update to 2.19.90
- Further correction of the license field

* Fri Aug  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1
- Update to 2.19.6
- Update license field

* Wed Jun 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-1
- Update to 2.19.1

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.5-1
- Update to 2.17.5

* Wed Dec 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.4.1-1
- Update to 2.17.4.1

* Wed Dec 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.4-1
- Update to 2.17.4

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.3-1
- Update to 2.17.3

* Tue Nov 28 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2.1-2
- Fix duplicate emblems in nautilus (#217090)

* Sun Nov 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2.1-1
- Update to 2.17.2.1

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Wed Oct  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0.1-2
- Fix broken symlinks (#208399)

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0.1-1
- Update to 2.16.0.1

* Sun Sep  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1
- Update to 2.16.0

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> 2.15.92-1.fc6
- Update to 2.15.92
- Require pkgconfig

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> 2.15.91-1.fc6
- Update to 2.15.91

* Thu Aug  2 2006 Matthias Clasen <mclasen@redhat.com> 2.15.90-1.fc6
- Update to 2.15.90

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> 2.15.3-1
- Update to 2.15.3

* Wed Jun  7 2006 Matthias Clasen <mclasen@redhat.com> 2.15.2-3
- Fix a problem in %%post (#194323)

* Tue Jun  6 2006 Matthias Clasen <mclasen@redhat.com> 2.15.2-2
- Add BuildRequires for perl-XML-Parser

* Tue May 16 2006 Matthias Clasen <mclasen@redhat.com> 2.15.2-1
- Update to 2.15.2

* Tue May  9 2006 Matthias Clasen <mclasen@redhat.com> 2.15.1-1
- Update to 2.15.1

* Wed Mar 22 2006 Matthias Clasen <mclasen@redhat.com> 2.14.2-2
- Update to 2.14.2
- Add symlinks to make application/xml work

* Sat Feb 25 2006 Matthias Clasen <mclasen@redhat.com> 2.14.1-1
- Update to 2.14.1

* Wed Feb 15 2006 Matthias Clasen <mclasen@redhat.com> 2.14.0-2
- Add small epiphany icon (again!!)

* Sun Feb 12 2006 Ray Strode <rstrode@redhat.com> 2.14.0-1
- Update to 2.14.0

* Thu Feb  9 2006 Matthias Clasen <mclasen@redhat.com> 2.13.7-4
- Add better shutdown icon

* Thu Feb  9 2006 Matthias Clasen <mclasen@redhat.com> 2.13.7-3
- Add the spinner back

* Tue Feb  7 2006 Matthias Clasen <mclasen@redhat.com> 2.13.7-2
- Add back some icons that went missing
- Fix redhat- symlinks that were broken since FC1

* Mon Feb  6 2006 Matthias Clasen <mclasen@redhat.com> 2.13.7-1
- Update to 2.13.7

* Mon Jan 23 2006 Matthias Clasen <mclasen@redhat.com> 2.13.5.1-2
- Fix a typo in index.theme

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> 2.13.5.1-1
- Update to 2.13.5.1
- BuildRequire icon-naming-utils

* Tue Jan 03 2006 Matthias Clasen <mclasen@redhat.com> 2.13.4-1
- Update to 2.13.4

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.13.2-1
- Update to 2.13.2

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.1-2
- Update to 2.12.1

* Sat Oct  1 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-2
- Only call gtk-update-icon-cache on directories which have a
  theme index file

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- update to 2.12.0

* Fri Jul 08 2005 John (J5) Palmieri <johnp@redhat.com> - 2.10.1-6
- update the redone icons with new ones from dfong

* Tue Jul 05 2005 John (J5) Palmieri <johnp@redhat.com> - 2.10.1-5
- replace some upstream icons with redone ones 

* Wed Apr 13 2005 John (J5) Palmieri <johnp@redhat.com> - 2.10.1-4
- Fix redhat-office link

* Wed Apr 13 2005 John (J5) Palmieri <johnp@redhat.com> - 2.10.1-3
- More relative symlink fixes

* Tue Apr 12 2005 Matthias Clasen <mclasen@redhat.com> - 2.10.1-2
- Use relative symlinks instead of absolute ones, 
  which the build system no longer accepts.

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> - 2.10.1-1
- Update to upstream version 2.10.1

* Thu Mar 17 2005 John (J5) Palmieri <johnp@redhat.com> - 2.9.92-1
- Update to upstream version 2.9.92

* Sun Mar  7 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.91-2
- Fix %%post 

* Wed Feb  9 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.91-1
- Update to 2.9.91

* Fri Feb  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.90-3
- Silence %%post

* Fri Jan 28 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.90-2
- Prereq gtk2 since we use gtk-update-icon-cache in %%post

* Thu Jan 27 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.90-1
- Update to 2.9.90
- Update icon caches in %%post

* Wed Sep 22 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Wed Sep  1 2004 Alexander Larsson <alexl@redhat.com> - 2.7.90-2
- Import copies of fallback icon in other packages (#128800, #114534)

* Tue Aug 31 2004 Alex Larsson <alexl@redhat.com> 2.7.90-1
- update to 2.7.90

* Wed Aug  4 2004 Owen Taylor <otaylor@redhat.com> - 1.3.6-1
- Update to 1.3.6

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr  1 2004 Alex Larsson <alexl@redhat.com> 1.2.0-1
- update to 1.2.0

* Wed Mar 10 2004 Alexander Larsson <alexl@redhat.com> 1.1.90-1
- update to 1.1.90

* Wed Mar  3 2004 Alexander Larsson <alexl@redhat.com> 1.1.8-2
- remove redhat-main-menu symlink (#100407)

* Mon Feb 23 2004 Alexander Larsson <alexl@redhat.com> 1.1.8-1
- update to 1.1.8

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 19 2004 Alexander Larsson <alexl@redhat.com> 1.1.5-1
- 1.1.5
- Removed hidden patch. Why should gnome not be visible?
  Its not like you don't see all the kde themes from Gnome, and
  they don't work well in Gnome.

* Thu Oct  9 2003 Alexander Larsson <alexl@redhat.com> 1.0.9-2
- Fix symlinks for redhat menu icons

* Fri Oct  3 2003 Alexander Larsson <alexl@redhat.com> 1.0.9-1
- update to 1.0.9

* Tue Jul 15 2003 Matt Wilson <msw@redhat.com> 1.0.6-1
- update to 1.0.6

* Wed Jul  9 2003 Alexander Larsson <alexl@redhat.com> 1.0.5-1.E
- Rebuild

* Tue Jul  1 2003 Alexander Larsson <alexl@redhat.com> 1.0.5-1
- Update to 1.0.5

* Fri Jun 13 2003 Elliot Lee <sopwithredhat.com> 1.0.2-3
- Update evolution icon link again

* Fri May 16 2003 Alexander Larsson <alexl@redhat.com> 1.0.2-2
- Update evolution icon link (#90050)

* Mon Mar 31 2003 Alexander Larsson <alexl@redhat.com> 1.0.2-1
- Update to 1.0.2

* Sun Feb 16 2003 Than Ngo <than@redhat.com> 1.0.0-4
- remove kde hicolor patch, it's not required anymore
- add patch to make gnome icon theme hidden in KDE

* Mon Feb 10 2003 Alexander Larsson <alexl@redhat.com> 1.0.0-3
- inherit from hicolor to make kde work

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Alexander Larsson <alexl@redhat.com> 1.0.0-1
- Update to 1.0.0

* Fri Jan 17 2003 Havoc Pennington <hp@redhat.com> 0.1.5-2
- make the gnome theme contain some symlinks to cover 
  the redhat-*.png names

* Mon Dec 16 2002 Alexander Larsson <alexl@redhat.com> 0.1.5-1
- Update to 0.1.5

* Wed Dec  4 2002 Alexander Larsson <alexl@redhat.com> 0.1.3-1
- Initial build.
