# Bloatzilla's build system _sucks_
%undefine _debugsource_packages

#
# WARNING, READ FIRST:
#
# This is a special package that needs special treatment. Due to the amount of
# security updates it needs, it's common to ship new upstream versions instead of patching.
# That means this package MUST be BUILDABLE for stable official releases.
# This also means only STABLE upstream releases, NO betas.
# This is a discussed topic. Please, do not flame it again.

# Set up Google API keys, see http://www.chromium.org/developers/how-tos/api-keys
# OpenMandriva key, id and secret
# For your own builds, please get your own set of keys.
%define google_api_key AIzaSyAraWnKIFrlXznuwvd3gI-gqTozL-H-8MU
%define google_default_client_id 1089316189405-m0ropn3qa4p1phesfvi2urs7qps1d79o.apps.googleusercontent.com
%define google_default_client_secret RDdr-pHq2gStY4uw0m-zxXeo
%define mozilla_api_key 9008bb7e-1e22-4038-94fe-047dd48ccc0b

%define firefox_appid \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
%define firefox_langdir %{_datadir}/mozilla/extensions/%{firefox_appid}
%define pluginsdir %{_libdir}/mozilla/plugins

# libxul.so is provided by libxulrunnner2.0.
%global __requires_exclude libxul.so

# The totally messed up build system insists on *.o files being ELF
# (and not LLVM bytecode)
%define _disable_lto 1

# use bundled cbindgen
# currently enabled as updating all rust deps would take eons
%global use_bundled_cbindgen  1

# Dual toolkit by default. For faster local Qt-only iteration use a single
# rpm define (abb treats a bare "gtk" argument as a project name to clone):
#   abb build --define=_without_gtk=1
#   rpmbuild -bb --without gtk …   # also fine with plain rpmbuild
# Same with --define=_without_qt=1 / --without qt for GTK-only.
%bcond_without gtk
%bcond_without qt

%if !%{with gtk} && !%{with qt}
%{error:Need at least one of --with gtk or --with qt}
%endif

# Toolkit builds install to separate trees (toolkit is compiled into libxul).
%define mozillalibdir_qt  %{_libdir}/%{name}-qt-%{version}
%define mozillalibdir_gtk %{_libdir}/%{name}-gtk-%{version}
# Default path for rpm macros / extension packaging (prefer Qt when both built).
%if %{with qt}
%define mozillalibdir %{mozillalibdir_qt}
%else
%define mozillalibdir %{mozillalibdir_gtk}
%endif

%bcond_with valgrind

# pgo seems to cause segfault on znver1
%ifarch znver1
%bcond_with pgo
%else
%bcond_without pgo
%endif

%define build_py python3

# enable use system python modules
# currently broken
%bcond_with system_python

# this seems fragile, so require the exact version or later (#58754)
%define nss_version %(pkg-config --modversion nss &>/dev/null && pkg-config --modversion nss 2>/dev/null || echo 0)
%define nspr_version %(pkg-config --modversion nspr &>/dev/null && pkg-config --modversion nspr 2>/dev/null |sed -e 's!\.0!!' || echo 0)

%define update_channel release

%define xpidir https://ftp.mozilla.org/pub/firefox/releases/%{version}%{?beta:%{beta}}/linux-x86_64/xpi/

# Supported l10n language lists
%define langlist af ar ast bg bn br bs ca cs cy da de el en_GB eo es_AR es_CL es_ES es_MX et eu fa fi fr fy ga_IE gd gl gu_IN he hi hr hu hy id is it ja kk ko km kn lt lv mk mr nb_NO nl nn_NO pa_IN pl pt_BR pt_PT ro ru si sk sl sq sr sv_SE ta te th tr uk vi zh_CN zh_TW

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
%define language_af af
%define langname_af Afrikaans
%define language_be be
%define langname_be Belarusian
%define language_bg bg
%define langname_bg Bulgarian
%define language_bn bn
%define langname_bn Bengali
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
%define language_mk mk
%define langname_mk Macedonian
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
%{expand:%(for lang in %{langlist}; do if echo " %{disabled_dict_langlist} " |grep -q " $lang "; then echo "%%define with_dict_$lang 0"; else echo "%%define with_dict_$lang 1"; fi; done)}

# Locales
%{expand:%(for lang in %{langlist}; do echo "%%global locale_$lang $(echo $lang | cut -d _ -f 1) "; done)}

#define beta b9

Summary:	Next generation web browser
Name:		firefox
# IMPORTANT: When updating, you MUST also update the l10n files by running
# download.sh after editing the version number
Version:	153.0.4
Release:	%{?beta:0.%{beta}.}1
License:	MPLv1+
Group:		Networking/WWW
Url:		https://www.mozilla.com/firefox/
Source0:	http://ftp.mozilla.org/pub/%{name}/releases/%{version}%{?beta:%{beta}}/source/%{name}-%{version}%{?beta:%{beta}}.source.tar.xz
%if 0%{?use_bundled_cbindgen}
Source2:	cbindgen-vendor.tar.xz
%endif
Source4:	%{name}.desktop
Source5:	firefox-searchengines-jamendo.xml
Source6:	firefox-searchengines-exalead.xml
Source8:	firefox-searchengines-askcom.xml
Source9:	kde.js
Source10:	firefox-searchengines-yandex.xml
Source12:	firefox-omv-default-prefs.js
Source13:	firefox-l10n-template.in
Source21:	distribution.ini
Source100:      firefox.rpmlintrc
# l10n sources
%{expand:%(\
        i=500; \
        for lang in %langlist; do\
                echo "%%{expand:Source$i: %{xpidir}%%{language_$lang}.xpi}";\
                i=$[i+1];\
        done\
        )
}

Patch15:	build-arm-libopus.patch
Patch16:	firefox-103.0-glibc-2.36.patch
Patch17:	firefox-112.0.1-no-static-libstdc++.patch

Patch51:	https://src.fedoraproject.org/rpms/firefox/raw/rawhide/f/0001-GLIBCXX-fix-for-GCC-12.patch
#Patch52:	0003-Patch-glsl-optimizer-to-build-with-glibc-2.43.patch
Patch61:	https://src.fedoraproject.org/rpms/firefox/raw/rawhide/f/mozilla-1196777.patch
Patch62:	https://src.fedoraproject.org/rpms/firefox/raw/rawhide/f/mozilla-1516803.patch
# GetSystemProxyDirect is already upstream in 153+
#Patch63:	mozilla-2040125.patch

# Restore --with-system-harfbuzz (removed upstream; always vendor otherwise).
# Disabled for now: system lib + -fvisibility=hidden produces
# "undefined hidden symbol: hb_*" at libxul link time. Revisit later.
#Patch70:	firefox-system-harfbuzz.patch

# In-tree HarfBuzz: Clang 23 promotes -Wunused-template via -Wunused error pragma
Patch71:	firefox-harfbuzz-clang-unused-template.patch

# Qt support
Patch100:	0001-Bug-2054387-Build-system-add-cairo-qt-toolkit-option.patch
Patch101:	0002-Bug-2054387-widget-qt-add-exclusive-Qt-6-widget-back.patch
Patch102:	0003-Bug-2054387-IPC-wire-Chromium-message-pump-for-Qt.-r.patch
Patch103:	0004-Bug-2054387-gfx-Qt-platform-GL-EGL-and-WebRender-int.patch
Patch104:	0005-Bug-2054387-widget-gtk-share-DMABuf-helpers-with-Qt-.patch
Patch105:	0006-Bug-2054387-a11y-add-Qt-accessibility-backend.-r-acc.patch
Patch106:	0007-Bug-2054387-browser-Qt-shell-service-and-preferences.patch
Patch107:	0008-Bug-2054387-media-enable-VAAPI-DMABuf-and-WebRTC-pat.patch
Patch108:	0009-Bug-2054387-toolkit-FreeDesktop-services-and-portals.patch
Patch109:	0010-Bug-2054387-sandbox-and-misc-Qt-support-cleanups.-r-.patch
# Wire real fontconfig/Qt font options (AA, hinting, subpixel); 0004 left stubs.
Patch110:	0011-Bug-2054387-Qt-font-options-from-fontconfig.patch
# Fractional DPR: keep stable device size so pages do not 1px-shake on reflow.
Patch111:	0012-Bug-2054387-Qt-stabilize-DPR-size-round-trip.patch
# Overlay scrollbars: avoid layout shift when ads cross overflow threshold.
Patch112:	0013-Bug-2054387-Qt-force-overlay-scrollbars.patch
# Wayland HiDPI: re-read devicePixelRatio after map; notify Gecko on scale change.
Patch113:	0014-Bug-2054387-Qt-handle-devicePixelRatio-scale-changes.patch
# Content sandbox: writable user fontconfig cache (fixes "No writable cache dirs").
Patch114:	0015-Bug-2054387-sandbox-writable-user-fontconfig-cache.patch
# Wayland activation reclaim series (shared with Thunderbird toolkit patches;
# numbering matches TB 0017–0024 — skip 0016 which is TB-only mail shell).
Patch115:	0017-Bug-2054387-Qt-keep-chrome-active-with-nofocus-popups.patch
Patch116:	0018-Bug-2054387-Qt-reclaim-activation-after-nofocus-popups.patch
Patch117:	0019-Bug-2054387-Qt-reclaim-after-dialog-idle-activation.patch
Patch118:	0020-Bug-2054387-Qt-stop-activation-reclaim-input-thrash.patch
Patch119:	0021-Bug-2054387-Qt-never-reclaim-activation-from-focus-handlers.patch
Patch120:	0022-Bug-2054387-Qt-clear-WindowTransparentForInput-on-Enable.patch
Patch121:	0023-Bug-2054387-Qt-safe-stacking-reclaim-without-focus-loops.patch
# Modal/dialog present, secondary top-level SW present, theme/tooltip paint,
# geometry deadband, mouse button state (from TB in-tree validation).
Patch122:	0024-Bug-2054387-Qt-modal-compose-theme-and-geometry-stabilization.patch

BuildRequires:	doxygen
BuildRequires:	gnutar
BuildRequires:	makedepend
BuildRequires:	make
BuildRequires:	glibc-static-devel
BuildRequires:	pkgconfig(python3)
%if %{with system_python}
BuildRequires:	python%{pyver}dist(aiohttp)
BuildRequires:	python%{pyver}dist(attrs)
BuildRequires:	python%{pyver}dist(argparse)
BuildRequires:	python%{pyver}dist(traceback2)
BuildRequires:	python%{pyver}dist(certifi)
BuildRequires:	python%{pyver}dist(cffi)
BuildRequires:	python%{pyver}dist(chardet)
BuildRequires:	python%{pyver}dist(colorama)
BuildRequires:	python%{pyver}dist(distro)
BuildRequires:	python%{pyver}dist(idna)
BuildRequires:	python%{pyver}dist(jsonschema)
BuildRequires:	python%{pyver}dist(multidict)
BuildRequires:	python%{pyver}dist(packaging)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(ply)
BuildRequires:	python%{pyver}dist(pyparsing)
BuildRequires:	python%{pyver}dist(pyrsistent)
BuildRequires:	python%{pyver}dist(requests)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(six)
BuildRequires:	python%{pyver}dist(urllib3)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	python%{pyver}dist(yarl)
BuildRequires:	python%{pyver}dist(zipp)
%endif
BuildRequires:	python%{pyver}dist(pyyaml)
BuildRequires:	rootcerts >= 1:20110830.00
BuildRequires:	unzip
BuildRequires:	wget
BuildRequires:	zip
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(libjpeg)
# Only needed if/when --with-system-harfbuzz is re-enabled (Patch70).
#BuildRequires:	pkgconfig(harfbuzz)
#BuildRequires:	pkgconfig(harfbuzz-subset)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:	pkgconfig(libspa-0.2)
BuildRequires:	pkgconfig(hunspell)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(libIDL-2.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libpng) >= 1.6.34
BuildRequires:	pkgconfig(libproxy-1.0)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(nspr) >= 4.32.0
BuildRequires:	pkgconfig(nss) >= 3.123.1
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(icu-uc) >= 78.1
BuildRequires:	pkgconfig(icu-i18n) >= 78.1
BuildRequires:	pkgconfig(libwebp) >= 1.0.2
BuildRequires:	pkgconfig(libwebpdemux) >= 1.0.2
BuildRequires:	pkgconfig(aom) >= 3.0.0
BuildRequires:	pkgconfig(dav1d) >= 1.2.1
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(theoradec)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(vpx)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(zlib)
%if %{with gtk}
BuildRequires:	pkgconfig(gtk+-3.0)
%endif
%if %{with qt}
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6DBus)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(Qt6OpenGL)
BuildRequires:	pkgconfig(Qt6PrintSupport)
# System cairo for gfxFcPlatformFontList desktop font options (tree cairo is separate).
BuildRequires:	pkgconfig(cairo)
%endif
%if !0%{?use_bundled_cbindgen}
BuildRequires:	cbindgen >= 0.29.4
%endif
BuildRequires:	nss-static-devel
BuildRequires:	clang-devel
BuildRequires:	llvm-devel
BuildRequires:	stdc++-static-devel
%ifnarch %mips
%if %{with valgrind}
BuildRequires:	valgrind
BuildRequires:	pkgconfig(valgrind)
%endif
BuildRequires:	yasm >= 1.0.1
BuildRequires:	nasm
%endif
BuildRequires:	rust >= 1.66.0
BuildRequires:	cargo >= 1.66.0
BuildRequires:	nodejs >= 12.22.12
BuildRequires:	pkgconfig(jemalloc)
%if %{with pgo}
BuildRequires:	x11-server-xvfb
%endif
Requires:	indexhtml
# fixes bug #42096
Requires:	mailcap
Requires:	xdg-utils
Suggests:	%{_lib}canberra0
Suggests:	%{_lib}cups2

Provides:	mozilla-firefox = %{EVRD}
Provides:	webclient

Obsoletes:	firefox-ext-weave-sync
Obsoletes:	firefox-beta < 11
# (tpg) needed for bookmarks
Requires(post):	distro-release-desktop
# Need at least one toolkit binary for the neutral /usr/bin/firefox wrapper.
%if %{with qt} && %{with gtk}
Requires:	(%{name}-qt = %{EVRD} or %{name}-gtk = %{EVRD})
Recommends:	(%{name}-qt = %{EVRD} if %{_lib}Qt6Widgets)
Recommends:	(%{name}-gtk = %{EVRD} if %{_lib}gtk3_0)
%elif %{with qt}
Requires:	%{name}-qt = %{EVRD}
%elif %{with gtk}
Requires:	%{name}-gtk = %{EVRD}
%endif

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

This package provides the shared launcher, desktop entry and icons. The actual
browser builds are in the firefox-qt and/or firefox-gtk subpackages. The
/usr/bin/firefox wrapper picks GTK on GNOME/MATE/Cinnamon/XFCE and Qt on other
desktops, falling back to whichever toolkit is installed.

%if %{with qt}
%package qt
Summary:	Firefox built with the Qt 6 toolkit
Group:		Networking/WWW
Requires:	%{name} = %{EVRD}
Suggests:	%{_lib}canberra0
Suggests:	%{_lib}cups2

%description qt
Firefox web browser built against the Qt 6 toolkit (cairo-qt). On Plasma and
other non-GTK desktops, /usr/bin/firefox selects this build by default.
%endif

%if %{with gtk}
%package gtk
Summary:	Firefox built with the GTK 3 toolkit
Group:		Networking/WWW
Requires:	%{name} = %{EVRD}
# (tpg) fix bug https://issues.openmandriva.org/show_bug.cgi?id=1525
Requires:	gtk3-modules
Suggests:	%{_lib}canberra0
Suggests:	%{_lib}cups2

%description gtk
Firefox web browser built against the GTK 3 toolkit (cairo-gtk3-wayland).
On GNOME, MATE, Cinnamon and XFCE, /usr/bin/firefox selects this build by
default.
%endif

%package devel
Summary:	Development files for %{name}
Group:		Development/Other
Obsoletes:	firefox-beta-devel < 11

%description devel
Files and macros mainly for building Firefox extensions.

# Expand all languages packages.
%{expand:%(\
        for lang in %langlist; do\
                echo "%%{expand:%%(sed -e "s!__LANG__!$lang!g" %{SOURCE13} 2> /dev/null)}";\
        done\
        )
}

%prep
%autosetup -p1
%if 0
# NOT YET, needs more work
# Drop the gazillion of internalized ffmpeg copies,
# we want system ffmpeg
rm -rf media/ffvpx/libav{codec,util} dom/media/platforms/ffmpeg/ffmpeg* dom/media/platforms/ffmpeg/libav*
%endif

# We trust our toolchain. More than we trust hardcodes copied from
# whatever someone found on a prehistoric brokenbuntu box.
for i in security/sandbox/chromium/sandbox/linux/system_headers/*_linux_syscalls.h; do
    echo '#include <asm/unistd.h>' >$i
done

echo -n "%google_api_key" > google-api-key
echo -n "%google_default_client_id %google_default_client_secret" > google-oauth-api-key
echo -n "%mozilla_api_key" > mozilla-api-key

export MOZCONFIG=$(pwd)/mozconfig

if [ $(getconf _NPROCESSORS_ONLN) -le 16 ]; then
    export SMP_FLAGS="%{_smp_mflags}"
else
    export SMP_FLAGS="-j 16"
fi

cat << EOF > $MOZCONFIG
ac_add_options --target="%{_target_platform}"
ac_add_options --host="%{_host}"
ac_add_options --prefix="%{_prefix}"
ac_add_options --libdir="%{_libdir}"
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
export MOZ_MAKE_FLAGS="$SMP_FLAGS"
export MOZ_SERVICES_SYNC=1
export TAR=gtar
export PYTHON3=%build_py
ac_add_options --with-mozilla-api-keyfile=$(pwd)/mozilla-api-key
ac_add_options --with-google-location-service-api-keyfile=$(pwd)/google-api-key
ac_add_options --with-google-safebrowsing-api-keyfile=$(pwd)/google-api-key
ac_add_options --enable-release
ac_add_options --update-channel=%{update_channel}
ac_add_options --enable-update-channel=%{update_channel}
ac_add_options --with-distribution-id=org.openmandriva
ac_add_options --enable-optimize="-O3"
# Distro builds use system toolchains and libraries, not mach bootstrap
# sysroots (which reject --with-system-nspr/nss among others).
ac_add_options --disable-bootstrap
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-zlib
ac_add_options --enable-necko-wifi
ac_add_options --with-system-libevent
ac_add_options --with-system-icu
ac_add_options --with-system-libvpx
ac_add_options --with-system-webp
ac_add_options --with-system-av1
ac_add_options --with-system-pipewire
ac_add_options --with-system-gbm
ac_add_options --with-system-libdrm
ac_add_options --with-system-pixman
ac_add_options --disable-updater
ac_add_options --disable-tests
ac_add_options --disable-debug
ac_add_options --disable-debug-symbols
ac_add_options --enable-official-branding
ac_add_options --enable-libproxy
ac_add_options --with-system-jpeg
ac_add_options --with-system-png
# System HarfBuzz deferred (visibility/link issues with -fvisibility=hidden).
#ac_add_options --with-system-harfbuzz
ac_add_options --enable-jemalloc
ac_add_options --enable-replace-malloc
ac_add_options --disable-crashreporter
ac_add_options --enable-pulseaudio
ac_add_options --enable-webrtc
ac_add_options --with-system-ffi
ac_add_options --with-unsigned-addon-scopes=app,system
ac_add_options --allow-addon-sideload
ac_add_options --without-wasm-sandboxed-libraries
%ifarch %{aarch64}
# doesnt seem to compile
#ac_add_options --enable-rust-simd
%endif
%ifarch %{arm}
ac_add_options --enable-skia
ac_add_options --disable-webrtc
ac_add_options --disable-elf-hack
%endif
%if %{with valgrind}
ac_add_options --with-valgrind
%endif
export LLVM_PROFDATA="llvm-profdata"
export AR="llvm-ar"
export NM="llvm-nm"
export RANLIB="llvm-ranlib"
# (tpg) use LLD if build with LLVM/clang
ac_add_options --enable-linker=lld
%if %{with pgo}
ac_add_options MOZ_PGO=1
%endif
ac_add_options --disable-lto

# We don't care about binary compatibility
# with prehistoric libstdc++ versions. No need
# to bloat things
unset MOZ_STDCXX_COMPAT
EOF

%if %{with qt}
cp -a $MOZCONFIG $MOZCONFIG-qt
echo 'mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-qt' >>$MOZCONFIG-qt
echo 'ac_add_options --enable-default-toolkit=cairo-qt' >>$MOZCONFIG-qt
%endif
%if %{with gtk}
cp -a $MOZCONFIG $MOZCONFIG-gtk
echo 'mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-gtk' >>$MOZCONFIG-gtk
echo 'ac_add_options --enable-default-toolkit=cairo-gtk3-wayland' >>$MOZCONFIG-gtk
%endif

%build
%global optflags %{optflags} -g0

%global optflags %{optflags} -Wno-error=c++11-narrowing-const-reference
%global optflags %{optflags} -Qunused-arguments -g0 -fno-lto

#(tpg) do not use serverbuild or serverbuild_hardened macros
# because compile will fail of missing -fPIC  :)
%set_build_flags

%if 0%{?use_bundled_cbindgen}
mkdir -p my_rust_vendor
cd my_rust_vendor
%{__tar} xf %{SOURCE2}
mkdir -p .cargo
cat > .cargo/config <<EOL
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "$(pwd)"
EOL

env CARGO_HOME=.cargo cargo install cbindgen
export PATH=$(pwd)/.cargo/bin:$PATH
cd -
%endif

MC=$(pwd)/mozconfig
MOZCONFIGS=""
%if %{with gtk}
MOZCONFIGS="$MOZCONFIGS $MC-gtk"
%endif
%if %{with qt}
MOZCONFIGS="$MOZCONFIGS $MC-qt"
%endif

# Append once before the dual-toolkit loop. Using LDFLAGS+= inside the loop
# concatenated flags without a separator on the second pass
# (…--no-keep-memory-Os), which breaks lld.
export LDFLAGS="${LDFLAGS:+$LDFLAGS }%{build_ldflags} -Wl,--no-keep-memory"
export RUSTFLAGS="-Cdebuginfo=0"
export MOZ_NOSPAM=1
export MOZ_SERVICES_SYNC=1
export MACH_NO_WRITE_TIMES=1

for MOZCONFIG in $MOZCONFIGS; do
	export MOZCONFIG
	# Show the config just for debugging
	cat $MOZCONFIG

	# (tpg) re-use already existing user profile
	export MOZ_ALLOW_DOWNGRADE=1

	%if %{with system_python}
		# FIXME We should enable system python, but need to sort out dependencies
		# Current status: builds locally on developer boxes, but fails inside abf
		# (tpg) use system python
		export MACH_USE_SYSTEM_PYTHON=1
		# FF seems to always sees its own in-tree stuff before system versions.
		# Remove obsolete bits and pieces that don't actually work with system
		# bits it does try to use...
		rm -rf third_party/python/{aiohttp,colorama,jsonschema,multidict,pip,pip_tools,ply,pyrsistent,setuptools,wheel,yarl,zipp}
	%endif

	%if %{with pgo}
		# pipefail: without it, "| cat -" makes the pipeline always succeed and
		# rpm proceeds to %install with a half-built tree (ABF build 629385).
		set -o pipefail
		QT_QPA_PLATFORM=xcb GDK_BACKEND=x11 xvfb-run %build_py ./mach build -v  2>&1 | cat -
	%else
		%build_py ./mach build -v
	%endif
done

%install
# Install one toolkit build into its libdir and apply shared distro customizations.
install_toolkit() {
	local toolkit="$1"
	local libdir="$2"
	local obj="obj-${toolkit}"

	# Make sure locale works for langpacks
	mkdir -p ${obj}/dist/bin/browser/defaults/preferences
	cat > ${obj}/dist/bin/browser/defaults/preferences/firefox-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF

	make -C ${obj}/browser/installer STRIP=/bin/true MOZ_PKG_FATAL_WARNINGS=0

	mkdir -p %{buildroot}${libdir}
	cp -a ${obj}/dist/firefox/* %{buildroot}${libdir}/

	mkdir -p %{buildroot}${libdir}/browser/defaults/preferences
	install -m 644 %{SOURCE9} %{buildroot}${libdir}/browser/defaults/preferences/kde.js
	install -m 644 %{SOURCE12} %{buildroot}${libdir}/browser/defaults/preferences/vendor.js

	# (cg) Not all icon sizes are installed with make install, so just redo it here.
	mkdir -p %{buildroot}${libdir}/icons
	mkdir -p %{buildroot}${libdir}/browser/chrome/icons/default
	for i in 16 22 24 32 48 256; do
		install -m 644 browser/branding/official/default$i.png \
			%{buildroot}${libdir}/browser/chrome/icons/default/default$i.png
	done
	cp %{buildroot}${libdir}/browser/chrome/icons/default/default16.png \
		%{buildroot}${libdir}/icons/

	# exclusions
	rm -f %{buildroot}${libdir}/README.txt
	rm -f %{buildroot}${libdir}/removed-files
	rm -f %{buildroot}${libdir}/precomplete

	# display icon for Firefox button
	mkdir -p %{buildroot}${libdir}/browser/defaults/profile/chrome
	cat > %{buildroot}${libdir}/browser/defaults/profile/chrome/userChrome.css << EOF
#appmenu-toolbar-button {
  list-style-image: url("chrome://branding/content/icon16.png");
}
EOF

	# use the system myspell dictionaries
	rm -fr %{buildroot}${libdir}/dictionaries
	ln -s %{_datadir}/dict/mozilla/ %{buildroot}${libdir}/dictionaries

	# (lm) touch and %ghost bookmarks.html to a proper uninstall
	mkdir -p %{buildroot}${libdir}/browser/defaults/profile
	touch %{buildroot}${libdir}/browser/defaults/profile/bookmarks.html

	# search engines
	mkdir -p %{buildroot}${libdir}/distribution/searchplugins/common
	cp -f %{SOURCE5} %{buildroot}${libdir}/distribution/searchplugins/common/jamendo.xml
	cp -f %{SOURCE6} %{buildroot}${libdir}/distribution/searchplugins/common/exalead.xml
	cp -f %{SOURCE8} %{buildroot}${libdir}/distribution/searchplugins/common/askcom.xml
	cp -f %{SOURCE10} %{buildroot}${libdir}/distribution/searchplugins/common/yandex.xml
	sed -i 's/@DISTRO_VALUE@/ffx/' %{buildroot}${libdir}/distribution/searchplugins/common/askcom.xml
	sed -i 's/@DISTRO_VALUE@//' %{buildroot}${libdir}/distribution/searchplugins/common/exalead.xml

	# Add distribution.ini
	cp %{SOURCE21} %{buildroot}${libdir}/distribution
}

%if %{with qt}
install_toolkit qt %{mozillalibdir_qt}
%endif
%if %{with gtk}
install_toolkit gtk %{mozillalibdir_gtk}
%endif

mkdir -p %{buildroot}%{_bindir}

# Toolkit-specific launchers
%if %{with qt}
cat > %{buildroot}%{_bindir}/firefox-qt << EOF
#!/bin/sh
# (tpg) do not create new user profiles on each upgrade, use existing one
export MOZ_LEGACY_PROFILES=1
exec %{mozillalibdir_qt}/firefox "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/firefox-qt
%endif

%if %{with gtk}
cat > %{buildroot}%{_bindir}/firefox-gtk << EOF
#!/bin/sh
# (tpg) do not create new user profiles on each upgrade, use existing one
export MOZ_LEGACY_PROFILES=1
if [ "\${XDG_SESSION_TYPE:-}" = wayland ]; then
	export MOZ_ENABLE_WAYLAND=1
	unset MOZ_DISABLE_WAYLAND
else
	export MOZ_DISABLE_WAYLAND=1
	unset MOZ_ENABLE_WAYLAND
fi
exec %{mozillalibdir_gtk}/firefox "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/firefox-gtk
%endif

# Neutral dispatcher: GTK on GNOME/MATE/Cinnamon/XFCE, Qt elsewhere;
# fall back to whichever toolkit is installed.
cat > %{buildroot}%{_bindir}/firefox << EOF
#!/bin/sh
# (tpg) do not create new user profiles on each upgrade, use existing one
export MOZ_LEGACY_PROFILES=1

GTK_BIN="%{mozillalibdir_gtk}/firefox"
QT_BIN="%{mozillalibdir_qt}/firefox"

prefer=qt
# XDG_CURRENT_DESKTOP is often colon-separated, e.g. ubuntu:GNOME
desktop=\$(printf '%s' "\${XDG_CURRENT_DESKTOP:-}" | tr '[:upper:]' '[:lower:]')
oifs=\$IFS
IFS=:
for d in \$desktop; do
	case "\$d" in
	gnome|gnome-classic|gnome-flashback|unity|mate|cinnamon|x-cinnamon|xfce)
		prefer=gtk
		break
		;;
	esac
done
IFS=\$oifs

# Fall back to DESKTOP_SESSION when XDG_CURRENT_DESKTOP is unset
if [ -z "\${XDG_CURRENT_DESKTOP:-}" ]; then
	case "\$(printf '%s' "\${DESKTOP_SESSION:-}" | tr '[:upper:]' '[:lower:]')" in
	gnome*|mate*|cinnamon*|xfce*)
		prefer=gtk
		;;
	esac
fi

run_gtk() {
	if [ "\${XDG_SESSION_TYPE:-}" = wayland ]; then
		export MOZ_ENABLE_WAYLAND=1
		unset MOZ_DISABLE_WAYLAND
	else
		export MOZ_DISABLE_WAYLAND=1
		unset MOZ_ENABLE_WAYLAND
	fi
	exec "\$GTK_BIN" "\$@"
}

run_qt() {
	unset MOZ_ENABLE_WAYLAND
	unset MOZ_DISABLE_WAYLAND
	exec "\$QT_BIN" "\$@"
}

if [ "\$prefer" = gtk ]; then
	if [ -x "\$GTK_BIN" ]; then
		run_gtk "\$@"
	elif [ -x "\$QT_BIN" ]; then
		run_qt "\$@"
	fi
else
	if [ -x "\$QT_BIN" ]; then
		run_qt "\$@"
	elif [ -x "\$GTK_BIN" ]; then
		run_gtk "\$@"
	fi
fi

echo "firefox: no toolkit binary found (install firefox-qt and/or firefox-gtk)" >&2
exit 1
EOF
chmod +x %{buildroot}%{_bindir}/firefox

ln -sf firefox %{buildroot}%{_bindir}/mozilla-firefox

# Create and own %_libdir/mozilla/plugins & firefox extensions directories
mkdir -p %{buildroot}%{pluginsdir}
mkdir -p %{buildroot}%{_libdir}/mozilla/extensions/%{firefox_appid}
mkdir -p %{buildroot}%{_datadir}/mozilla/extensions/%{firefox_appid}

# (tpg) desktop entry (uses neutral /usr/bin/firefox)
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE4} %{buildroot}%{_datadir}/applications/%{name}.desktop

# Icons live in the main package so either toolkit can be removed independently
mkdir -p %{buildroot}{%{_liconsdir},%{_iconsdir},%{_miconsdir}}
for i in 16 22 24 32 48 256; do
	mkdir -p %{buildroot}%{_iconsdir}/hicolor/"$i"x"$i"/apps
	install -m 644 browser/branding/official/default$i.png \
		%{buildroot}%{_iconsdir}/hicolor/"$i"x"$i"/apps/%{name}.png
done
install -m 644 browser/branding/official/default48.png %{buildroot}%{_liconsdir}/%{name}.png
install -m 644 browser/branding/official/default32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 browser/branding/official/default16.png %{buildroot}%{_miconsdir}/%{name}.png

## (crazy) why the appid? not used since 57.0 or so
## also what is the magic of that _extdir ? does not make any sense..
mkdir -p %{buildroot}%{_sys_macros_dir}
cat <<FIN >%{buildroot}%{_sys_macros_dir}/%{name}.macros
# Macros from %{name} package
%%firefox_major              %{version}
%%firefox_version            %{version}%{?beta:-0.%{beta}}
%%firefox_mozillapath        %{mozillalibdir}
%%firefox_mozillapath_qt     %{mozillalibdir_qt}
%%firefox_mozillapath_gtk    %{mozillalibdir_gtk}
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

%if %{with qt}
%pre qt
if [ -d %{mozillalibdir_qt}/dictionaries ]; then
	rm -fr %{mozillalibdir_qt}/dictionaries
fi

%post qt
if [ -e %{mozillalibdir_qt}/browser/defaults/profile ]; then
	if [ "$(readlink %{mozillalibdir_qt}/browser/defaults/profile/bookmarks.html)" != "%{_datadir}/mdk/bookmarks/mozilla/bookmarks.html" ]; then
		rm -rf %{mozillalibdir_qt}/browser/defaults/profile/bookmarks.html
		ln -s -f %{_datadir}/mdk/bookmarks/mozilla/bookmarks.html %{mozillalibdir_qt}/browser/defaults/profile/bookmarks.html
	fi
fi
%endif

%if %{with gtk}
%pre gtk
if [ -d %{mozillalibdir_gtk}/dictionaries ]; then
	rm -fr %{mozillalibdir_gtk}/dictionaries
fi

%post gtk
if [ -e %{mozillalibdir_gtk}/browser/defaults/profile ]; then
	if [ "$(readlink %{mozillalibdir_gtk}/browser/defaults/profile/bookmarks.html)" != "%{_datadir}/mdk/bookmarks/mozilla/bookmarks.html" ]; then
		rm -rf %{mozillalibdir_gtk}/browser/defaults/profile/bookmarks.html
		ln -s -f %{_datadir}/mdk/bookmarks/mozilla/bookmarks.html %{mozillalibdir_gtk}/browser/defaults/profile/bookmarks.html
	fi
fi
%endif

%files
%{_bindir}/%{name}
%{_bindir}/mozilla-firefox
%{_iconsdir}/hicolor/*/apps/*.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/%{name}.desktop
%dir %{_libdir}/mozilla
%dir %{pluginsdir}
%dir %{_libdir}/mozilla/extensions
%dir %{_libdir}/mozilla/extensions/%{firefox_appid}
%dir %{_datadir}/mozilla/extensions/%{firefox_appid}

%if %{with qt}
%files qt
%{_bindir}/firefox-qt
%{mozillalibdir_qt}/
%endif

%if %{with gtk}
%files gtk
%{_bindir}/firefox-gtk
%{mozillalibdir_gtk}/
%endif

%files devel
%{_sys_macros_dir}/%{name}.macros
