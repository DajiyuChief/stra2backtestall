# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['Strategy2.py','back.py','backtest_all.py','baseFun.py','buyandsellui.py','customer.py','gol_all.py','Holder.py','kline.py','load_csvdata.py','Main.py','MessageBox.py','setting.py','stockinfo.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['talib.stream'],
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
    [],
    exclude_binaries=True,
    name='Strategy2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon='stock.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Strategy2',
)