# -*- mode: python ; coding: utf-8 -*-
import shutil
import os

block_cipher = None


app_standalone = Analysis(
    ['src\\app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

app_pkg = Analysis(
    ['src\\app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# app_cli = Analysis(
#     ['src\\cli.py'],
#     pathex=[],
#     binaries=[],
#     datas=[],
#     hiddenimports=[],
#     runtime_hooks=[],
#     excludes=[],
#     win_no_prefer_redirects=False,
#     win_private_assemblies=False,
#     cipher=block_cipher,
#     noarchive=False,
# )

app_standalone_pyz = PYZ(app_standalone.pure, app_standalone.zipped_data, cipher=block_cipher)
app_pkg_pyz = PYZ(app_pkg.pure, app_pkg.zipped_data, cipher=block_cipher)
# app_cli_pyz = PYZ(app_cli.pure, app_cli.zipped_data, cipher=block_cipher)

app_standalone_exe = EXE(
    app_standalone_pyz,
    app_standalone.scripts,
    app_standalone.binaries,
    app_standalone.zipfiles,
    app_standalone.datas,
    [],
    name='app_standalone',
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

app_pkg_exe = EXE(
    app_pkg_pyz,
    app_pkg.scripts,
    [],
    exclude_binaries=True,
    name='app_pkg',
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
)

# app_cli_exe = EXE(
#     app_cli_pyz,
#     app_cli.scripts,
#     app_cli.binaries,
#     app_cli.zipfiles,
#     app_cli.datas,
#     [],
#     name='app_cli',
#     debug=False,
#     bootloader_ignore_signals=False,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     runtime_tmpdir=None,
#     console=True,
#     disable_windowed_traceback=False,
#     argv_emulation=False,
#     target_arch=None,
#     codesign_identity=None,
#     entitlements_file=None,
# )

coll = COLLECT(
    app_pkg_exe,
    app_pkg.binaries,
    app_pkg.zipfiles,
    app_pkg.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app_pkg'

)

if not os.path.exists ('./dist/bin'):
    os.mkdir ('./dist/bin')

shutil.copyfile ('./src/app.ini', f'{DISTPATH}/bin/app.ini')
shutil.copyfile ('./src/app.ini', f'{DISTPATH}/app_pkg/app.ini')
shutil.copyfile (f'{DISTPATH}/app_standalone.exe', f'{DISTPATH}/bin/app_standalone.exe')
shutil.make_archive (f'{DISTPATH}/app_pkg', 'zip', f'{DISTPATH}/app_pkg')
shutil.make_archive (f'{DISTPATH}/app_bin', 'zip', f'{DISTPATH}/bin')

