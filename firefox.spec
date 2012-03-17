%define major 11
%define realver %{major}.0

# (tpg) MOZILLA_FIVE_HOME
%define mozillalibdir %{_libdir}/%{name}-%{realver}
%define pluginsdir %{_libdir}/mozilla/plugins
%define firefox_channel release

%if %mandriva_branch == Cooker
# Cooker
%define release 1
%else
# Old distros
%define subrel 1
%define release %mkrel 0
%endif

# this seems fragile, so require the exact version or later (#58754)
%define sqlite3_version %(pkg-config --modversion sqlite3 &>/dev/null && pkg-config --modversion sqlite3 2>/dev/null || echo 0)
# this one as well (#59759)
%define nss_libname %mklibname nss 3
%define nss_version %(pkg-config --modversion nss &>/dev/null && pkg-config --modversion nss 2>/dev/null || echo 0)

Summary:	Mozilla Firefox web browser
Name:		firefox
Version:	%{realver}
Release:	%{release}
License:	MPLv1+
Group:		Networking/WWW
Url:		http://www.firefox.com/
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{realver}/source/firefox-%{realver}.source.tar.bz2
Source4:	firefox.desktop
Source5:	firefox-searchengines-jamendo.xml
Source6:	firefox-searchengines-exalead.xml
Source8:	firefox-searchengines-askcom.xml
Source9:	kde.js
Patch1:		firefox-lang.patch
Patch2:		firefox-vendor.patch
Patch3:		firefox-disable-check-default-browser.patch
# NOTE: P4 and P41 stems from suse. you can also find updated ones here:
# http://svnweb.mageia.org/packages/cauldron/firefox/current/SOURCES/
Patch4:		firefox-kde.patch
Patch41:	mozilla-kde.patch
# (OpenSuse) add patch to make firefox always use /usr/bin/firefox when "make firefox
# the default web browser" is used fix mdv bug#58784
Patch5:		firefox-3.6.3-appname.patch
Patch6:		firefox-5.0-asciidel.patch
Patch7:		firefox-10.0-no_optimizarion_override.diff
Patch8:		firefox-10.0.2-libvpx-1.0.0.diff
BuildRequires:	gtk+2-devel
Requires:	%{mklibname sqlite3_ 0} >= %{sqlite3_version}
Requires:	%{nss_libname} >= 2:%{nss_version}
BuildRequires:	autoconf2.1
BuildRequires:  nspr-devel >= 2:4.9.0
BuildRequires:  nss-devel >= 2:3.13.2
BuildRequires:  nss-static-devel >= 2:3.13.2
BuildRequires:	sqlite3-devel >= 3.7.7.1
BuildRequires:	libproxy-devel >= 0.4.4
BuildRequires:	libalsa-devel
BuildRequires:	libiw-devel
BuildRequires:	unzip
BuildRequires:	zip
#(tpg) older versions doesn't support apng extension
%if %mdkversion >= 201101
BuildRequires:	libpng-devel >= 1.4.8
%endif
BuildRequires:	makedepend
BuildRequires:	python
BuildRequires:	valgrind
BuildRequires:	rootcerts
BuildRequires:	doxygen
%if %mdkversion >= 201200
BuildRequires:	gnome-vfs2-devel
%else
BuildRequires:	libgnome-vfs2-devel
%endif
BuildRequires:	libgnome2-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	java-rpmbuild
BuildRequires:	wget
BuildRequires:	libnotify-devel
BuildRequires:	libevent-devel >= 1.4.7
BuildRequires:	libvpx-devel >= 0.9.7
%if %mdkversion >= 201100
BuildRequires:	cairo-devel >= 1.10
%endif
BuildRequires:	yasm >= 1.0.1
BuildRequires:	mesagl-devel
BuildRequires:	startup-notification-devel >= 0.8
Provides:	webclient
#Requires:	indexhtml
Requires:       xdg-utils
%if %mdkversion >= 201200
# https://qa.mandriva.com/show_bug.cgi?id=65237
Requires:       gtk2-modules
%endif
Suggests:	ff_deps myspell-en_US nspluginwrapper
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Mozilla Firefox is a web browser

%package	devel
Summary:	Development files for %{name}
Group:		Development/Other

%description	devel
Files and macros mainly for building Firefox extensions.

%prep
%setup -qn mozilla-%{firefox_channel}

# disabled for tests
%patch1 -p1 -b .lang
%patch2 -p1 -b .vendor
%patch3 -p1 -b .defaultbrowser
%patch6 -p1 -b .wintitle
%patch7 -p0 -b .no_optimizarion_override

%if %mdkversion >= 201200
%patch8 -p0 -b .libvpx-1.0.0
%endif

## KDE INTEGRATION
# copy current files and patch them later to keep them in sync
# %%patch4 -p1 -b .kde
# %%patch41 -F 1 -p1 -b .kdemoz
# install kde.js
install -m 644 %{SOURCE9} browser/app/profile/kde.js

# disabled for now, lets see!
#%patch5 -p1 -b .appname

# (tpg) remove ff bookmarks, use mdv ones
rm -rf browser/locales/en-US/profile/bookmarks.html
touch browser/locales/en-US/profile/bookmarks.html

%build
# (gmoro) please dont enable all options by hand
# we need to trust firefox defaults
export MOZCONFIG=`pwd`/mozconfig
cat << EOF > $MOZCONFIG
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
#mk_add_options MOZ_MAKE_FLAGS="%{_smp_mflags}"
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@
ac_add_options --prefix="%{_prefix}"
ac_add_options --libdir="%{_libdir}"
ac_add_options --sysconfdir="%{_sysconfdir}"
ac_add_options --mandir="%{_mandir}"
ac_add_options --includedir="%{_includedir}"
ac_add_options --datadir="%{_datadir}"
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
ac_add_options --with-system-libevent
ac_add_options --with-system-libvpx
%if %mdkversion >= 201101
ac_add_options --with-system-png
%else
ac_add_options --disable-system-png
%endif
ac_add_options --with-system-bz2
ac_add_options --enable-system-sqlite
ac_add_options --disable-installer
ac_add_options --disable-updater
ac_add_options --with-pthreads
ac_add_options --disable-tests
ac_add_options --disable-debug
ac_add_options --enable-strip
ac_add_options --enable-official-branding
ac_add_options --enable-libproxy
%if %mdkversion >= 201100
ac_add_options --enable-system-cairo
%else
ac_add_options --disable-system-cairo
%endif
ac_add_options --with-distribution-id=com.mandriva
ac_add_options --disable-crashreporter
ac_add_options --enable-optimize
ac_add_options --enable-startup-notification
ac_add_options --disable-cpp-exceptions
EOF

# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | sed -e 's/-Wall//' -e 's/-fexceptions/-fno-exceptions/g')
export CFLAGS="$MOZ_OPT_FLAGS"
export CXXFLAGS="$MOZ_OPT_FLAGS"
export PREFIX="%{_prefix}"
export LIBDIR="%{_libdir}"

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
%endif

export LDFLAGS="%{ldflags}"
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"

%install

%makeinstall_std STRIP=/bin/true

%{__mkdir_p} %{buildroot}%{_bindir}
ln -snf %{mozillalibdir}/firefox %{buildroot}%{_bindir}/firefox

# don't package two identical binaries
pushd %{buildroot}%{mozillalibdir}
    ln -snf firefox-bin firefox
popd

# Create an own %_libdir/mozilla/plugins
%{__mkdir_p} %{buildroot}%{_libdir}/mozilla/plugins

# (tpg) desktop entry
%{__mkdir_p} %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/applications/firefox.desktop

# (gmoro) icons
%{__cp} %{buildroot}%{mozillalibdir}/chrome/icons/default/default16.png %{buildroot}/%{mozillalibdir}/icons/
for i in 16 32 48 ; do
%{__mkdir_p} %{buildroot}%{_iconsdir}/hicolor/"$i"x"$i"/apps
ln -sf %{mozillalibdir}/chrome/icons/default/default$i.png %{buildroot}%{_iconsdir}/hicolor/"$i"x"$i"/apps/firefox.png ;
done

# exclusions
rm -f %{buildroot}%{mozillalibdir}/README.txt
rm -f %{buildroot}%{mozillalibdir}/removed-files
rm -f %{buildroot}%{mozillalibdir}/precomplete

install -D -m644 browser/app/profile/prefs.js %{buildroot}%{mozillalibdir}/defaults/profile/prefs.js
cat << EOF >> %{buildroot}%{mozillalibdir}/defaults/profile/prefs.js
user_pref("browser.search.selectedEngine","Ask.com");
user_pref("browser.search.order.1","Ask.com");
user_pref("browser.search.order.2","Exalead");
user_pref("browser.search.order.3","Google");
user_pref("browser.search.order.4","Yahoo");
user_pref("browser.EULA.override", true);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.ctrlTab.previews", true);
user_pref("browser.tabs.insertRelatedAfterCurrent", false);
user_pref("app.update.auto", false);
user_pref("app.update.enabled", false);
user_pref("app.update.autoInstallEnabled", false);
user_pref("security.ssl.require_safe_negotiation", false);
user_pref("browser.startup.homepage", "file:///usr/share/doc/HTML/index.html");
EOF

# files in this directory are read on every startup, and can change/add
# preferences for existing profiles
# extensions.autoDisableScopes is a new preference added in firefox 8
# it defines "scopes" where newly installed addons are disabled by default
# this is an additive bit field, and the value defaults to 15 (1+2+4+8)
# we need to remove system scope (8) from it so language packs and other addons
# which are installed systemwide won't get marked as 3rd party and disabled
# documentation: http://kb.mozillazine.org/About:config_entries#Extensions.
# or in toolkit/mozapps/extensions/AddonManager.jsm
# we also need to disable the "disable addon selection dialog"
cat << EOF > %{buildroot}%{mozillalibdir}/defaults/pref/mandriva.js
pref("app.update.auto", false);
pref("app.update.autoInstallEnabled", false);
pref("app.update.enabled", false);
pref("browser.backspace_action", 2);
pref("browser.ctrlTab.previews", true);
pref("browser.display.use_system_colors", true);
pref("browser.download.folderList", 1);
pref("browser.link.open_external", 3);
pref("browser.search.order.1","Ask.com");
pref("browser.search.order.2","Exalead");
pref("browser.search.order.3","Google");
pref("browser.search.order.4","Yahoo");
pref("browser.search.selectedEngine","Ask.com");
pref("browser.shell.checkDefaultBrowser", false);
pref("browser.tabs.insertRelatedAfterCurrent", false);
pref("dom.ipc.plugins.enabled.nswrapper*", false);
pref("extensions.autoDisableScope", 0);
pref("extensions.shownSelectionUI", true);
pref("network.manage-offline-status", true);
EOF

# search engines
cp -f %{SOURCE5} %{buildroot}%{mozillalibdir}/searchplugins/jamendo.xml
cp -f %{SOURCE6} %{buildroot}%{mozillalibdir}/searchplugins/exalead.xml
cp -f %{SOURCE8} %{buildroot}%{mozillalibdir}/searchplugins/askcom.xml

# Correct distro values on search engines
sed -i 's/@DISTRO_VALUE@/ffx/' %{buildroot}%{mozillalibdir}/searchplugins/askcom.xml
sed -i 's/@DISTRO_VALUE@//' %{buildroot}%{mozillalibdir}/searchplugins/exalead.xml

mkdir -p %{buildroot}%{_sys_macros_dir}
cat <<FIN >%{buildroot}%{_sys_macros_dir}/%{name}.macros
# Macros from %{name} package
%%firefox_major              %{major}
%%firefox_version            %{realver}
%%firefox_mozillapath        %{mozillalibdir}
%%firefox_pluginsdir         %{pluginsdir}
%%firefox_appid              \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
%%firefox_extdir             %%(if [ "%%_target_cpu" = "noarch" ]; then echo %%{_datadir}/mozilla/extensions/%%{firefox_appid}; else echo %%{_libdir}/mozilla/extensions/%%{firefox_appid}; fi)
FIN

# the %%makeinstall_std macro also installs devel files that we don't need (yet?)
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_libdir}/firefox-devel*
rm -rf %{buildroot}%{_datadir}/idl

%post
unset DISPLAY
if [ ! -r /etc/sysconfig/oem ]; then
  case `grep META_CLASS /etc/sysconfig/system` in
    *powerpack) bookmark="mozilla-powerpack.html" ;;
    *desktop) bookmark="mozilla-one.html";;
    *) bookmark="mozilla-download.html";;
  esac
  ln -s -f ../../../../share/mdk/bookmarks/mozilla/$bookmark  %{mozillalibdir}/defaults/profile/bookmarks.html
fi

%files
%{_bindir}/firefox
%{_iconsdir}/hicolor/*/apps/*.png
%{_datadir}/applications/*.desktop
%{_libdir}/%{name}-%{realver}*
%dir %{_libdir}/mozilla
%dir %{pluginsdir}

%files devel
%{_sys_macros_dir}/%{name}.macros
