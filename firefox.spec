#
# WARNING, READ FIRST:
#
# This is a special package that needs special treatment. Due to the amount of
# security updates it needs, it's common to ship new upstream versions instead of patching.
# That means this package MUST be BUILDABLE for stable official releases.
# This also means only STABLE upstream releases, NO betas.
# This is a discussed topic. Please, do not flame it again.

%define major 3
%define ff_epoch 0
# (tpg) set version HERE !!!
%define realver %{major}.6.2
%define xulrunner_version 1.9.2.2
# (tpg) MOZILLA_FIVE_HOME
%define mozillalibdir %{_libdir}/%{name}-%{realver}
%define pluginsdir %{_libdir}/mozilla/plugins

# libxul.so is provided by libxulrunnner1.9.
%define _requires_exceptions libxul.so

%if %mdkversion >= 200900
%define _use_syshunspell 1
%else
%define _use_syshunspell 0
%endif

%if %mandriva_branch == Cooker
# Cooker
%define release %mkrel 1
%else
# Old distros
%define subrel 1
%define release %mkrel 0
%endif

Summary:	Next generation web browser
Name:		firefox
Version:	%{realver}
Epoch:		%{ff_epoch}
Release:	%{release}
License:	MPLv1+
Group:		Networking/WWW
Url:		http://www.mozilla.org/
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/%{name}/releases/%{realver}/source/%{name}-%{realver}.source.tar.bz2
Source1:	%{SOURCE0}.asc
Source4:	%{name}.desktop
Source5:	firefox-searchengines-jamendo.xml
Source6:	firefox-searchengines-exalead.xml
Source7:	firefox-rebuild-databases.pl.in.generatechrome
Source8:	firefox-searchengines-askcom.xml
Source9:    kde.js
Patch1:		mozilla-firefox-3.0.5-lang.patch
Patch2:		mozilla-firefox-3.0.5-vendor.patch
Patch3:		mozilla-firefox-1.5.0.6-systemproxy.patch
Patch4:		firefox-3.0b3-homepage.patch
Patch5:		firefox-3.0b3-check-default-browser.patch
Patch6:		mozilla-firefox-run-mozilla.patch
Patch14:	mozilla-firefox-1.5-software-update.patch
#Patch15:	firefox-3.0.1-disable-classic-theme.patch
Patch16:	firefox-3.5.3-default-mail-handler.patch
Patch17:    firefox-kde.patch
BuildRequires:	gtk+2-devel
BuildRequires:	libx11-devel
BuildRequires:	unzip
BuildRequires:	zip
#(tpg) older versions doesn't support apng extension
BuildRequires:	libpng-devel >= 1.2.25-2
BuildRequires:	libjpeg-devel
BuildRequires:	zlib-devel
BuildRequires:	libcairo-devel
BuildRequires:	glib2-devel
BuildRequires:	libIDL2-devel
BuildRequires:	makedepend
BuildRequires:	nss-devel >= 2:3.12.4
BuildRequires:	nspr-devel >= 2:4.8
BuildRequires:	startup-notification-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	python-devel
# (fhimpe) Starting from Firefox 3.0.1, at least sqlite 3.5.9 is needed
# so only use system sqlite on Mandriva >= 2009.0
# (eugeni) Starting from Firefox 3.0.11, at least sqlite 3.6.7 is required
%if %mdkversion >= 200900
BuildRequires:	libsqlite3-devel >= 3.6.7
%endif
BuildRequires:	valgrind
BuildRequires:	rootcerts
BuildRequires:	libxt-devel
%if %_use_syshunspell
BuildRequires:	hunspell-devel
%endif
BuildRequires:	doxygen
BuildRequires:	libgnome-vfs2-devel
BuildRequires:	libgnome2-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	java-rpmbuild
BuildRequires:  xulrunner-devel >= %xulrunner_version
BuildRequires:	wget
BuildRequires:	libnotify-devel
Provides:	webclient
Requires:	indexhtml
Requires:       xdg-utils
Suggests:	myspell-en_US
Requires(post):	desktop-file-utils
Requires(postun):	desktop-file-utils
# fixes bug #42096
Requires:	mailcap
# ff3 now provides /usr/bin/firefox and mozilla-firefox
Conflicts:	mozilla-firefox < 2.0.0.16-2
Obsoletes:	mozilla-firefox-gnome-support
Obsoletes:	mozilla-firefox < 3.0
Provides:	mozilla-firefox = %{epoch}:%{version}-%{release}
Obsoletes:	mozilla-firefox-theme-gnome
Obsoletes:	mozilla-firefox-theme-kdeff <= 0.4
# since 3.0.1-2 we do not have ff libification anymore
Obsoletes:	%{mklibname firefox 3} < 3.0.1-2
# (salem) while we dont have a better solution, we need to obsolete them all
Obsoletes:	%mklibname mozilla-firefox 2.0.0.1
Obsoletes:	%mklibname mozilla-firefox 2.0.0.3
Obsoletes:	%mklibname mozilla-firefox 2.0.0.4
Obsoletes:	%mklibname mozilla-firefox 2.0.0.6
Obsoletes:	%mklibname mozilla-firefox 2.0.0.8
Obsoletes:	%mklibname mozilla-firefox 2.0.0.11
Obsoletes:	%mklibname mozilla-firefox 2.0.0.12
Obsoletes:	%mklibname mozilla-firefox 2.0.0.13
Obsoletes:	%mklibname mozilla-firefox 2.0.0.14
Obsoletes:	%mklibname mozilla-firefox 2.0.0.15
Obsoletes:	%mklibname mozilla-firefox 2.0.0.16
Obsoletes:	%mklibname mozilla-firefox 2.0.0.17
Obsoletes:	%mklibname mozilla-firefox 2.0.0.18
Obsoletes:	%mklibname mozilla-firefox 2.0.0.19
Requires:	xulrunner >= %{xulrunner_version}
Requires:	%{mklibname xulrunner %xulrunner_version}
Suggests:	nspluginwrapper
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The award-winning Web browser is now faster, more secure, and fully customizable 
to your online life. With Firefox(R) 3, we've added powerful new features that 
make your online experience even better. It is an 'open source' product which is 
freely available, and is acquiring a growing proportion of international web 
browser usage.

Firefox claims to offer a more secure web browsing experience than other products, 
with better protection against spyware and other Internet-based security threats. 
It includes all the standard features of a modern web browser, like Internet 
searching, tracking recently visited sites, setting up shortcuts to favourite 
sites, customising the software behaviour and so on. Firefox also includes 
features like 'tabbed browsing' (opening several web sites as sections within the 
same window) and methods for controlling pop-up windows, cookies and downloaded 
files.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Other

%description	devel
Files and macros mainly for building Firefox extensions.

%prep
%setup -qn mozilla-1.9.2
#%patch1 -p1 -b .lang rediff
%patch2 -p1 -b .vendor
# Temporary disabled. It prevents firefox from running. 
#%patch3 -p1
#%patch4 -p1 -b .homepage
#%patch5 -p1 -b .defaultbrowser
# It was disabled because firefox3 hangs when using soundwrapper
#%patch6 -p1
#%patch14 -p1 -b .disable-software-update rediff
# (salem)	this patch does not work properly on ff3.
#%patch15 -p1 -b .disable-classic-theme
%patch16 -p1 -b .default-mail-handler
## KDE INTEGRATION
# copy current files and patch them later to keep them in sync
%patch17 -p1
# install kde.js
install -m 644 %{SOURCE9} browser/app/profile/kde.js
# (tpg) remove ff bookmarks, to use mdv ones
rm -rf browser/locales/en-US/profile/bookmarks.html
touch browser/locales/en-US/profile/bookmarks.html

# needed to regenerate certdata.c
pushd security/nss/lib/ckfw/builtins
perl ./certdata.perl < /etc/pki/tls/mozilla/certdata.txt
popd

%build
%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed 1
%if %mdkversion >= 200900
%setup_compile_flags
%else
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ;
%endif
%serverbuild
export PREFIX="%{_prefix}"
export LIBDIR="%{_libdir}"
export MOZILLA_OFFICIAL=1
export BUILD_OFFICIAL=1

# (tpg) don't use macro here
# (fhimpe) javaxpcom does not build correctly with xulrunner (is it
# actually needed/useful here when enabled already in xulrunner?)
# https://bugzilla.mozilla.org/show_bug.cgi?id=448386
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--includedir=%{_includedir} \
	--datadir=%{_datadir} \
	--enable-application=browser \
	--with-pthreads \
	--with-system-jpeg \
	--with-system-zlib \
	--with-system-bz2 \
	--with-system-png \
	--with-system-nspr \
	--with-system-nss \
	--disable-ldap \
	--disable-calendar \
	--disable-mailnews \
	--disable-chatzilla \
	--disable-composer \
	--disable-profilesharing \
	--disable-toolkit-qt \
	--disable-installer \
	--disable-updater \
	--disable-debug \
	--disable-pedantic \
	--disable-native-uconv \
	--disable-elf-dynstr-gc \
	--disable-crashreporter \
	--disable-strip \
	--enable-crypto \
	--enable-gnomevfs \
	--enable-gnomeui \
	--enable-places \
	--enable-storage \
	--enable-default-toolkit=cairo-gtk2 \
	--enable-official-branding \
	--enable-svg \
	--enable-svg-renderer=cairo \
	--enable-single-profile \
	--enable-startup-notification \
	--enable-system-cairo \
	--enable-reorder \
	--enable-optimize \
	--enable-safe-browsing \
	--enable-xinerama \
	--enable-canvas \
	--enable-pango \
	--enable-xft \
	--enable-image-encoder=all \
	--enable-image-decoders=all \
	--enable-extensions=default \
%if %_use_syshunspell
	--enable-system-hunspell \
%endif
	--enable-install-strip \
	--enable-url-classifier \
	--disable-faststart \
	--enable-smil \
	--disable-tree-freetype \
	--disable-canvas3d \
	--disable-coretext \
	--enable-necko-protocols=all \
	--disable-necko-wifi \
	--disable-tests \
	--disable-mochitest \
	--with-distribution-id=com.mandriva \
	--with-valgrind \
	--enable-jemalloc \
%if %mdkversion >= 200900
	--enable-system-sqlite \
%else
	--disable-system-sqlite \
%endif
	--with-system-libxul \
        --with-libxul-sdk=`pkg-config --variable=sdkdir libxul` \
	--with-java-include-path=%{java_home}/include \
	--with-java-bin-path=%{java_home}/bin \
	--with-default-mozilla-five-home="%{mozillalibdir}"

%__perl -p -i -e 's|\-0|\-9|g' config/make-jars.pl

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

ln -s firefox %{buildroot}%{_bindir}/mozilla-firefox
sed -i "s,@LIBDIR@,%{_libdir}," %{buildroot}%{mozillalibdir}/%{name}

# Create an own %_libdir/mozilla/plugins
%{__mkdir_p} %{buildroot}%{_libdir}/mozilla/plugins

# (tpg) desktop entry
%{__mkdir_p} %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/applications/%{name}.desktop

# (tpg) icons
%{__cp} other-licenses/branding/%{name}/default16.png %{buildroot}/%{mozillalibdir}/icons/
for i in 16 22 24 32 48 256; do
%{__mkdir_p} %{buildroot}%{_iconsdir}/hicolor/"$i"x"$i"/apps
%{__cp} other-licenses/branding/%{name}/default$i.png %{buildroot}%{_iconsdir}/hicolor/"$i"x"$i"/apps/firefox.png ;
done

cat << EOF >> %{buildroot}%{mozillalibdir}/defaults/profile/prefs.js
user_pref("browser.search.selectedEngine","Ask.com");
user_pref("browser.search.order.1","Ask.com");
user_pref("browser.search.order.2","Exalead");
user_pref("browser.search.order.3","Google");
user_pref("browser.search.order.4","Yahoo");
user_pref("browser.EULA.override", true);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.startup.homepage", "file:///usr/share/doc/HTML/index.html");
user_pref("browser.ctrlTab.previews", true);
user_pref("browser.tabs.insertRelatedAfterCurrent", false);
user_pref("app.update.auto", false);
user_pref("app.update.enabled", false);
user_pref("app.update.autoInstallEnabled", false);
EOF

# search engines
cp -f %{SOURCE5} %{buildroot}%{mozillalibdir}/searchplugins/jamendo.xml
cp -f %{SOURCE6} %{buildroot}%{mozillalibdir}/searchplugins/exalead.xml
cp -f %{SOURCE8} %{buildroot}%{mozillalibdir}/searchplugins/askcom.xml

%if %mdkversion == 200900
sed -i 's/@DISTRO_VALUE@/101490/' %{buildroot}%{mozillalibdir}/searchplugins/askcom.xml
sed -i 's/@DISTRO_VALUE@/MDV20090/' %{buildroot}%{mozillalibdir}/searchplugins/exalead.xml
%else
%if %mdkversion == 200810
sed -i 's/@DISTRO_VALUE@/1681/' %{buildroot}%{mozillalibdir}/searchplugins/askcom.xml
sed -i 's/@DISTRO_VALUE@/MDV20081/' %{buildroot}%{mozillalibdir}/searchplugins/exalead.xml
%else
%if %mdkversion == 200800
sed -i 's/@DISTRO_VALUE@/1680/' %{buildroot}%{mozillalibdir}/searchplugins/askcom.xml
sed -i 's/@DISTRO_VALUE@/MDV20080/' %{buildroot}%{mozillalibdir}/searchplugins/exalead.xml
%else
%if %mdkversion == 200710
sed -i 's/@DISTRO_VALUE@/1655/' %{buildroot}%{mozillalibdir}/searchplugins/askcom.xml
sed -i 's/@DISTRO_VALUE@/MDV20071/' %{buildroot}%{mozillalibdir}/searchplugins/exalead.xml
%else
%if %mdkversion == 200700
sed -i 's/@DISTRO_VALUE@/101489/' %{buildroot}%{mozillalibdir}/searchplugins/askcom.xml
sed -i 's/@DISTRO_VALUE@/MDV20070/' %{buildroot}%{mozillalibdir}/searchplugins/exalead.xml
%else
%if %mdkversion == 300
sed -i 's/@DISTRO_VALUE@/101471/' %{buildroot}%{mozillalibdir}/searchplugins/askcom.xml
sed -i 's/@DISTRO_VALUE@/MDVCorp/' %{buildroot}%{mozillalibdir}/searchplugins/exalead.xml
%else
# default
sed -i 's/@DISTRO_VALUE@/ffx/' %{buildroot}%{mozillalibdir}/searchplugins/askcom.xml
sed -i 's/@DISTRO_VALUE@//' %{buildroot}%{mozillalibdir}/searchplugins/exalead.xml
%endif #corp
%endif #200700
%endif #200710
%endif #200800
%endif #200810
%endif #200900

#ghost files
touch %{buildroot}%{mozillalibdir}/components/compreg.dat
touch %{buildroot}%{mozillalibdir}/components/xpti.dat

# firefox update tool
cat %{SOURCE7} |\
    sed -e "s|FIREFOX_VERSION|%{realver}|g;s|LIBDIR|%{_libdir}|g"\
    > %{buildroot}%{mozillalibdir}/firefox-rebuild-databases.pl
chmod 755 %{buildroot}%{mozillalibdir}/firefox-rebuild-databases.pl

%find_lang %{name}

mkdir -p %{buildroot}%{_sys_macros_dir}
cat <<FIN >%{buildroot}%{_sys_macros_dir}/%{name}.macros
# Macros from %{name} package
%%firefox_major              %{major}
%%firefox_epoch              %{ff_epoch}
%%firefox_version            %{realver}
%%firefox_mozillapath        %{mozillalibdir}
%%firefox_xulrunner_version  %{xulrunner_version}
%%firefox_pluginsdir         %{pluginsdir}
FIN

%post
%if %mdkversion < 200900
%{update_menus}
%{update_desktop_database}
%endif
unset DISPLAY
%{mozillalibdir}/firefox-rebuild-databases.pl
if [ ! -r /etc/sysconfig/oem ]; then
  case `grep META_CLASS /etc/sysconfig/system` in
    *powerpack) bookmark="mozilla-powerpack.html" ;;
    *desktop) bookmark="mozilla-one.html";;
    *) bookmark="mozilla-download.html";;
  esac
  ln -s -f ../../../../share/mdk/bookmarks/mozilla/$bookmark  %{mozillalibdir}/defaults/profile/bookmarks.html
fi

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_desktop_database}
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/mozilla-firefox
%{_iconsdir}/hicolor/*/apps/*.png
%ghost %{mozillalibdir}/components/compreg.dat
%ghost %{mozillalibdir}/components/xpti.dat
%{_datadir}/applications/*.desktop
%{_libdir}/%{name}-%{realver}*
%dir %{_libdir}/mozilla
%dir %{pluginsdir}

%files devel
%{_sys_macros_dir}/%{name}.macros
