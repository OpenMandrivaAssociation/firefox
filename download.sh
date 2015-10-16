langlist="af ar as ast be bg bn-IN bn-BD br bs ca cs cy da de el en-GB en-ZA eo es-AR es-CL es-ES es-MX et eu fa fi fr fy-NL ga-IE gd gl gu-IN he hi-IN hr hu hy-AM id is it ja kk ko km kn lt lv mai mk ml mr nb-NO nl nn-NO or pa-IN pl pt-BR pt-PT ro ru si sk sl sq sr sv-SE ta te th tr uk vi zh-CN zh-TW"

fversion=`grep ^Version: firefox.spec  | awk '{print $2}'`

echo "Fetching $fversion files"
for i in $langlist;do wget https://ftp.mozilla.org/pub/mozilla.org/firefox/releases/$fversion/linux-i686/xpi/$i.xpi;done

if [ -x /usr/bin/abf ]; then
    echo "Uploading to www.abf.io"
    for i in `ls *.xpi`; do /usr/bin/abf store $i | awk '{print "'"$i"'"": " $1}'; done
fi
