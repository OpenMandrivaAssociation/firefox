
# HG changeset patch
# User Paul Adenot <paul@paul.cx>
# Date 1714136726 0
# Node ID fe050f00b35a8a1d503e218c0f8ed181dc935629
# Parent  f0be91bf67da6d7771e7444085157972500e15ab
Bug 1889978 - FFVPX is now using FFmpeg API 7.0. r=media-playback-reviewers,alwu

Differential Revision: https://phabricator.services.mozilla.com/D206925

diff --git a/dom/media/platforms/ffmpeg/ffvpx/moz.build b/dom/media/platforms/ffmpeg/ffvpx/moz.build
--- a/dom/media/platforms/ffmpeg/ffvpx/moz.build
+++ b/dom/media/platforms/ffmpeg/ffvpx/moz.build
@@ -20,17 +20,17 @@ UNIFIED_SOURCES += [
     "../FFmpegVideoDecoder.cpp",
     "../FFmpegVideoEncoder.cpp",
 ]
 SOURCES += [
     "FFVPXRuntimeLinker.cpp",
 ]
 LOCAL_INCLUDES += [
     "..",
-    "../ffmpeg60/include",
+    "../ffmpeg61/include",
     "/media/mozva",
 ]
 
 CXXFLAGS += ["-Wno-deprecated-declarations"]
 if CONFIG["CC_TYPE"] == "clang":
     CXXFLAGS += [
         "-Wno-unknown-attributes",
     ]

