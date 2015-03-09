#
# WARNING, READ FIRST:
#
# This is a special package that needs special treatment. Due to the amount of
# security updates it needs, it's common to ship new upstream versions instead of patching.
# That means this package MUST be BUILDABLE for stable official releases.
# This also means only STABLE upstream releases, NO betas.
# This is a discussed topic. Please, do not flame it again.

%define firefox_appid \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
%define firefox_langdir %{_datadir}/mozilla/extensions/%{firefox_appid}
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

%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define xpidir ftp://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/linux-i686/xpi/

# Supported l10n language lists
%define langlist af ar as ast be bg bn_IN bn_BD br bs ca cs cy da de el en_GB en_ZA eo es_AR es_CL es_ES es_MX et eu fa fi fr fy ga_IE gd gl gu_IN he hi hr hu hy id is it ja kk ko km kn lt lv mai mk ml mr nb_NO nl nn_NO or pa_IN pl pt_BR pt_PT ro ru si sk sl sq sr sv_SE ta te th tr uk vi zh_CN zh_TW

# Disabled l10n languages, for any reason
# - no locales-XX package:
# uu ak rm son

# Disabled hunspell dicts, for any reason (e.g. because there is no dictionary for the language)
%define disabled_dict_langlist as ast be bs bn_BD bn_IN br es_AR es_CL fi gu_IN ja kk kn ko lg mai mk ml pa_IN ta_LK si sq sr te tr zh_CN zh_TW

# Language descriptions
%define language_ak ak
%define langname_ak Akan
%define language_ar ar
%define langname_ar Arabic
%define language_ast ast
%define langname_ast Asturian
%define language_as as
%define langname_as Assamese
%define language_af af
%define langname_af Afrikaans
%define language_be be
%define langname_be Belarusian
%define language_bg bg
%define langname_bg Bulgarian
%define language_bn_BD bn-BD
%define langname_bn_BD Bengali
%define language_bn_IN bn-IN
%define langname_bn_IN Bengali
%define language_br br
%define langname_br Breton
%define language_bs bs
%define langname_bs Bosnian
%define language_ca ca
%define langname_ca Catalan
%define language_cs cs
%define langname_cs Czech
%define language_cy cy
%define langname_cy Welsh
%define language_da da
%define langname_da Dansk
%define language_de de
%define langname_de German
%define language_el el
%define langname_el Greek
%define language_en_GB en-GB
%define langname_en_GB British English
%define language_en_ZA en-ZA
%define langname_en_ZA English (South Africa)
%define language_eo eo
%define langname_eo Esperanto
%define language_es_AR es-AR
%define langname_es_AR Spanish (Argentina)
%define language_es_CL es-CL
%define langname_es_CL Spanish (Chile)
%define language_es_ES es-ES
%define langname_es_ES Spanish
%define language_es_MX es-MX
%define langname_es_MX Spanish (Mexico)
%define language_et et
%define langname_et Estonian
%define language_eu eu
%define langname_eu Basque
%define language_fa fa
%define langname_fa Farsi
%define language_fi fi
%define langname_fi Finnish
%define language_fr fr
%define langname_fr French
%define language_fy fy-NL
%define langname_fy Frisian
%define language_ga_IE ga-IE
%define langname_ga_IE Irish
%define language_gd gd
%define langname_gd Scottish Gaelic
%define language_gl gl
%define langname_gl Galician
%define language_gu_IN gu-IN
%define langname_gu_IN Gujarati
%define language_he he
%define langname_he Hebrew
%define language_hi hi-IN
%define langname_hi Hindi
%define language_hr hr
%define langname_hr Croatian
%define language_hu hu
%define langname_hu Hungarian
%define language_hy hy-AM
%define langname_hy Armenian
%define language_id id
%define langname_id Indonesian
%define language_is is
%define langname_is Icelandic
%define language_it it
%define langname_it Italian
%define language_ja ja
%define langname_ja Japanese
%define language_kk kk
%define langname_kk Kazakh
%define language_ko ko
%define langname_ko Korean
%define language_km km
%define langname_km Khmer
%define language_kn kn
%define langname_kn Kannada
%define language_ku ku
%define langname_ku Kurdish
%define language_lg lg
%define langname_lg Ganda
%define language_lt lt
%define langname_lt Lithuanian
%define language_lv lv
%define langname_lv Latvian
%define language_mai mai
%define langname_mai Maithili
%define language_mk mk
%define langname_mk Macedonian
%define language_ml ml
%define langname_ml Malayalam
%define language_mr mr
%define langname_mr Marathi
%define language_nb_NO nb-NO
%define langname_nb_NO Norwegian Bokmaal
%define language_nn_NO nn-NO
%define langname_nn_NO Norwegian Nynorsk
%define language_nl nl
%define langname_nl Dutch
%define language_nso nso
%define langname_nso Northern Sotho
%define language_or or
%define langname_or Oriya
%define language_pa_IN pa-IN
%define langname_pa_IN Punjabi (gurmukhi)
%define language_pl pl
%define langname_pl Polish
%define language_pt_BR pt-BR
%define langname_pt_BR Brazilian portuguese
%define language_pt_PT pt-PT
%define langname_pt_PT Portuguese
%define language_rm rm
%define langname_rm Rumantsch
%define language_ro ro
%define langname_ro Romanian
%define language_ru ru
%define langname_ru Russian
%define language_si si
%define langname_si Sinhala
%define language_sk sk
%define langname_sk Slovak
%define language_sl sl
%define langname_sl Slovenian
%define language_son son
%define langname_son So?ay
%define language_sq sq
%define langname_sq Shqipe
%define language_sr sr
%define langname_sr Serbian
%define language_sv_SE sv-SE
%define langname_sv_SE Swedish
%define language_ta ta
%define langname_ta Tamil
%define language_ta_LK ta-LK
%define langname_ta_LK Tamil (Sri Lanka)
%define language_te te
%define langname_te Telugu
%define language_th th
%define langname_th Thai
%define language_tr tr
%define langname_tr Turkish
%define language_uk uk
%define langname_uk Ukrainian
%define language_uk_UA uk-UA
%define langname_uk_UA Ukrainian
%define language_vi vi
%define langname_vi Vietnamese
%define language_zh_CN zh-CN
%define langname_zh_CN Simplified Chinese
%define language_zh_TW zh-TW
%define langname_zh_TW Traditional Chinese
%define language_zu zu
%define langname_zu Zulu

# Defaults (all languages enabled by default)
# dicts
%{expand:%(for lang in %{langlist}; do echo "%%define with_dict_$lang 1"; done)}
%{expand:%(for lang in %{disabled_dict_langlist}; do echo "%%define with_dict_$lang 0"; done)}

# Locales
%{expand:%(for lang in %{langlist}; do echo "%%define locale_$lang `echo $lang | cut -d _ -f 1` "; done)}


Summary:	Next generation web browser
Name:		firefox
Epoch:		0
# IMPORTANT: When updating, you MUST also update the firefox-l10n package
# because its subpackages depend on the exact version of Firefox it was
# built for.
Version:	36.0.1
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
Source13:	firefox-l10n-template.in
Source100:      firefox.rpmlintrc
# l10n sources
%{expand:%(\
        i=500; \
        for lang in %langlist; do\
                echo "%%{expand:Source$i: %{xpidir}/%%{language_$lang}.xpi}";\
                i=$[i+1];\
        done\
        )
}
Patch1:		firefox-6.0-lang.patch
Patch2:		firefox-vendor.patch
# (OpenSuse) add patch to make firefox always use /usr/bin/firefox when "make firefox
# the default web browser" is used fix mdv bug#58784
Patch5:		firefox-6.0-appname.patch
Patch10:	firefox-3.5.3-default-mail-handler.patch
# Patches for kde integration of FF 
Patch11:	firefox-36.0-kde.patch
Patch12:	mozilla-36.0-kde.patch
# (crisb) fix for two component (3.16) NSS version
Patch40:	firefox-28.0-nss_detect.patch
# (crisb) java does not actually seem to be required except for android builds
Patch41:	firefox-30.0-no_java.patch

#BuildConflicts:	libreoffice-core
BuildRequires:	doxygen
BuildRequires:	makedepend
BuildRequires:	pkgconfig(python2)
%if %mdvver >= 201500
BuildRequires:	python2
BuildRequires:	python2-distribute
%else
BuildRequires:  python
BuildRequires:  python-distribute
%endif
#(tpg) this is in contrib
#BuildRequires:	python-ply
BuildRequires:	rootcerts >= 1:20110830.00
BuildRequires:	unzip
BuildRequires:	wget
BuildRequires:	zip
BuildRequires:	bzip2-devel
BuildRequires:	jpeg-devel
BuildRequires:	libiw-devel
BuildRequires:	icu-devel
BuildRequires:	pkgconfig(harfbuzz)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(cairo) >= 1.10
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gl)
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

# Expand all languages packages.
%{expand:%(\
        for lang in %langlist; do\
                echo "%%{expand:%%(sed "s!__LANG__!$lang!g" %{_sourcedir}/%{name}-template.in 2> /dev/null)}";\
        done\
        )
}

%prep
%setup -qc %{name}-%{version} 
pushd mozilla-%update_channel
%patch1 -p1 -b .lang
#patch2 -p1 -b .vendor
%patch5 -p1 -b .appname
%patch10 -p1 -b .default-mail-handler

## KDE INTEGRATION
%patch11 -p1 -b .kdepatch
%patch12 -p1 -b .kdemoz

%patch40 -p1 
%patch41 -p0

#pushd js/src
#autoconf-2.13
#popd
#autoconf-2.13

# needed to regenerate certdata.c
pushd security/nss/lib/ckfw/builtins
perl ./certdata.perl < /etc/pki/tls/mozilla/certdata.txt
popd

%build
%global optflags %{optflags} -g0

pushd mozilla-%update_channel

# (crisb) use gcc for now
export CXX=g++
export CC=gcc

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
ac_add_options --prefix="%{_prefix}"
ac_add_options --libdir="%{_libdir}"
ac_add_options --sysconfdir="%{_sysconfdir}"
ac_add_options --mandir="%{_mandir}"
ac_add_options --includedir="%{_includedir}"
ac_add_options --datadir="%{_datadir}"
%ifarch %{ix86}
ac_add_options --disable-optimize
%else
ac_add_options --enable-optimize
%endif
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-zlib
ac_add_options --with-system-libevent
ac_add_options --with-system-icu
ac_add_options --with-system-libvpx
ac_add_options --with-system-ogg
ac_add_options --with-system-harfbuzz
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
ac_add_options --with-system-jpeg
%if %mdvver >= 201500
ac_add_options --with-system-png
ac_add_options --enable-system-sqlite
%endif
ac_add_options --disable-system-cairo
ac_add_options --enable-startup-notification
ac_add_options --enable-xinerama
#ac_add_options --with-system-ply
ac_add_options --with-distribution-id=org.openmandriva
ac_add_options --disable-crashreporter
ac_add_options --enable-update-channel=%{update_channel}
ac_add_options --enable-gstreamer=1.0
ac_add_options --enable-media-plugins
ac_add_options --enable-dash
%if %mdvver >= 201300
ac_add_options --enable-pulseaudio
ac_add_options --enable-webrtc
ac_add_options --enable-system-ffi
%endif
%ifarch %arm
%if "%{_target_cpu}" != "armv7l"
ac_add_options --disable-methodjit
ac_add_options --disable-tracejit
%endif
ac_add_options --enable-skia
ac_add_options --disable-webrtc
%endif
%ifnarch %arm %mips
ac_add_options --with-valgrind
ac_add_options --enable-opus
%endif

EOF

# Show the config just for debugging
cat $MOZCONFIG


export LDFLAGS="%ldflags"
export PYTHON=python2
make -f client.mk build

%install

pushd mozilla-%update_channel

make -C %{_builddir}/%{name}-%{version}/obj/browser/installer STRIP=/bin/true MOZ_PKG_FATAL_WARNINGS=0

# Copy files to buildroot
mkdir -p %{buildroot}%{mozillalibdir}
cp -rf %{_builddir}/%{name}-%{version}/obj/dist/firefox/* %{buildroot}%{mozillalibdir}

mkdir -p  %{buildroot}%{_bindir}
ln -sf %{mozillalibdir}/firefox %{buildroot}%{_bindir}/firefox
pushd %{buildroot}%{_bindir}
	ln -sf firefox mozilla-firefox
popd
mkdir -p %{buildroot}%{mozillalibdir}/browser/defaults/preferences/
install -m 644 %{SOURCE9} %{buildroot}%{mozillalibdir}/browser/defaults/preferences/kde.js

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
ln -sf %{mozillalibdir}/browser/chrome/icons/default/default$i.png %{buildroot}%{_iconsdir}/hicolor/"$i"x"$i"/apps/%{name}.png ;
done
mkdir -p %{buildroot}{%{_liconsdir},%{_iconsdir},%{_miconsdir}}
ln -sf %{mozillalibdir}/browser/chrome/icons/default/default48.png %{buildroot}%{_liconsdir}/%{name}.png
ln -sf %{mozillalibdir}/browser/chrome/icons/default/default32.png %{buildroot}%{_iconsdir}/%{name}.png
ln -sf %{mozillalibdir}/browser/chrome/icons/default/default16.png %{buildroot}%{_miconsdir}/%{name}.png

# exclusions
rm -f %{buildroot}%{mozillalibdir}/README.txt
rm -f %{buildroot}%{mozillalibdir}/removed-files
rm -f %{buildroot}%{mozillalibdir}/precomplete

install -D -m644 browser/app/profile/prefs.js %{buildroot}%{mozillalibdir}/browser/defaults/profile/prefs.js
cat << EOF >> %{buildroot}%{mozillalibdir}/browser/defaults/profile/prefs.js
user_pref("browser.EULA.override", true);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.ctrlTab.previews", true);
user_pref("browser.tabs.insertRelatedAfterCurrent", true);
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
user_pref("media.gstreamer.enabled", true);
user_pref("media.webaudio.enabled", true);
EOF

# display icon for Firefox button
mkdir -p %{buildroot}%{mozillalibdir}/browser/defaults/profile/chrome
cat << EOF > %{buildroot}%{mozillalibdir}/browser/defaults/profile/chrome/userChrome.css
#appmenu-toolbar-button {
  list-style-image: url("chrome://branding/content/icon16.png");
}
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
cat << EOF > %{buildroot}%{mozillalibdir}/browser/defaults/preferences/mga.js
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
pref("extensions.autoDisableScopes", 0);
pref("extensions.shownSelectionUI", true);
EOF

# use the system myspell dictionaries
rm -fr %{buildroot}%{mozillalibdir}/dictionaries
#ln -s %{_datadir}/hunspell %{buildroot}%{mozillalibdir}/dictionaries
ln -s %{_datadir}/dict/mozilla/ %{buildroot}%{mozillalibdir}/dictionaries

# (lm) touch and %ghost bookmarks.html to a proper uninstall
touch %{buildroot}%{mozillalibdir}/browser/defaults/profile/bookmarks.html

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

# Convert rpm macros to bash variables
%{expand:%(for lang in %{langlist}; do echo "language_$lang=%%{language_$lang}"; done)}

mkdir -p %{buildroot}%{firefox_langdir}/

# Install all languages
for lang in %{langlist}; do
        language="language_$lang"
        language=${!language}

        # l10n
        cp %{_sourcedir}/${language}.xpi %{buildroot}%{firefox_langdir}/langpack-${language}@firefox.mozilla.org.xpi

done

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
  ln -s -f ../../../../share/mdk/bookmarks/mozilla/$bookmark  %{mozillalibdir}/browser/defaults/profile/bookmarks.html
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
#% ghost %{mozillalibdir}/browser/defaults/profile/bookmarks.html
%dir %{_libdir}/mozilla
%dir %{pluginsdir}
%dir %{_libdir}/mozilla/extensions
%dir %{_libdir}/mozilla/extensions/%{firefox_appid}
%dir %{_datadir}/mozilla/extensions/%{firefox_appid}

%files devel
%{_sys_macros_dir}/%{name}.macros
