# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:\\MyProjectLocation\\MARCCrucible-CommandLineTool.py'],
             pathex=[r'C:\Program Files (x86)\Windows Kits\10\Redist\10.0.22000.0\ucrt\DLLs\x64'],
             binaries=[],
             datas=[('my_icon_x.ico', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='MARC Crucible',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='my_icon_x.ico')
