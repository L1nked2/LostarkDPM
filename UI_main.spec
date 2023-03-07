# -*- mode: python ; coding: utf-8 -*-


block_cipher = None
data_paths = [('./pyqt5/setting_window.ui', '.'), 
      ('./pyqt5/result_window.ui', '.'),
      ('./pyqt5/setting_window_alpha.ui', '.'),
      ('./pyqt5/result_window_alpha.ui', '.'),
      ('./db/characters/*.json', './db/characters'),
      ('./db/skills/*.json', './db/skills'),
      ('./pyqt5/translation_table.json', '.'),
      ('./db/character_settings.json', './db'),
      ('./src/classes/*.py', './src/classes')]

a = Analysis(
    ['UI_main.py'],
    pathex=[],
    binaries=[],
    datas=data_paths,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LostarkDPM',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    icon='C:\\Users\\K\\Desktop\\LostarkDPM\\dist\\favicon.ico',
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
