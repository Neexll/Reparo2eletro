# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Lista de arquivos e pastas a serem incluídos
added_files = [
    ('templates', 'templates'),
    ('static', 'static'),
    ('database.db', '.') if os.path.exists('database.db') else None,
    ('schema.sql', '.') if os.path.exists('schema.sql') else None
]
# Remove entradas None (caso o arquivo de banco de dados não exista)
added_files = [x for x in added_files if x is not None]

a = Analysis(
    ['desktop.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'flask',
        'flask_sqlalchemy',
        'openpyxl',
        'fpdf',
        'matplotlib',
        'sqlite3',
        'PIL',
        'PIL._imaging',
        'PIL._imagingcms',
        'PIL._imagingft',
        'PIL._imagingmath',
        'PIL._imagingmorph',
        'PIL._imagingtk',
        'PIL._webp',
        'numpy',
        'scipy',
        'scipy.integrate',
        'scipy.special',
        'scipy.spatial',
        'scipy.spatial.transform',
        'jinja2',
        'markupsafe',
        'werkzeug',
        'itsdangerous',
        'click',
        'pyparsing',
        'pytz',
        'six',
        'dateutil',
        'dateutil.zoneinfo',
        'matplotlib.backends.backend_qt5agg',
        'matplotlib.backends.backend_agg',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.backends.backend_webagg',
        'matplotlib.pyplot',
    ],
    hooksparams=None,
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
    name='Reparo2Eletro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)

# Adiciona os arquivos de dados adicionais
for src, dest in added_files:
    if os.path.isdir(src):
        for root, dirs, files in os.walk(src):
            for file in files:
                src_path = os.path.join(root, file)
                dest_path = os.path.join('templates' if 'templates' in root else 'static', os.path.relpath(root, src), file)
                exe.datas.append((src_path, os.path.dirname(dest_path)))
    else:
        exe.datas.append((src, os.path.dirname(dest) if os.path.dirname(dest) else '.'))
