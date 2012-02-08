Name:           pangzero
Version:        1.3
Release:        4%{?dist}
Summary:        A clone and enhancement of Super Pang
Group:          Amusements/Games
License:        GPLv2
URL:            http://apocalypse.rulez.org/pangzero
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
Patch0:         pangzero-1.2-nowin32.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  lame
BuildRequires:  perl-SDL >= 2.1.0
BuildRequires:  vorbis-tools
Requires:       hicolor-icon-theme

%description
Pang Zero is a clone and enhancement of Super Pang, a fast-paced action game
that involves popping balloons with a harpoon. Currently up to 6 people can
play together.


%prep
%setup -q
%patch0 -p1

# Set the data location
sed -i 's|$::DataDir = '`echo -e "\047\047"`'|$::DataDir = '`echo -e "\047%{_datadir}/%{name}\047"`'|' bin/pangzero

# Convert audio, Fedora's SDL does not support MP3
lame --silent --decode data/UPiPang.mp3 - | oggenc -Q - -o data/UPiPang.ogg ||:

# Use the ogg instead of mp3
sed -i 's|UPiPang.mp3|UPiPang.ogg|' bin/pangzero


%build
%configure
make %{?_smp_mflags}



%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/
install -m0644 data/UPiPang.ogg %{buildroot}%{_datadir}/%{name}

desktop-file-install --vendor "" \
                     --dir %{buildroot}%{_datadir}/applications \
                     %{SOURCE1}

install -m0644 data/icon.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/pangzero
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%exclude %{_datadir}/%{name}/UPiPang.mp3
%exclude %{_datadir}/%{name}/icon.ico


%changelog
* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3-3
- rebuild for new F11 features

* Mon Sep 08 2008 Xavier Lamien <lxtnow[at]gmail.com> - 1.3-2
- Update for rpmfusion inclusion.

* Mon Jan 07 2008 Ian Chapman <packages[AT]amiga-hardware.com> 1.3-1
- Upgrade to 1.3
- License change due to new guidelines

* Fri Jun 29 2007 Ian Chapman <packages[AT]amiga-hardware.com> 1.2-1
- Upgrade to 1.2
- Minor changes to spec due to new guidelines
- Updated patch as some fixes are now fixed upstream

* Thu Jan 04 2007 Ian Chapman <packages[AT]amiga-hardware.com> 1.1-1
- Upgrade to 1.1
- Patched so perl(Win32) is not picked up as a dependancy
- Patched so that view website on exit works properly
- Patched for ogg audio as perl-SDL no longer supports MP3 since moving to FE
- Added vorbis-tools and lame BRs for audio conversion
- Use the icon supplied in this version instead of our own

* Wed Nov 01 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.15-2
- Rebuild due to perl-SDL 1 -> 2 upgrade on FC5
- Now requires perl SDL 2+ on all supported FCs.

* Sat Oct 14 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.15-1
- Upgrade to 0.15
- Updated perl-SDL2 patch

* Fri Oct 06 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.14-1
- Upgrade to 0.14
- Updated perl-SDL2 patch
- Added perl-SDL buildrequire as configure now checks to see if it's installed

* Sat Aug 26 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.12-2
- Added patch to run with perl-SDL v2 on FC6 courtesy of Hans de Goede

* Sat Aug 12 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.12-1
- Upgraded to 0.12
- Dropped my division by zero patch as it's been merged upstream

* Sun Jul 30 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.11-3
- Added patch to fix division by zero (BZ #10)

* Sun Jul 23 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.11-2
- Don't use /usr/share/games/%%{name} as that is deprecated too.

* Thu Jul 20 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.11-1
- Initial Release
