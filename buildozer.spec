[app]
title = 夹饼桌面宠物
package.name = beaglepet
package.domain = org.beagle
source.dir = .
source.include_exts = py,png
source.main = beagle_mobile.py
version = 1.0
requirements = python3==3.13.9,hostpython3==3.13.9,kivy==2.3.1
orientation = portrait
fullscreen = 1
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
