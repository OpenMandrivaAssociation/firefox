#
# WARNING, READ FIRST:
#
# This is a special package that needs special treatment. Due to the amount of
# security updates it needs, it's common to ship new upstream versions instead of patching.
# That means this package MUST be BUILDABLE for stable official releases.
# This also means only STABLE upstream releases, NO betas.
# This is a discussed topic. Please, do not flame it again.

%define firefox_appid \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
%define mozillalibdir %{_libdir}/%{name}-%{version}
%define pluginsdir %{_libdir}/mozilla/plugins

# libxul.so is provided by libxulrunnner2.0.
%if %{_use_internal_dependency_generator}
%define __noautoreq 'libxul.so'
%else
%define _requires_exceptions libxul.so
%endif

# this seems fragile, so require the exact version or later (#58754)
%define sqlite3_version %(pkg-config --modversion sqlite3 &>/dev/null && pkg-config --modversion sqlite3 2>/dev/null || echo 0)
%define nss_version %(pkg-config --modversion nss &>/dev/null && pkg-config --modversion nss 2>/dev/null || echo 0)
%define nspr_version %(pkg-config --modversion nspr &>/dev/null && pkg-config --modversion nspr 2>/dev/null |sed -e 's!\.0!!' || echo 0)

%define update_channel  release

Summary:	Next generation web browser
Name:		firefox
Epoch:		0
# IMPORTANT: When updating, you MUST also update the firefox-l10n package
# because its subpackages depend on the exact version of Firefox it was
# built for.
Version:	23.0
Release:	1
License:	MPLv1+
Group:		Networking/WWW
Url:		http://www.mozilla.com/firefox/
%if 0%{?prel}
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/%{name}/releases/%{version}/source/%{name}-%{version}%{prel}.source.tar.bz2
%else
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/%{name}/releases/%{version}/source/%{name}-%{version}.source.tar.bz2
%endif
Source4:	%{name}.desktop
Source5:	firefox-searchengines-jamendo.xml
Source6:	firefox-searchengines-exalead.xml
Source8:	firefox-searchengines-askcom.xml
Source9:	kde.js
Source10:	firefox-searchengines-yandex.xml
Source11:	firefox-searchengines-google.xml
Source12:	firefox-searchengines-bing.xml
Patch1:		firefox-6.0-lang.patch
Patch2:		firefox-vendor.patch
Patch3:		mozilla-firefox-1.5.0.6-systemproxy.patch
Patch4:		firefox-17.0-nss-binary.patch
# (OpenSuse) add patch to make firefox always use /usr/bin/firefox when "make firefox
# the default web browser" is used fix mdv bug#58784
Patch5:		firefox-6.0-appname.patch
Patch6:		firefox-7.0-fix-str-fmt.patch
Patch7:		mozilla-firefox-run-mozilla.patch
Patch8:		firefox-18.0-tirpc.patch
Patch9:		firefox-5.0-asciidel.patch
Patch10:	firefox-3.5.3-default-mail-handler.patch
# Patches for kde integration of FF 
Patch11:	firefox-18.0-kde.patch
Patch12:	mozilla-18.0-kde.patch
Patch13:	firefox-13-fix-nspr-include.patch
Patch14:        firefox-18.0-fix-cairo-build.patch
Patch34:	xulrunner_nojit.patch
# (cjw) use system virtualenv
Patch36:	firefox-17.0-virtualenv.patch
# (tpg) from Mageia use system-wide ogg
Patch37:	firefox-18.0.1-system-ogg.patch
# (tpg) from Mageia use mozilla ogg player instead of gstreamer
Patch38:	firefox-17.0-moz-ogg.patch
#fedya
Patch39:	this_realloc-mozilla21.patch

#BuildConflicts:	libreoffice-core
BuildRequires:	doxygen
BuildRequires:	makedepend
BuildRequires:	python
BuildRequires:	python-virtualenv
BuildRequires:	python-distribute
BuildRequires:	rootcerts >= 1:20110830.00
BuildRequires:	unzip
BuildRequires:	wget
BuildRequires:	zip
BuildRequires:	bzip2-devel
BuildRequires:	jpeg-devel
BuildRequires:	libiw-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(cairo) >= 1.10
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(gstreamer-plugins-base-0.10)
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(hunspell)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(libIDL-2.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libpng) >= 1.4
BuildRequires:	pkgconfig(libproxy-1.0)
%if %mdvver >= 201300
BuildRequires:	pkgconfig(libpulse)
%endif
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(sqlite3) >= 3.7.7.1
BuildRequires:	pkgconfig(theoradec)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(vpx)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	nss-static-devel
%ifnarch %arm %mips
BuildRequires:	valgrind
BuildRequires:	java-rpmbuild
BuildRequires:	yasm >= 1.0.1
%endif
Requires:	indexhtml
# fixes bug #42096
Requires:	mailcap
Requires:	xdg-utils
Suggests:	%{_lib}canberra0
Suggests:	%{_lib}cups2

%if 0%{?prel}
Provides:	%{name} = %{epoch}:%{version}-0.%{prel}
%else
Provides:	%{name} = %{epoch}:%{version}
%endif
Provides:	mozilla-firefox = %{epoch}:%{version}-%{release}
Provides:	webclient

Obsoletes:	firefox-ext-weave-sync
Obsoletes:	firefox-beta < 11

%description
The award-winning Web browser is now faster, more secure, and fully
customizable to your online life. With Firefox(R), we've added powerful new
features that make your online experience even better. It is an 'open source'
product which is  freely available, and is acquiring a growing proportion of
international web browser usage.

Firefox claims to offer a more secure web browsing experience than other
products, with better protection against spyware and other Internet-based
security threats.  It includes all the standard features of a modern web
browser, like Internet searching, tracking recently visited sites, setting up
shortcuts to favourite sites, customising the software behaviour and so on.
Firefox also includes  features like 'tabbed browsing' (opening several web
sites as sections within the same window) and methods for controlling pop-up
windows, cookies and downloaded files.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Other
Obsoletes:	firefox-beta-devel < 11

%description	devel
Files and macros mainly for building Firefox extensions.

%prep
%setup -qn mozilla-%update_channel
%patch1 -p1 -b .lang
%patch2 -p1 -b .vendor
#patch3 -p1 -b .systemproxy
#%patch4 -p1 -b .nsspatch
%patch5 -p1 -b .appname
# It was disabled because firefox3 hangs when using soundwrapper
#patch7 -p1
%patch8 -p0 -b .tirpc
%patch9 -p1 -b .ascii
%patch10 -p1 -b .default-mail-handler
%patch14 -p1

## KDE INTEGRATION
# Disable kde integration , need refactoring
#patch11 -p1 -b .kdepatch
#patch12 -p1 -b .kdemoz

%ifarch %arm
%if "%{_target_cpu}" != "armv7l"
%patch34 -p1
%patch39 -p1
%endif
%endif
#patch36 -p1 -b .system-virtualenv
#patch37 -p1
#patch38 -p1

#pushd js/src
#autoconf-2.13
#popd
#autoconf-2.13

# needed to regenerate certdata.c
pushd security/nss/lib/ckfw/builtins
perl ./certdata.perl < /etc/pki/tls/mozilla/certdata.txt
popd

%build
#(tpg) do not use serverbuild or serverbuild_hardened macros
# because compile will fail of missing -fPIC  :)
%setup_compile_flags

export MOZCONFIG=`pwd`/mozconfig
cat << EOF > $MOZCONFIG
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZ_MAKE_FLAGS="%{_smp_mflags}"
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/../obj
ac_add_options --host=%{_host}
ac_add_options --target=%{_target_platform}
ac_add_options --enable-optimize="%{optflags}"
ac_add_options --prefix="%{_prefix}"
ac_add_options --libdir="%{_libdir}"
ac_add_options --sysconfdir="%{_sysconfdir}"
ac_add_options --mandir="%{_mandir}"
ac_add_options --includedir="%{_includedir}"
ac_add_options --datadir="%{_datadir}"
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-zlib
ac_add_options --with-system-libevent
ac_add_options --with-system-libvpx
ac_add_options --with-system-ogg
ac_add_options --disable-webrtc
ac_add_options --enable-system-pixman
ac_add_options --enable-system-hunspell
ac_add_options --enable-webm
ac_add_options --enable-gio
ac_add_options --disable-gnomevfs
ac_add_options --disable-updater
ac_add_options --disable-tests
ac_add_options --disable-debug
#ac_add_options --enable-chrome-format=jar
#ac_add_options --enable-update-channel=beta
ac_add_options --enable-official-branding
ac_add_options --enable-libproxy
ac_add_options --with-system-bz2
ac_add_options --with-system-png
ac_add_options --with-system-jpeg
ac_add_options --enable-system-cairo
ac_add_options --enable-system-sqlite
ac_add_options --enable-startup-notification
ac_add_options --enable-xinerama
ac_add_options --with-distribution-id=org.rosa
ac_add_options --disable-crashreporter
ac_add_options --enable-update-channel=%{update_channel}
ac_add_options --enable-gstreamer
ac_add_options --enable-media-plugins
ac_add_options --enable-dash
%if %mdvver >= 201300
ac_add_options --enable-pulseaudio
ac_add_options --enable-profile-guided-optimization
%endif
%ifarch %arm
%if "%{_target_cpu}" != "armv7l"
ac_add_options --disable-methodjit
ac_add_options --disable-tracejit
%endif
ac_add_options --enable-system-ffi
%endif
%ifnarch %arm %mips
ac_add_options --with-valgrind
ac_add_options --with-java-include-path=%{java_home}/include
ac_add_options --with-java-bin-path=%{java_home}/bin
ac_add_options --enable-opus
%endif

EOF

perl -pi -e 's|\-0|\-9|g' config/make-jars.pl

export LDFLAGS="%ldflags"
make -f client.mk build

%install
make -C %{_builddir}/obj/browser/installer STRIP=/bin/true MOZ_PKG_FATAL_WARNINGS=0

# Copy files to buildroot
mkdir -p %{buildroot}%{mozillalibdir}
cp -rf %{_builddir}/obj/dist/firefox/* %{buildroot}%{mozillalibdir}

mkdir -p  %{buildroot}%{_bindir}
ln -sf %{mozillalibdir}/firefox %{buildroot}%{_bindir}/firefox
pushd %{buildroot}%{_bindir}
	ln -sf firefox mozilla-firefox
popd
mkdir -p %{buildroot}%{mozillalibdir}/defaults/preferences/
install -m 644 %{SOURCE9} %{buildroot}%{mozillalibdir}/defaults/preferences/kde.js

# Create and own %_libdir/mozilla/plugins & firefox extensions directories
mkdir -p %{buildroot}%{pluginsdir}
mkdir -p %{buildroot}%{_libdir}/mozilla/extensions/%{firefox_appid}
mkdir -p %{buildroot}%{_datadir}/mozilla/extensions/%{firefox_appid}

# (tpg) desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/applications/%{name}.desktop

# (tpg) icons
mkdir -p %{buildroot}/%{mozillalibdir}/icons
cp %{buildroot}%{mozillalibdir}/browser/chrome/icons/default/default16.png %{buildroot}/%{mozillalibdir}/icons/
for i in 16 22 24 32 48 256; do
# (cg) Not all icon sizes are installed with make install, so just redo it here.
install -m 644 browser/branding/official/default$i.png %{buildroot}%{mozillalibdir}/browser/chrome/icons/default/default$i.png
mkdir -p %{buildroot}%{_iconsdir}/hicolor/"$i"x"$i"/apps
ln -sf %{mozillalibdir}/chrome/icons/default/default$i.png %{buildroot}%{_iconsdir}/hicolor/"$i"x"$i"/apps/%{name}.png ;
done
mkdir -p %{buildroot}{%{_liconsdir},%{_iconsdir},%{_miconsdir}}
ln -sf %{mozillalibdir}/browser/chrome/icons/default/default48.png %{buildroot}%{_liconsdir}/%{name}.png
ln -sf %{mozillalibdir}/browser/chrome/icons/default/default32.png %{buildroot}%{_iconsdir}/%{name}.png
ln -sf %{mozillalibdir}/browser/chrome/icons/default/default16.png %{buildroot}%{_miconsdir}/%{name}.png

# exclusions
rm -f %{buildroot}%{mozillalibdir}/README.txt
rm -f %{buildroot}%{mozillalibdir}/removed-files
rm -f %{buildroot}%{mozillalibdir}/precomplete

install -D -m644 browser/app/profile/prefs.js %{buildroot}%{mozillalibdir}/defaults/profile/prefs.js
cat << EOF >> %{buildroot}%{mozillalibdir}/defaults/profile/prefs.js
user_pref("browser.EULA.override", true);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.ctrlTab.previews", true);
user_pref("browser.tabs.insertRelatedAfterCurrent", false);
user_pref("browser.startup.homepage", "file:///usr/share/doc/HTML/index.html");
#user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.backspace_action", 2);
user_pref("browser.display.use_system_colors", true);
user_pref("browser.download.folderList", 1);
user_pref("browser.link.open_external", 3);
user_pref("app.update.auto", false);
user_pref("app.update.enabled", false);
user_pref("app.update.autoInstallEnabled", false);
user_pref("security.ssl.require_safe_negotiation", false);
user_pref("dom.ipc.plugins.enabled.nswrapper*", false);
user_pref("extensions.autoDisableScopes", 0);
user_pref("extensions.shownSelectionUI", true);
user_pref("network.manage-offline-status", true);
user_pref("browser.shell.checkDefaultBrowser", false);
EOF

# display icon for Firefox button
mkdir -p %{buildroot}%{mozillalibdir}/defaults/profile/chrome
cat << EOF > %{buildroot}%{mozillalibdir}/defaults/profile/chrome/userChrome.css
#appmenu-toolbar-button {
  list-style-image: url("chrome://branding/content/icon16.png");
}
EOF

# use the system myspell dictionaries
rm -fr %{buildroot}%{mozillalibdir}/dictionaries
#ln -s %{_datadir}/hunspell %{buildroot}%{mozillalibdir}/dictionaries
ln -s %{_datadir}/dict/mozilla/ %{buildroot}%{mozillalibdir}/dictionaries

# (lm) touch and %ghost bookmarks.html to a proper uninstall
touch %{buildroot}%{mozillalibdir}/defaults/profile/bookmarks.html

# search engines
rm -f %{buildroot}%{mozillalibdir}/browser/searchplugins/*
cp -f %{SOURCE5} %{buildroot}%{mozillalibdir}/browser/searchplugins/jamendo.xml
cp -f %{SOURCE6} %{buildroot}%{mozillalibdir}/browser/searchplugins/exalead.xml
cp -f %{SOURCE8} %{buildroot}%{mozillalibdir}/browser/searchplugins/askcom.xml
cp -f %{SOURCE10} %{buildroot}%{mozillalibdir}/browser/searchplugins/yandex.xml
cp -f %{SOURCE11} %{buildroot}%{mozillalibdir}/browser/searchplugins/google.xml
cp -f %{SOURCE12} %{buildroot}%{mozillalibdir}/browser/searchplugins/bing.xml

# Correct distro values on search engines
sed -i 's/@DISTRO_VALUE@/ffx/' %{buildroot}%{mozillalibdir}/browser/searchplugins/askcom.xml
sed -i 's/@DISTRO_VALUE@//' %{buildroot}%{mozillalibdir}/browser/searchplugins/exalead.xml

mkdir -p %{buildroot}%{_sys_macros_dir}
cat <<FIN >%{buildroot}%{_sys_macros_dir}/%{name}.macros
# Macros from %{name} package
%%firefox_major              %{version}
%%firefox_epoch              %{epoch}
%%firefox_version            %{version}%{?prel:-0.%{prel}}
%%firefox_mozillapath        %{mozillalibdir}
%%firefox_pluginsdir         %{pluginsdir}
%%firefox_appid              \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
%%firefox_extdir             %%(if [ "%%_target_cpu" = "noarch" ]; then echo %%{_datadir}/mozilla/extensions/%%{firefox_appid}; else echo %%{_libdir}/mozilla/extensions/%%{firefox_appid}; fi)
FIN

%pre
if [ -d %{mozillalibdir}/dictionaries ]; then
    rm -fr %{mozillalibdir}/dictionaries
fi

%post
if [ ! -r /etc/sysconfig/oem ]; then
  case `grep META_CLASS /etc/sysconfig/system` in
    *powerpack) bookmark="mozilla-powerpack.html" ;;
    *desktop) bookmark="mozilla-one.html";;
    *) bookmark="mozilla-download.html";;
  esac
  ln -s -f ../../../../share/mdk/bookmarks/mozilla/$bookmark  %{mozillalibdir}/defaults/profile/bookmarks.html
fi

%files
%{_bindir}/%{name}
%{_bindir}/mozilla-firefox
%{_iconsdir}/hicolor/*/apps/*.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop
%{_libdir}/%{name}-%{version}*
#% ghost %{mozillalibdir}/defaults/profile/bookmarks.html
%dir %{_libdir}/mozilla
%dir %{pluginsdir}
%dir %{_libdir}/mozilla/extensions
%dir %{_libdir}/mozilla/extensions/%{firefox_appid}
%dir %{_datadir}/mozilla/extensions/%{firefox_appid}

%files devel
%{_sys_macros_dir}/%{name}.macros
