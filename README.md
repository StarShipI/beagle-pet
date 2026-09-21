# 夹饼桌面宠物 - 手机版 (Android)

## 项目结构
- `beagle_mobile.py` - Kivy 主程序
- `anim/` - 动画帧（从桌面版复制）
- `buildozer.spec` - 构建配置

## 本地预览 (Windows)
```
cd D:\夹饼是比格\手机版
python beagle_mobile.py
```

## 构建 APK (需要 WSL2 + Ubuntu)

Windows 上 buildozer 不支持原生运行，需要 WSL2：

1. 安装 WSL2 + Ubuntu（管理员 PowerShell）:
   ```
   wsl --install
   ```
   重启后设置 Ubuntu 用户名密码。

2. 在 Ubuntu 里安装依赖:
   ```
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   pip3 install buildozer
   ```

3. 复制项目到 WSL（或直接在 Windows 路径访问）:
   ```
   cd /mnt/d/夹饼是比格/手机版
   ```

4. 构建:
   ```
   buildozer android debug
   ```
   首次构建会自动下载 Android SDK/NDK（约 1-2GB），需 20-40 分钟。

5. 生成的 APK 在 `bin/` 目录，传到手机安装即可。

## 交互
- 点宠物 = 摸摸
- 拖动宠物 = 移动位置
- 底部按钮 = 喂食/摸摸/挑逗/拉屎
