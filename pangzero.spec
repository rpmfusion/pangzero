%global github_repo https://github.com/jwrdegoede/pangzero/archive/%{commit}
%global commit      259f9679773273cb0b8ec5026046f5f27af1b0c0
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           pangzero
Version:        1.4.1
Release:        23%{?dist}
Summary:        A clone and enhancement of Super Pang
Group:          Amusements/Games
License:        GPLv2
URL:            http://apocalypse.rulez.org/pangzero
Source0:        %{github_repo}/pangzero-%{shortcommit}.tar.gz
Source3:        %{name}.appdata.xml
BuildArch:      noarch
BuildRequires:  desktop-file-utils
#BuildRequires:  lame
BuildRequires:  perl-SDL >= 2.536
BuildRequires:  vorbis-tools
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(File::ShareDir)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
Requires:       hicolor-icon-theme
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Pang Zero is a clone and enhancement of Super Pang, a fast-paced action game
that involves popping balloons with a harpoon. Currently up to 6 people can
play together.


%prep
%setup -q -n pangzero-%{commit}

# Convert audio, Fedora's SDL does not support MP3
#lame --silent --decode data/UPiPang.mp3 - | oggenc -Q - -o data/UPiPang.ogg


%build
perl Build.PL --installdirs vendor
./Build


%install
./Build install --destdir=%{buildroot}
rm %{buildroot}%{perl_vendorarch}/auto/Games/PangZero/.packlist
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/
desktop-file-install --vendor "" \
                     --dir %{buildroot}%{_datadir}/applications \
                     %{name}.desktop
install -m0644 data/icon.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -m 0644 -D %{SOURCE3} %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%if 0%{?rhel} && 0%{?rhel} < 8
%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
%endif


%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/pangzero
%{perl_vendorlib}/Games/
%{perl_vendorlib}/auto/
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%exclude %{perl_vendorlib}/auto/share/dist/Games-PangZero/icon.ico
%exclude %{perl_vendorlib}/auto/share/dist/Games-PangZero/icon.png
%{_metainfodir}/%{name}.appdata.xml


%changelog
* Tue Jun 21 2022 Paul Howarth <paul@city-fan.org> - 1.4.1-23
- Perl 5.36 rebuild

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.4.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 16 2021 Leigh Scott <leigh123linux@gmail.com> - 1.4.1-20
- Rebuild for new perl version

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 02 2020 Paul Howarth <paul@city-fan.org> - 1.4.1-17
- Perl 5.32 rebuild

* Sun Mar 01 2020 Sérgio Basto <sergio@serjux.com> - 1.4.1-16
- Add appdata file, copied from
  https://github.com/sanjayankur31/rpmfusion-appdata

* Sun Mar 01 2020 Sérgio Basto <sergio@serjux.com> - 1.4.1-15
- Add appdata file, copied from
  https://github.com/sanjayankur31/rpmfusion-appdata

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 05 2018 Sérgio Basto <sergio@serjux.com> - 1.4.1-11
- Upstream code now have pangzero.desktop
- Use original mp3 (SDL now should support MP3)
- Improve some scriplets

* Mon Sep 03 2018 Sérgio Basto <sergio@serjux.com> - 1.4.1-10
- New upstream commit

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 15 2017 Paul Howarth <paul@city-fan.org> - 1.4.1-6
- Perl 5.26 rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 30 2016 Sérgio Basto <sergio@serjux.com> - 1.4.1-4
- Add perl-generators to get proper requires/provides on F-25 and later

* Fri Sep 30 2016 Sérgio Basto <sergio@serjux.com> - 1.4.1-3
- Rebuild for Perl with locale (buildroot with glibc-all-langpacks)

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Oct 28 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.1-1
- New upstream: https://github.com/jwrdegoede/pangzero
- New upstream version 1.4.1, which works with latest perl-SDL

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
