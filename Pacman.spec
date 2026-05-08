# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pacman_chasing.py'],
    pathex=[],
    binaries=[],
    datas=[('pacman.png', '.'), ('ghost.png', '.'), ('wall.png', '.'), ('food.png', '.'), ('red_ball.jpg', '.'), ('ghost(2).jpg', '.'), ('map2.txt', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Pacman',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
