[app]
title = Branch Manager
package.name = branchmanager
package.domain = com.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0

requirements = python3,kivy,kivymd,requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25.1.8937393
android.accept_sdk_license = True
android.skip_update = False

[buildozer]
log_level = 2
warn_on_root = 1
