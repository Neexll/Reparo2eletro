# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['desktop.py'],
    pathex=[],
    binaries=[],
    datas=[('templates', 'templates'), ('static', 'static'), ('database.db', '.'), ('schema.sql', '.')],
    hiddenimports=['flask', 'flask_sqlalchemy', 'openpyxl', 'fpdf', 'matplotlib', 'sqlite3', 'PIL', 'PIL._imaging', 'PIL._imagingcms', 'PIL._imagingft', 'PIL._imagingmath', 'PIL._imagingmorph', 'PIL._imagingtk', 'PIL._webp', 'numpy', 'jinja2', 'markupsafe', 'werkzeug', 'itsdangerous', 'click', 'pyparsing', 'pytz', 'six', 'dateutil', 'dateutil.zoneinfo', 'matplotlib.backends.backend_agg', 'matplotlib.pyplot'],
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
    name='Reparo2Eletro',
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
