# OuterD 项目结构详细说明文档

## 项目概述

**OuterD** 是一个跨平台远程桌面控制应用程序，基于 RustDesk 开发。采用 **Rust 后端 + Flutter 前端** 的混合架构，支持 Windows、macOS、Linux、Android、iOS 等多个平台。

- **当前版本**: 1.4.6
- **开发语言**: Rust (核心) + Dart/Flutter (UI)
- **许可证**: AGPL-3.0
- **官方网站**: https://outerd.com

---

## 技术栈

### 核心技术
- **Rust**: 核心逻辑、网络通信、音视频处理
- **Flutter/Dart**: 跨平台用户界面
- **FFI**: Rust 与 Flutter 之间的桥接（flutter_rust_bridge）

### 关键依赖库
- **视频编解码**: libvpx, libyuv, opus, aom
- **屏幕捕获**: 自研 scrap 库（支持 DXGI, Quartz, X11, Wayland, PipeWire）
- **输入模拟**: 自研 enigo 库
- **剪贴板**: 自研 clipboard 库
- **网络协议**: KCP, TCP, UDP
- **GUI 框架**: Flutter (现代), Sciter (遗留，已弃用)

---

## 目录结构总览

```
outerd/
├── src/                          # Rust 核心代码
├── flutter/                      # Flutter 前端代码
├── libs/                         # 核心库
│   ├── hbb_common/              # 通用工具库
│   ├── scrap/                   # 屏幕捕获库
│   ├── enigo/                   # 输入模拟库
│   ├── clipboard/               # 剪贴板库
│   ├── virtual_display/         # 虚拟显示器
│   ├── portable/                # 便携版支持
│   └── remote_printer/          # 远程打印
├── res/                          # 资源文件（图标、图片等）
├── docs/                         # 多语言文档
├── .cargo/                       # Cargo 配置
├── build.py                      # Python 构建脚本
├── build.rs                      # Rust 构建脚本
├── Cargo.toml                    # Rust 项目配置
├── Dockerfile                    # Docker 构建配置
└── vcpkg.json                    # vcpkg 依赖配置
```

---

## 一、src/ - Rust 核心代码

### 1.1 核心模块

#### 主入口文件
- **[main.rs](src/main.rs)** - 程序主入口
- **[lib.rs](src/lib.rs)** - 库导出接口
- **[core_main.rs](src/core_main.rs:1)** (34.1 KB) - 核心启动逻辑
- **[common.rs](src/common.rs:1)** (96.9 KB) - 通用工具函数和常量

#### 客户端相关
- **[client.rs](src/client.rs:1)** (149.2 KB) - 客户端连接管理
  - **[client/io_loop.rs](src/client/io_loop.rs:1)** (112.5 KB) - IO 事件循环
  - **[client/file_trait.rs](src/client/file_trait.rs:1)** - 文件传输特性
  - **[client/helper.rs](src/client/helper.rs:1)** - 辅助函数
  - **[client/screenshot.rs](src/client/screenshot.rs:1)** - 截图功能

#### 服务端相关
- **[server.rs](src/server.rs:1)** - 服务器端主逻辑
  - **[server/connection.rs](src/server/connection.rs:1)** (232.0 KB) - **最大文件**，连接处理核心
  - **[server/audio_service.rs](src/server/audio_service.rs:1)** - 音频服务
  - **[server/clipboard_service.rs](src/server/clipboard_service.rs:1)** - 剪贴板服务
  - **[server/display_service.rs](src/server/display_service.rs:1)** - 显示服务
  - **[server/input_service.rs](src/server/input_service.rs:1)** (78.0 KB) - 输入服务
  - **[server/video_service.rs](src/server/video_service.rs:1)** - 视频流服务
  - **[server/video_qos.rs](src/server/video_qos.rs:1)** - 视频质量控制
  - **[server/terminal_service.rs](src/server/terminal_service.rs:1)** - 终端服务
  - **[server/terminal_helper.rs](src/server/terminal_helper.rs:1)** - 终端辅助
  - **[server/portable_service.rs](src/server/portable_service.rs:1)** - 便携版服务
  - **[server/printer_service.rs](src/server/printer_service.rs:1)** - 打印机服务
  - **[server/rdp_input.rs](src/server/rdp_input.rs:1)** - RDP 输入支持
  - **[server/service.rs](src/server/service.rs:1)** - 基础服务抽象
  - **[server/dbus.rs](src/server/dbus.rs:1)** - Linux D-Bus 集成
  - **[server/uinput.rs](src/server/uinput.rs:1)** - Linux uinput 输入
  - **[server/wayland.rs](src/server/wayland.rs:1)** - Wayland 支持

#### Flutter 绑定
- **[flutter.rs](src/flutter.rs:1)** (77.9 KB) - Flutter 绑定实现
- **[flutter_ffi.rs](src/flutter_ffi.rs:1)** (94.4 KB) - FFI 接口定义

#### 进程间通信
- **[ipc.rs](src/ipc.rs:1)** (57.2 KB) - IPC 通信机制

#### 输入处理
- **[keyboard.rs](src/keyboard.rs:1)** (46.9 KB) - 键盘输入处理

### 1.2 平台特定代码 (platform/)

#### 主模块
- **[platform/mod.rs](src/platform/mod.rs:1)** - 平台模块导出

#### Windows 平台
- **[platform/windows.rs](src/platform/windows.rs:1)** (142.2 KB) - Windows 实现
- **[platform/windows.cc](src/platform/windows.cc:1)** - Windows C++ 辅助代码
- **[platform/win_device.rs](src/platform/win_device.rs:1)** - Windows 设备管理

#### macOS 平台
- **[platform/macos.rs](src/platform/macos.rs:1)** (42.7 KB) - macOS 实现
- **[platform/macos.mm](src/platform/macos.mm:1)** - macOS Objective-C++ 代码

#### Linux 平台
- **[platform/linux.rs](src/platform/linux.rs:1)** (72.8 KB) - Linux 实现
- **[platform/linux_desktop_manager.rs](src/platform/linux_desktop_manager.rs:1)** - Linux 桌面环境管理

#### 其他
- **[platform/delegate.rs](src/platform/delegate.rs:1)** - 委托处理
- **[platform/gtk_sudo.rs](src/platform/gtk_sudo.rs:1)** - GTK sudo 提权对话框
- **[platform/privileges_scripts/](src/platform/privileges_scripts/)** - macOS 权限脚本
  - `agent.plist` - LaunchAgent 配置
  - `daemon.plist` - LaunchDaemon 配置
  - `install.scpt` - AppleScript 安装脚本
  - `uninstall.scpt` - AppleScript 卸载脚本
  - `update.scpt` - AppleScript 更新脚本

### 1.3 插件系统 (plugin/)

- **[plugin/mod.rs](src/plugin/mod.rs:1)** - 插件模块导出
- **[plugin/manager.rs](src/plugin/manager.rs:1)** (20.2 KB) - 插件管理器
- **[plugin/plugins.rs](src/plugin/plugins.rs:1)** (20.7 KB) - 插件注册
- **[plugin/config.rs](src/plugin/config.rs:1)** - 插件配置
- **[plugin/ipc.rs](src/plugin/ipc.rs:1)** - 插件 IPC 通信
- **[plugin/callback_msg.rs](src/plugin/callback_msg.rs:1)** - 消息回调
- **[plugin/callback_ext.rs](src/plugin/callback_ext.rs:1)** - 扩展回调
- **[plugin/native.rs](src/plugin/native.rs:1)** - 原生插件支持
- **[plugin/native_handlers/](src/plugin/native_handlers/)** - 原生处理器
  - `mod.rs` - 模块导出
  - `macros.rs` - 宏定义
  - `session.rs` - Session 处理器
  - `ui.rs` - UI 处理器
- **[plugin/desc.rs](src/plugin/desc.rs:1)** - 描述信息
- **[plugin/errno.rs](src/plugin/errno.rs:1)** - 错误码定义
- **[plugin/plog.rs](src/plugin/plog.rs:1)** - 日志记录

### 1.4 白板功能 (whiteboard/)

- **[whiteboard/mod.rs](src/whiteboard/mod.rs:1)** - 白板模块
- **[whiteboard/client.rs](src/whiteboard/client.rs:1)** - 客户端白板
- **[whiteboard/server.rs](src/whiteboard/server.rs:1)** - 服务端白板
- **[whiteboard/windows.rs](src/whiteboard/windows.rs:1)** - Windows 白板实现
- **[whiteboard/linux.rs](src/whiteboard/linux.rs:1)** - Linux 白板实现
- **[whiteboard/macos.rs](src/whiteboard/macos.rs:1)** - macOS 白板实现
- **[whiteboard/win_linux.rs](src/whiteboard/win_linux.rs:1)** - Win/Linux 共享实现

### 1.5 HTTP 服务 (hbbs_http/)

- **[hbbs_http/mod.rs](src/hbbs_http/mod.rs:1)** - HTTP 模块
- **[hbbs_http/account.rs](src/hbbs_http/account.rs:1)** - 账户管理
- **[hbbs_http/http_client.rs](src/hbbs_http/http_client.rs:1)** - HTTP 客户端
- **[hbbs_http/downloader.rs](src/hbbs_http/downloader.rs:1)** - 下载器
- **[hbbs_http/sync.rs](src/hbbs_http/sync.rs:1)** - 数据同步
- **[hbbs_http/record_upload.rs](src/hbbs_http/record_upload.rs:1)** - 记录上传

### 1.6 国际化 (lang/)

支持 **40+ 种语言**的本地化：

- **[lang/mod.rs](src/lang/mod.rs:1)** - 语言模块
- **[lang/template.rs](src/lang/template.rs:1)** - 翻译模板
- **[lang/en.rs](src/lang/en.rs:1)** - 英语
- **[lang/cn.rs](src/lang/cn.rs:1)** - 简体中文
- **[lang/tw.rs](src/lang/tw.rs:1)** - 繁体中文
- **[lang/ja.rs](src/lang/ja.rs:1)** - 日语
- **[lang/ko.rs](src/lang/ko.rs:1)** - 韩语
- 其他语言：德语、法语、西班牙语、俄语等约 35 种

### 1.7 隐私模式 (privacy_mode/)

- **[privacy_mode/win_mag.rs](src/privacy_mode/win_mag.rs:1)** - Windows 放大镜隐私模式
- **[privacy_mode/win_exclude_from_capture.rs](src/privacy_mode/win_exclude_from_capture.rs:1)** - Windows 排除捕获
- **[privacy_mode/win_input.rs](src/privacy_mode/win_input.rs:1)** - Windows 输入隐私
- **[privacy_mode/win_virtual_display.rs](src/privacy_mode/win_virtual_display.rs:1)** - Windows 虚拟显示
- **[privacy_mode/macos.rs](src/privacy_mode/macos.rs:1)** - macOS 隐私模式

### 1.8 遗留 UI (ui/) - 已弃用

使用 Sciter 框架的旧版 UI，已被 Flutter 取代：

- `index.html/tis/css` - 主界面
- `remote.html/tis/css` - 远程控制界面
- `cm.html/tis/css` - 连接管理器
- `file_transfer.tis/css` - 文件传输界面
- `ab.tis` - 地址簿
- `header.tis/css` - 头部组件
- `common.tis/css` - 通用组件

### 1.9 其他核心模块

- **[auth_2fa.rs](src/auth_2fa.rs:1)** - 双因素认证
- **[cli.rs](src/cli.rs:1)** - 命令行接口
- **[clipboard.rs](src/clipboard.rs:1)** - 剪贴板处理
- **[clipboard_file.rs](src/clipboard_file.rs:1)** - 剪贴板文件传输
- **[custom_server.rs](src/custom_server.rs:1)** - 自定义服务器配置
- **[kcp_stream.rs](src/kcp_stream.rs:1)** - KCP 协议流实现
- **[lan.rs](src/lan.rs:1)** - 局域网发现
- **[lang.rs](src/lang.rs:1)** - 语言切换
- **[naming.rs](src/naming.rs:1)** - 命名服务（独立二进制）
- **[port_forward.rs](src/port_forward.rs:1)** - 端口转发
- **[rendezvous_mediator.rs](src/rendezvous_mediator.rs:1)** - 会合中介（P2P 穿透）
- **[service.rs](src/service.rs:1)** - 系统服务（独立二进制）
- **[tray.rs](src/tray.rs:1)** - 系统托盘
- **[updater.rs](src/updater.rs:1)** - 自动更新
- **[virtual_display_manager.rs](src/virtual_display_manager.rs:1)** - 虚拟显示管理
- **[ui_interface.rs](src/ui_interface.rs:1)** - UI 接口
- **[ui_cm_interface.rs](src/ui_cm_interface.rs:1)** - CM UI 接口
- **[ui_session_interface.rs](src/ui_session_interface.rs:1)** - Session UI 接口

---

## 二、flutter/ - Flutter 前端代码

### 2.1 配置文件

- **[pubspec.yaml](flutter/pubspec.yaml:1)** - Flutter 项目配置
- **[analysis_options.yaml](flutter/analysis_options.yaml:1)** - 代码分析配置
- **[build_android.sh](flutter/build_android.sh:1)** - Android 构建脚本
- **[build_ios.sh](flutter/build_ios.sh:1)** - iOS 构建脚本
- **[build_fdroid.sh](flutter/build_fdroid.sh:1)** - F-Droid 构建脚本
- **[run.sh](flutter/run.sh:1)** - 开发运行脚本

### 2.2 主入口

- **[lib/main.dart](flutter/lib/main.dart:1)** (18.8 KB) - 应用主入口

### 2.3 共享代码 (common/)

#### 核心工具
- **[lib/common/common.dart](flutter/lib/common/common.dart:1)** (126.0 KB) - **最大文件**，通用工具函数
- **[lib/common/consts.dart](flutter/lib/common/consts.dart:1)** - 常量定义
- **[lib/common/shared_state.dart](flutter/lib/common/shared_state.dart:1)** - 共享状态管理

#### 格式化
- **[lib/common/formatter/id_formatter.dart](flutter/lib/common/formatter/id_formatter.dart:1)** - ID 格式化

#### HBBS 服务
- **[lib/common/hbbs/hbbs.dart](flutter/lib/common/hbbs/hbbs.dart:1)** - HBBS 服务集成

#### 通用组件 (widgets/)
- **[lib/common/widgets/dialog.dart](flutter/lib/common/widgets/dialog.dart:1)** (83.4 KB) - 对话框组件
- **[lib/common/widgets/peer_card.dart](flutter/lib/common/widgets/peer_card.dart:1)** (50.0 KB) - 对等卡片
- **[lib/common/widgets/toolbar.dart](flutter/lib/common/widgets/toolbar.dart:1)** (34.2 KB) - 工具栏
- **[lib/common/widgets/peer_tab_page.dart](flutter/lib/common/widgets/peer_tab_page.dart:1)** - 标签页
- **[lib/common/widgets/peers_view.dart](flutter/lib/common/widgets/peers_view.dart:1)** - 对等视图
- **[lib/common/widgets/address_book.dart](flutter/lib/common/widgets/address_book.dart:1)** - 地址簿
- **[lib/common/widgets/login.dart](flutter/lib/common/widgets/login.dart:1)** - 登录界面
- **[lib/common/widgets/chat_page.dart](flutter/lib/common/widgets/chat_page.dart:1)** - 聊天页面
- **[lib/common/widgets/gestures.dart](flutter/lib/common/widgets/gestures.dart:1)** - 手势识别
- **[lib/common/widgets/overlay.dart](flutter/lib/common/widgets/overlay.dart:1)** - 覆盖层
- **[lib/common/widgets/autocomplete.dart](flutter/lib/common/widgets/autocomplete.dart:1)** - 自动完成

### 2.4 桌面端代码 (desktop/)

#### 页面 (pages/)
- **[lib/desktop/pages/desktop_home_page.dart](flutter/lib/desktop/pages/desktop_home_page.dart:1)** - 桌面主页
- **[lib/desktop/pages/desktop_setting_page.dart](flutter/lib/desktop/pages/desktop_setting_page.dart:1)** (100.7 KB) - 设置页面
- **[lib/desktop/pages/connection_page.dart](flutter/lib/desktop/pages/connection_page.dart:1)** - 连接页面
- **[lib/desktop/pages/remote_page.dart](flutter/lib/desktop/pages/remote_page.dart:1)** - 远程控制页面
- **[lib/desktop/pages/file_manager_page.dart](flutter/lib/desktop/pages/file_manager_page.dart:1)** - 文件管理
- **[lib/desktop/pages/terminal_page.dart](flutter/lib/desktop/pages/terminal_page.dart:1)** - 终端页面
- **[lib/desktop/pages/view_camera_page.dart](flutter/lib/desktop/pages/view_camera_page.dart:1)** - 摄像头查看
- **[lib/desktop/pages/port_forward_page.dart](flutter/lib/desktop/pages/port_forward_page.dart:1)** - 端口转发
- **[lib/desktop/pages/server_page.dart](flutter/lib/desktop/pages/server_page.dart:1)** - 服务器配置
- **[lib/desktop/pages/install_page.dart](flutter/lib/desktop/pages/install_page.dart:1)** - 安装页面
- **[lib/desktop/pages/desktop_tab_page.dart](flutter/lib/desktop/pages/desktop_tab_page.dart:1)** - 标签页容器

#### 屏幕组件 (screen/)
- **[lib/desktop/screen/desktop_remote_screen.dart](flutter/lib/desktop/screen/desktop_remote_screen.dart:1)** - 远程桌面屏幕
- **[lib/desktop/screen/desktop_file_transfer_screen.dart](flutter/lib/desktop/screen/desktop_file_transfer_screen.dart:1)** - 文件传输屏幕
- **[lib/desktop/screen/desktop_terminal_screen.dart](flutter/lib/desktop/screen/desktop_terminal_screen.dart:1)** - 终端屏幕
- **[lib/desktop/screen/desktop_port_forward_screen.dart](flutter/lib/desktop/screen/desktop_port_forward_screen.dart:1)** - 端口转发屏幕
- **[lib/desktop/screen/desktop_view_camera_screen.dart](flutter/lib/desktop/screen/desktop_view_camera_screen.dart:1)** - 摄像头屏幕

#### 桌面组件 (widgets/)
- **[lib/desktop/widgets/remote_toolbar.dart](flutter/lib/desktop/widgets/remote_toolbar.dart:1)** (85.7 KB) - 远程工具栏
- **[lib/desktop/widgets/tabbar_widget.dart](flutter/lib/desktop/widgets/tabbar_widget.dart:1)** (49.7 KB) - 标签栏组件
- **[lib/desktop/widgets/material_mod_popup_menu.dart](flutter/lib/desktop/widgets/material_mod_popup_menu.dart:1)** - 弹出菜单
- **[lib/desktop/widgets/popup_menu.dart](flutter/lib/desktop/widgets/popup_menu.dart:1)** - 弹出菜单
- **[lib/desktop/widgets/button.dart](flutter/lib/desktop/widgets/button.dart:1)** - 按钮组件
- **[lib/desktop/widgets/update_progress.dart](flutter/lib/desktop/widgets/update_progress.dart:1)** - 更新进度
- **[lib/desktop/widgets/kb_layout_type_chooser.dart](flutter/lib/desktop/widgets/kb_layout_type_chooser.dart:1)** - 键盘布局选择

### 2.5 移动端代码 (mobile/)

#### 页面 (pages/)
- **[lib/mobile/pages/home_page.dart](flutter/lib/mobile/pages/home_page.dart:1)** - 移动主页
- **[lib/mobile/pages/connection_page.dart](flutter/lib/mobile/pages/connection_page.dart:1)** - 连接页面
- **[lib/mobile/pages/remote_page.dart](flutter/lib/mobile/pages/remote_page.dart:1)** (48.8 KB) - 远程控制页面
- **[lib/mobile/pages/file_manager_page.dart](flutter/lib/mobile/pages/file_manager_page.dart:1)** - 文件管理
- **[lib/mobile/pages/settings_page.dart](flutter/lib/mobile/pages/settings_page.dart:1)** - 设置页面
- **[lib/mobile/pages/server_page.dart](flutter/lib/mobile/pages/server_page.dart:1)** - 服务器配置
- **[lib/mobile/pages/terminal_page.dart](flutter/lib/mobile/pages/terminal_page.dart:1)** - 终端页面
- **[lib/mobile/pages/scan_page.dart](flutter/lib/mobile/pages/scan_page.dart:1)** - QR 码扫描
- **[lib/mobile/pages/view_camera_page.dart](flutter/lib/mobile/pages/view_camera_page.dart:1)** - 摄像头查看

#### 移动组件 (widgets/)
- **[lib/mobile/widgets/floating_mouse.dart](flutter/lib/mobile/widgets/floating_mouse.dart:1)** (40.4 KB) - 浮动鼠标控制
- **[lib/mobile/widgets/floating_mouse_widgets.dart](flutter/lib/mobile/widgets/floating_mouse_widgets.dart:1)** - 浮动鼠标子组件
- **[lib/mobile/widgets/gesture_help.dart](flutter/lib/mobile/widgets/gesture_help.dart:1)** - 手势帮助
- **[lib/mobile/widgets/dialog.dart](flutter/lib/mobile/widgets/dialog.dart:1)** - 对话框
- **[lib/mobile/widgets/custom_scale_widget.dart](flutter/lib/mobile/widgets/custom_scale_widget.dart:1)** - 自定义缩放

### 2.6 数据模型 (models/)

- **[lib/models/model.dart](flutter/lib/models/model.dart:1)** (137.0 KB) - **主模型文件**
- **[lib/models/ab_model.dart](flutter/lib/models/ab_model.dart:1)** - 地址簿模型
- **[lib/models/file_model.dart](flutter/lib/models/file_model.dart:1)** - 文件模型
- **[lib/models/input_model.dart](flutter/lib/models/input_model.dart:1)** - 输入模型
- **[lib/models/relative_mouse_model.dart](flutter/lib/models/relative_mouse_model.dart:1)** - 相对鼠标模型
- **[lib/models/peer_model.dart](flutter/lib/models/peer_model.dart:1)** - 对等设备模型
- **[lib/models/server_model.dart](flutter/lib/models/server_model.dart:1)** - 服务器模型
- **[lib/models/chat_model.dart](flutter/lib/models/chat_model.dart:1)** - 聊天模型
- **[lib/models/group_model.dart](flutter/lib/models/group_model.dart:1)** - 设备组模型
- **[lib/models/terminal_model.dart](flutter/lib/models/terminal_model.dart:1)** - 终端模型
- **[lib/models/state_model.dart](flutter/lib/models/state_model.dart:1)** - 状态模型
- **[lib/models/user_model.dart](flutter/lib/models/user_model.dart:1)** - 用户模型

### 2.7 插件系统 (plugin/)

- **[lib/plugin/manager.dart](flutter/lib/plugin/manager.dart:1)** - 插件管理器
- **[lib/plugin/handlers.dart](flutter/lib/plugin/handlers.dart:1)** - 插件处理器
- **[lib/plugin/model.dart](flutter/lib/plugin/model.dart:1)** - 插件模型
- **[lib/plugin/event.dart](flutter/lib/plugin/event.dart:1)** - 插件事件
- **[lib/plugin/common.dart](flutter/lib/plugin/common.dart:1)** - 插件通用
- **[lib/plugin/ui_manager.dart](flutter/lib/plugin/ui_manager.dart:1)** - UI 插件管理
- **[lib/plugin/utils/dialogs.dart](flutter/lib/plugin/utils/dialogs.dart:1)** - 对话框工具
- **[lib/plugin/widgets/desc_ui.dart](flutter/lib/plugin/widgets/desc_ui.dart:1)** - 描述 UI
- **[lib/plugin/widgets/desktop_settings.dart](flutter/lib/plugin/widgets/desktop_settings.dart:1)** - 桌面设置

### 2.8 原生集成 (native/)

- **[lib/native/common.dart](flutter/lib/native/common.dart:1)** - 原生通用
- **[lib/native/custom_cursor.dart](flutter/lib/native/custom_cursor.dart:1)** - 自定义光标
- **[lib/native/win32.dart](flutter/lib/native/win32.dart:1)** - Win32 API 调用

### 2.9 Web 平台支持 (web/)

- **[lib/web/bridge.dart](flutter/lib/web/bridge.dart:1)** (59.1 KB) - Web 桥接层
- **[lib/web/common.dart](flutter/lib/web/common.dart:1)** - Web 通用
- **[lib/web/custom_cursor.dart](flutter/lib/web/custom_cursor.dart:1)** - Web 自定义光标
- **[lib/web/dummy.dart](flutter/lib/web/dummy.dart:1)** - 占位实现
- **[lib/web/settings_page.dart](flutter/lib/web/settings_page.dart:1)** - Web 设置页
- **[lib/web/texture_rgba_renderer.dart](flutter/lib/web/texture_rgba_renderer.dart:1)** - 纹理渲染
- **[lib/web/web_unique.dart](flutter/lib/web/web_unique.dart:1)** - Web 特有功能
- **[lib/web/win32.dart](flutter/lib/web/win32.dart:1)** - Web Win32 模拟
- **[lib/web/plugin/handlers.dart](flutter/lib/web/plugin/handlers.dart:1)** - Web 插件处理器

### 2.10 工具类 (utils/)

- **[lib/utils/event_loop.dart](flutter/lib/utils/event_loop.dart:1)** - 事件循环
- **[lib/utils/http_service.dart](flutter/lib/utils/http_service.dart:1)** - HTTP 服务
- **[lib/utils/image.dart](flutter/lib/utils/image.dart:1)** - 图像处理
- **[lib/utils/multi_window_manager.dart](flutter/lib/utils/multi_window_manager.dart:1)** - 多窗口管理
- **[lib/utils/platform_channel.dart](flutter/lib/utils/platform_channel.dart:1)** - 平台通道
- **[lib/utils/scale.dart](flutter/lib/utils/scale.dart:1)** - 缩放计算
- **[lib/utils/relative_mouse_accumulator.dart](flutter/lib/utils/relative_mouse_accumulator.dart:1)** - 相对鼠标累加器

### 2.11 资源文件 (assets/)

包含 50+ 个 SVG/PNG 图标和字体文件：
- SVG 图标（各种 UI 元素）
- PNG 图片（Logo、截图等）
- TTF 字体文件（GestureIcons, Tabbar, AddressBook 等自定义字体）

### 2.12 平台特定代码

#### Android (android/)
- **[android/app/src/main/kotlin/com/carriez/flutter_hbb/MainActivity.kt](flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/MainActivity.kt:1)** - 主活动
- **[android/app/src/main/kotlin/com/carriez/flutter_hbb/MainService.kt](flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/MainService.kt:1)** - 主服务
- **[android/app/src/main/kotlin/com/carriez/flutter_hbb/InputService.kt](flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/InputService.kt:1)** - 输入服务
- **[android/app/src/main/kotlin/com/carriez/flutter_hbb/FloatingWindowService.kt](flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/FloatingWindowService.kt:1)** - 悬浮窗服务
- **[android/app/src/main/kotlin/com/carriez/flutter_hbb/AudioRecordHandle.kt](flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/AudioRecordHandle.kt:1)** - 音频录制
- **[android/app/src/main/kotlin/com/carriez/flutter_hbb/VolumeController.kt](flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/VolumeController.kt:1)** - 音量控制
- **[android/app/src/main/kotlin/com/carriez/flutter_hbb/RdClipboardManager.kt](flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/RdClipboardManager.kt:1)** - 剪贴板管理
- **[android/app/src/main/kotlin/com/carriez/flutter_hbb/BootReceiver.kt](flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/BootReceiver.kt:1)** - 启动接收器
- **[android/app/src/main/kotlin/com/carriez/flutter_hbb/KeyboardKeyEventMapper.kt](flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/KeyboardKeyEventMapper.kt:1)** - 键盘事件映射
- **[android/app/src/main/kotlin/com/carriez/flutter_hbb/PermissionRequestTransparentActivity.kt](flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/PermissionRequestTransparentActivity.kt:1)** - 权限请求
- **[android/app/src/main/kotlin/com/carriez/flutter_hbb/MainApplication.kt](flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/MainApplication.kt:1)** - 应用类
- **[android/app/src/main/kotlin/com/carriez/flutter_hbb/common.kt](flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/common.kt:1)** - 通用函数
- **[android/app/src/main/kotlin/com/carriez/flutter_hbb/ffi.kt](flutter/android/app/src/main/kotlin/com/carriez/flutter_hbb/ffi.kt:1)** - FFI 绑定

#### iOS (ios/)
- **[ios/Runner/AppDelegate.swift](flutter/ios/Runner/AppDelegate.swift:1)** - iOS 应用代理
- **[ios/Runner/MainFlutterWindow.swift](flutter/ios/Runner/MainFlutterWindow.swift:1)** - 主窗口
- **[ios/Runner/Assets.xcassets/](flutter/ios/Runner/Assets.xcassets/)** - iOS 资源

#### macOS (macos/)
- **[macos/Runner/AppDelegate.swift](flutter/macos/Runner/AppDelegate.swift:1)** - macOS 应用代理
- **[macos/Runner/MainFlutterWindow.swift](flutter/macos/Runner/MainFlutterWindow.swift:1)** - 主窗口

#### Windows (windows/)
- **[windows/runner/main.cpp](flutter/windows/runner/main.cpp:1)** - Windows 入口
- **[windows/runner/flutter_window.cpp](flutter/windows/runner/flutter_window.cpp:1)** - Flutter 窗口
- **[windows/runner/win32_window.cpp](flutter/windows/runner/win32_window.cpp:1)** - Win32 窗口
- **[windows/runner/win32_desktop.cpp](flutter/windows/runner/win32_desktop.cpp:1)** - 桌面集成

#### Linux (linux/)
- **[linux/main.cc](flutter/linux/main.cc:1)** - Linux 入口
- **[linux/my_application.cc](flutter/linux/my_application.cc:1)** - 应用实现
- **[linux/bump_mouse.cc](flutter/linux/bump_mouse.cc:1)** - 鼠标增强
- **[linux/bump_mouse_x11.cc](flutter/linux/bump_mouse_x11.cc:1)** - X11 鼠标增强
- **[linux/wayland_shortcuts_inhibit.cc](flutter/linux/wayland_shortcuts_inhibit.cc:1)** - Wayland 快捷键抑制

### 2.13 测试 (test/)
- **[test/cm_test.dart](flutter/test/cm_test.dart:1)** - 连接管理测试

---

## 三、libs/ - 核心库

### 3.1 hbb_common - 通用库

位于 **[libs/hbb_common/](libs/hbb_common/)**，提供：
- 视频编解码封装
- 配置管理
- TCP/UDP 网络封装
- Protobuf 序列化
- 文件传输文件系统操作
- 通用工具函数

### 3.2 scrap - 屏幕捕获库

位于 **[libs/scrap/](libs/scrap/)**，支持多平台屏幕捕获：

#### 核心代码
- **[libs/scrap/src/lib.rs](libs/scrap/src/lib.rs:1)** - 库入口
- **[libs/scrap/src/common/mod.rs](libs/scrap/src/common/mod.rs:1)** - 通用捕获逻辑
- **[libs/scrap/src/common/codec.rs](libs/scrap/src/common/codec.rs:1)** (39.7 KB) - 编解码器
- **[libs/scrap/src/common/aom.rs](libs/scrap/src/common/aom.rs:1)** - AV1 编码
- **[libs/scrap/src/common/vpx.rs](libs/scrap/src/common/vpx.rs:1)** - VP8/VP9 编码
- **[libs/scrap/src/common/hwcodec.rs](libs/scrap/src/common/hwcodec.rs:1)** - 硬件编解码
- **[libs/scrap/src/common/convert.rs](libs/scrap/src/common/convert.rs:1)** - 格式转换
- **[libs/scrap/src/common/camera.rs](libs/scrap/src/common/camera.rs:1)** - 摄像头捕获
- **[libs/scrap/src/common/record.rs](libs/scrap/src/common/record.rs:1)** - 屏幕录制
- **[libs/scrap/src/common/vram.rs](libs/scrap/src/common/vram.rs:1)** - VRAM 优化

#### 平台特定实现
- **[libs/scrap/src/common/android.rs](libs/scrap/src/common/android.rs:1)** - Android MediaCodec
- **[libs/scrap/src/common/linux.rs](libs/scrap/src/common/linux.rs:1)** - Linux 通用
- **[libs/scrap/src/common/x11.rs](libs/scrap/src/common/x11.rs:1)** - X11 捕获
- **[libs/scrap/src/common/wayland.rs](libs/scrap/src/common/wayland.rs:1)** - Wayland 捕获
- **[libs/scrap/src/common/quartz.rs](libs/scrap/src/common/quartz.rs:1)** - macOS Quartz
- **[libs/scrap/src/common/dxgi.rs](libs/scrap/src/common/dxgi.rs:1)** - Windows DXGI
- **[libs/scrap/src/common/mediacodec.rs](libs/scrap/src/common/mediacodec.rs:1)** - Android MediaCodec

#### 详细实现
- **[libs/scrap/src/dxgi/mod.rs](libs/scrap/src/dxgi/mod.rs:1)** (32.8 KB) - DXGI 主实现
- **[libs/scrap/src/dxgi/mag.rs](libs/scrap/src/dxgi/mag.rs:1)** - 放大镜捕获
- **[libs/scrap/src/dxgi/gdi.rs](libs/scrap/src/dxgi/gdi.rs:1)** - GDI 回退
- **[libs/scrap/src/x11/capturer.rs](libs/scrap/src/x11/capturer.rs:1)** - X11 捕获器
- **[libs/scrap/src/x11/display.rs](libs/scrap/src/x11/display.rs:1)** - X11 显示
- **[libs/scrap/src/x11/ffi.rs](libs/scrap/src/x11/ffi.rs:1)** - X11 FFI
- **[libs/scrap/src/wayland/pipewire.rs](libs/scrap/src/wayland/pipewire.rs:1)** (52.2 KB) - PipeWire 实现
- **[libs/scrap/src/wayland/display.rs](libs/scrap/src/wayland/display.rs:1)** - Wayland 显示
- **[libs/scrap/src/quartz/capturer.rs](libs/scrap/src/quartz/capturer.rs:1)** - Quartz 捕获器
- **[libs/scrap/src/quartz/display.rs](libs/scrap/src/quartz/display.rs:1)** - Quartz 显示

#### 示例程序
- `examples/benchmark.rs` - 性能基准测试
- `examples/screenshot.rs` - 截图示例
- `examples/capture_mag.rs` - 放大镜捕获示例

### 3.3 enigo - 输入模拟库

位于 **[libs/enigo/](libs/enigo/)**，跨平台键盘/鼠标控制：

- **[libs/enigo/src/lib.rs](libs/enigo/src/lib.rs:1)** (14.5 KB) - 库入口
- **[libs/enigo/src/dsl.rs](libs/enigo/src/dsl.rs:1)** - DSL 解析器
- **[libs/enigo/src/win/mod.rs](libs/enigo/src/win/mod.rs:1)** - Windows 输入
- **[libs/enigo/src/win/win_impl.rs](libs/enigo/src/win/win_impl.rs:1)** - Windows 实现
- **[libs/enigo/src/win/keycodes.rs](libs/enigo/src/win/keycodes.rs:1)** - Windows 键码
- **[libs/enigo/src/macos/mod.rs](libs/enigo/src/macos/mod.rs:1)** - macOS 输入
- **[libs/enigo/src/macos/macos_impl.rs](libs/enigo/src/macos/macos_impl.rs:1)** (30.6 KB) - macOS 实现
- **[libs/enigo/src/macos/keycodes.rs](libs/enigo/src/macos/keycodes.rs:1)** - macOS 键码
- **[libs/enigo/src/linux/mod.rs](libs/enigo/src/linux/mod.rs:1)** - Linux 输入
- **[libs/enigo/src/linux/nix_impl.rs](libs/enigo/src/linux/nix_impl.rs:1)** - Linux 实现
- **[libs/enigo/src/linux/xdo.rs](libs/enigo/src/linux/xdo.rs:1)** - XDo 实现

### 3.4 clipboard - 剪贴板库

位于 **[libs/clipboard/](libs/clipboard/)**，跨平台剪贴板实现：

- **[libs/clipboard/src/lib.rs](libs/clipboard/src/lib.rs:1)** - 库入口
- **[libs/clipboard/src/context_send.rs](libs/clipboard/src/context_send.rs:1)** - 上下文发送
- **[libs/clipboard/src/platform/mod.rs](libs/clipboard/src/platform/mod.rs:1)** - 平台模块
- **[libs/clipboard/src/platform/windows.rs](libs/clipboard/src/platform/windows.rs:1)** (43.2 KB) - Windows 剪贴板
- **[libs/clipboard/src/platform/unix/mod.rs](libs/clipboard/src/platform/unix/mod.rs:1)** - Unix 剪贴板
- **[libs/clipboard/src/platform/unix/filetype.rs](libs/clipboard/src/platform/unix/filetype.rs:1)** - 文件类型
- **[libs/clipboard/src/platform/unix/local_file.rs](libs/clipboard/src/platform/unix/local_file.rs:1)** - 本地文件
- **[libs/clipboard/src/platform/unix/serv_files.rs](libs/clipboard/src/platform/unix/serv_files.rs:1)** - 服务文件
- **[libs/clipboard/src/platform/unix/fuse/mod.rs](libs/clipboard/src/platform/unix/fuse/mod.rs:1)** - FUSE 文件系统
- **[libs/clipboard/src/platform/unix/fuse/cs.rs](libs/clipboard/src/platform/unix/fuse/cs.rs:1)** - FUSE C 绑定
- **[libs/clipboard/src/platform/unix/macos/mod.rs](libs/clipboard/src/platform/unix/macos/mod.rs:1)** - macOS 粘贴板
- **[libs/clipboard/src/platform/unix/macos/pasteboard_context.rs](libs/clipboard/src/platform/unix/macos/pasteboard_context.rs:1)** - 粘贴板上下文
- **[libs/clipboard/src/platform/unix/macos/paste_observer.rs](libs/clipboard/src/platform/unix/macos/paste_observer.rs:1)** - 粘贴观察者
- **[libs/clipboard/src/platform/unix/macos/paste_task.rs](libs/clipboard/src/platform/unix/macos/paste_task.rs:1)** - 粘贴任务
- **[libs/clipboard/src/platform/unix/macos/item_data_provider.rs](libs/clipboard/src/platform/unix/macos/item_data_provider.rs:1)** - 数据提供者
- **[libs/clipboard/src/windows/wf_cliprdr.c](libs/clipboard/src/windows/wf_cliprdr.c:1)** (82.8 KB) - Windows CLIPRDR 实现

### 3.5 virtual_display - 虚拟显示器

位于 **[libs/virtual_display/](libs/virtual_display/)**：

- **[libs/virtual_display/src/lib.rs](libs/virtual_display/src/lib.rs:1)** - 库入口
- **[libs/virtual_display/dylib/src/lib.rs](libs/virtual_display/dylib/src/lib.rs:1)** - 动态库
- **[libs/virtual_display/dylib/src/win10/IddController.c](libs/virtual_display/dylib/src/win10/IddController.c:1)** - IDD 控制器
- **[libs/virtual_display/dylib/src/win10/IddController.h](libs/virtual_display/dylib/src/win10/IddController.h:1)** - IDD 头文件
- **[libs/virtual_display/dylib/src/win10/Public.h](libs/virtual_display/dylib/src/win10/Public.h:1)** - 公共头文件

### 3.6 portable - 便携版支持

位于 **[libs/portable/](libs/portable/)**：

- **[libs/portable/src/main.rs](libs/portable/src/main.rs:1)** - 便携版主入口
- **[libs/portable/src/bin_reader.rs](libs/portable/src/bin_reader.rs:1)** - 二进制读取器
- **[libs/portable/src/ui.rs](libs/portable/src/ui.rs:1)** - 便携版 UI
- **[libs/portable/src/res/label.png](libs/portable/src/res/label.png:1)** - 标签图片
- **[libs/portable/src/res/spin.gif](libs/portable/src/res/spin.gif:1)** - 加载动画

### 3.7 remote_printer - 远程打印

位于 **[libs/remote_printer/](libs/remote_printer/)**：

- **[libs/remote_printer/src/lib.rs](libs/remote_printer/src/lib.rs:1)** - 库入口
- **[libs/remote_printer/src/setup/mod.rs](libs/remote_printer/src/setup/mod.rs:1)** - 设置模块
- **[libs/remote_printer/src/setup/driver.rs](libs/remote_printer/src/setup/driver.rs:1)** - 驱动安装
- **[libs/remote_printer/src/setup/printer.rs](libs/remote_printer/src/setup/printer.rs:1)** - 打印机设置
- **[libs/remote_printer/src/setup/port.rs](libs/remote_printer/src/setup/port.rs:1)** - 端口设置
- **[libs/remote_printer/src/setup/setup.rs](libs/remote_printer/src/setup/setup.rs:1)** - 安装逻辑

### 3.8 libxdo-sys-stub - libxdo 存根

位于 **[libs/libxdo-sys-stub/](libs/libxdo-sys-stub/)**：
- 提供 libxdo 的存根实现，允许在没有 libxdo 的系统上构建（如纯 Wayland 环境）

---

## 四、res/ - 资源文件

- **图标**: `icon.ico`, `icon.png`, `logo.svg`, `design.svg`
- **应用图标**: 多种尺寸（32x32, 128x128, 256x256 等）
- **平台特定图标**: `mac-icon.png` (macOS)
- **UI 资源**: Logo、按钮、背景图等

---

## 五、docs/ - 文档

包含 60+ 个多语言文档：

### 行为准则 (CODE_OF_CONDUCT)
11 种语言版本：英语、乌克兰语、捷克语、中文、匈牙利语、西班牙语、波斯语、法语、德语、波兰语、印尼语等

### 贡献指南 (CONTRIBUTING)
13 种语言版本

### README 翻译
25 种语言版本

### 安全策略 (SECURITY)
9 种语言版本

---

## 六、构建配置

### 6.1 Cargo.toml 关键配置

#### 项目信息
```toml
name = "outerd"
version = "1.4.6"
edition = "2021"
rust-version = "1.75"
```

#### 功能特性 (Features)
- `inline` - 内联优化
- `cli` - 命令行接口
- `flutter` - Flutter UI 支持
- `hwcodec` - 硬件编解码
- `vram` - VRAM 优化（仅 Windows）
- `mediacodec` - Android MediaCodec
- `plugin_framework` - 插件框架
- `linux-pkg-config` - Linux pkg-config 支持
- `unix-file-copy-paste` - Unix 文件复制粘贴
- `screencapturekit` - macOS ScreenCaptureKit

#### 主要依赖
- `scrap` - 屏幕捕获（本地路径）
- `hbb_common` - 通用库（本地路径）
- `flutter_rust_bridge = "1.80"` - Flutter-Rust 桥接
- `reqwest = "0.12"` - HTTP 客户端
- `tokio` - 异步运行时
- `serde` - 序列化
- `protobuf` - 协议缓冲

### 6.2 Flutter pubspec.yaml 配置

#### 项目信息
```yaml
name: flutter_hbb
version: 1.4.6+64
sdk: '^3.1.0'
```

#### 关键依赖
- `flutter_rust_bridge: "1.80.1"` - Rust 桥接
- `provider: ^6.0.5` - 状态管理
- `window_manager` - 窗口管理（自定义 fork）
- `desktop_multi_window` - 多窗口支持（自定义 fork）
- `texture_rgba_renderer` - 纹理渲染（自定义 fork）
- `xterm: 4.0.0` - 终端模拟器
- `sqflite: 2.2.0` - SQLite 数据库

---

## 七、工作空间 (Workspace)

Cargo workspace 成员：
```
libs/scrap
libs/hbb_common
libs/enigo
libs/clipboard
libs/virtual_display
libs/virtual_display/dylib
libs/portable
libs/remote_printer
```

排除项：
```
vdi/host
examples/custom_plugin
```

---

## 八、关键架构设计

### 8.1 网络架构

1. **会合中介 (Rendezvous Mediator)**
   - P2P 穿透（TCP hole punching）
   - 中继服务器支持
   - NAT 穿越

2. **KCP 协议**
   - 低延迟传输
   - 拥塞控制
   - 重传机制

3. **连接类型**
   - 直接连接（P2P）
   - 中继连接
   - 局域网发现

### 8.2 音视频架构

1. **视频编码**
   - VP8/VP9 (libvpx)
   - AV1 (aom)
   - H.264/H.265 (硬件加速)

2. **音频处理**
   - Opus 编解码
   - 采样率转换 (rubato/samplerate)
   - 回声消除

3. **屏幕捕获**
   - Windows: DXGI, GDI, Mirror Driver
   - macOS: Quartz, ScreenCaptureKit
   - Linux: X11, Wayland (PipeWire)
   - Android: MediaCodec

### 8.3 安全特性

1. **加密**
   - ChaCha20-Poly1305
   - RSA 密钥交换
   - ED25519 签名

2. **认证**
   - 密码保护
   - 双因素认证 (TOTP)
   - 白名单机制

3. **隐私模式**
   - 黑屏模式
   - 输入隐私
   - 虚拟显示器

### 8.4 插件系统

1. **插件类型**
   - 原生插件（Rust）
   - Flutter 插件（Dart）
   - Web 插件

2. **扩展点**
   - Session 生命周期
   - UI 组件
   - 消息处理
   - 工具栏按钮

---

## 九、开发规范

### 9.1 Rust 代码规范

根据 [AGENTS.md](AGENTS.md:1)：

- **禁止使用 `unwrap()` 和 `expect()`**
  - 例外：测试代码
  - 例外：锁获取（poison 处理）
  - 其他情况必须传播错误或显式处理

- **编辑卫生**
  - 不引入仅格式化更改
  - 不运行仓库范围的格式化
  - 保持 diff 仅限于语义更改

### 9.2 构建要求

1. **依赖安装**
   ```bash
   # vcpkg 依赖
   vcpkg install libvpx libyuv opus aom

   # 设置环境变量
   export VCPKG_ROOT=/path/to/vcpkg
   ```

2. **Sciter 库（仅用于遗留 UI）**
   - Windows: `sciter.dll`
   - Linux: `libsciter-gtk.so`
   - macOS: `libsciter.dylib`

3. **编译命令**
   ```bash
   # 调试模式
   cargo run

   # 发布模式
   cargo build --release

   # 带硬件编解码
   cargo build --features hwcodec

   # Flutter 版本
   python3 build.py --flutter
   ```

---

## 十、平台支持矩阵

| 平台 | 桌面 UI | 移动端 | 屏幕捕获 | 输入模拟 | 音频 |
|------|---------|--------|----------|----------|------|
| Windows 10/11 | ✅ Flutter/Sciter | ❌ | ✅ DXGI/GDI | ✅ WinAPI | ✅ WASAPI |
| macOS 10.14+ | ✅ Flutter/Sciter | ❌ | ✅ Quartz/SCK | ✅ CGEvent | ✅ CoreAudio |
| Linux | ✅ Flutter/Sciter | ❌ | ✅ X11/Wayland | ✅ XTest/uinput | ✅ PulseAudio/PipeWire |
| Android | ❌ | ✅ Flutter | ✅ MediaCodec | ✅ InputManager | ✅ AudioRecord |
| iOS | ❌ | ✅ Flutter | ✅ ReplayKit | ✅ UITouch | ✅ AVAudio |
| Web | ✅ Flutter Web | ✅ Flutter Web | ❌ | ❌ | ❌ |

---

## 十一、文件大小统计

### Rust 代码最大文件
1. `src/server/connection.rs` - 232.0 KB
2. `src/client.rs` - 149.2 KB
3. `src/platform/windows.rs` - 142.2 KB
4. `src/common.rs` - 96.9 KB
5. `src/flutter_ffi.rs` - 94.4 KB

### Flutter 代码最大文件
1. `flutter/lib/common/common.dart` - 126.0 KB
2. `flutter/lib/models/model.dart` - 137.0 KB
3. `flutter/lib/desktop/pages/desktop_setting_page.dart` - 100.7 KB
4. `flutter/lib/desktop/widgets/remote_toolbar.dart` - 85.7 KB
5. `flutter/lib/common/widgets/dialog.dart` - 83.4 KB

---

## 十二、CI/CD

### GitHub Actions 工作流
- `.github/workflows/flutter-build.yml` - Flutter 构建
- `.github/workflows/release.yml` - 发布流程
- `.github/workflows/codeql-analysis.yml` - 代码质量分析

### Docker 构建
- `Dockerfile` - 构建环境容器
- `entrypoint.sh` - 容器入口脚本

---

## 十三、常见问题

### Q1: 为什么有两种 UI 框架？
- **Sciter**: 早期版本使用，现已弃用
- **Flutter**: 现代跨平台 UI，推荐使用的版本

### Q2: 如何选择构建特性？
- 桌面版：默认特性 + `flutter`
- 需要硬件加速：添加 `hwcodec`
- Windows VRAM 优化：添加 `vram`
- macOS 最新捕获：添加 `screencapturekit`

### Q3: 如何贡献代码？
1. Fork 仓库
2. 创建特性分支
3. 遵循 Rust 代码规范
4. 提交 PR 并附上测试

---

## 十四、相关链接

- **官方网站**: https://outerd.com
- **GitHub**: https://github.com/outerd/outerd
- **服务器端**: https://github.com/outerd/outerd-server
- **文档**: https://outerd.com/docs
- **Discord**: https://discord.gg/nDceKgxnkV
- **F-Droid**: https://f-droid.org/en/packages/com.carriez.flutter_hbb
- **Flathub**: https://flathub.org/apps/com.outerd.OuterD

---

## 附录：完整文件树

由于项目规模庞大，此处仅展示主要结构。完整文件列表可使用以下命令生成：

```bash
# Rust 代码
find src -type f -name "*.rs" | wc -l

# Flutter 代码
find flutter/lib -type f -name "*.dart" | wc -l

# 总代码行数
tokei
```

预计统计：
- Rust 源文件：约 200+ 个
- Dart 源文件：约 150+ 个
- 总代码行数：约 100,000+ 行

---

*文档生成时间: 2026-04-14*
*项目版本: 1.4.6*
