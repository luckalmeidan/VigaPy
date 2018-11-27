# -*- mode: python -*-

block_cipher = None



a = Analysis(['../vigapy/beam_ui.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='VigaPy',
          debug=False,
          strip=False,
          upx=True,
          console=True,
          icon='C:\\Users\Lucas\\PycharmProjects\\BeamProject\\vigapy\\imgs\\beampy_icon2.ico'
           )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='VigaPy')
