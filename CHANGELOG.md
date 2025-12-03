# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-12-03

### Added
- **Complete rewrite in Python + Kivy** - Standalone application replacing Lua plugin
- **Native stylus button capture** - Detects side button press automatically via pynput
- **Real overlay window** - Menu appears over Xournal++ without drawing on page
- **Automatic cursor position detection** - Menu appears exactly where cursor is
- **Hover highlighting** - Visual feedback when hovering over menu slices
- **8 color palette** - Central circle with quick color selection
- **10 tools** - Outer ring with essential tools (pen, highlighter, eraser, hand, zoom, navigation)
- **Cross-platform builds** - Automated builds for Linux, Windows, and macOS via GitHub Actions
- **Single executable distribution** - PyInstaller packages everything into one file
- **Installation script** - `INSTALL.sh` for easy setup with virtual environment
- **Comprehensive documentation** - Complete README with usage instructions and troubleshooting

### Changed
- Replaced Lua plugin architecture with standalone Python application
- Menu now uses Kivy for rendering instead of Xournal++ drawing API
- Controls Xournal++ via keyboard automation (pyautogui) instead of plugin API
- Removed dependency on lua-lgi for cursor position detection

### Removed
- Lua plugin (`RadialMenu/`) - Had too many API limitations
- Dependencies on Xournal++ plugin API
- Issues with `addTexts` errors and API restrictions

### Fixed
- Menu position now follows cursor correctly (was fixed position in Lua version)
- No more `addTexts` errors (not using Xournal++ drawing API anymore)
- Stylus button detection works reliably (native capture instead of keyboard mapping)
- Menu doesn't interfere with document (overlay instead of drawing)

### Technical Details
- Built with Python 3.11+
- Uses Kivy 2.3+ for GUI
- pynput for input capture
- pyautogui for Xournal++ control
- GitHub Actions for CI/CD
- PyInstaller for packaging

## [1.0.0] - Previous (Lua Plugin)

### Features (deprecated)
- Lua-based plugin for Xournal++
- 8 colors + 8 tools in radial menu
- Keyboard shortcut activation (Alt+R)
- Basic menu rendering using Xournal++ API

### Issues (resolved in v2.0.0)
- Required lua-lgi for cursor position (not always available)
- Menu drawn permanently on page (not overlay)
- `addTexts` API caused errors
- No native stylus button capture
- Limited customization due to API restrictions

---

## Migration Guide (v1.0 → v2.0)

If you were using the Lua plugin:

1. **Remove old plugin:**
   ```bash
   rm -rf ~/.local/share/xournalpp/plugins/RadialMenu
   ```

2. **Install new Python app:**
   ```bash
   cd xournal-pen
   ./INSTALL.sh
   ```

3. **Run new app:**
   ```bash
   ./run.sh
   ```

4. **Configure stylus button** (optional):
   - The new version detects stylus buttons automatically
   - Alt+R still works as alternative

5. **Enjoy improved functionality!**
   - Menu now appears at cursor position
   - Real overlay (doesn't draw on page)
   - Better performance and reliability
