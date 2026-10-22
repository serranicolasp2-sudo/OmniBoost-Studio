#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de empaquetado para OmniBoost Studio (Video Booster Ultra):
1. Compila con PyInstaller a modo onedir con ícono oficial.
2. Integra ffmpeg.exe y ffprobe.exe para ejecución 100% offline y standalone.
3. Genera la versión Portable (carpeta lista para usar + archivo .zip).
4. Genera el Instalador .exe con Inno Setup (acceso directo en escritorio, menú inicio y desinstalador).
"""

import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

BASE_DIR = Path(r"C:\Users\Nicolás\Desktop\Proyectos\APPS")
APP_DIR = BASE_DIR / "Video_Booster"
ICONOS_DIR = BASE_DIR / "iconos"
THEME_FILE = BASE_DIR / "ui_theme.py"
ICON_ICO = ICONOS_DIR / "omniboost.ico"

# Herramientas
PYTHON_EXE = BASE_DIR / "Transcriptor" / "entorno" / "Scripts" / "python.exe"
ISCC_EXE = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Inno Setup 6" / "ISCC.exe"
if not ISCC_EXE.exists():
    ISCC_EXE = Path(os.environ.get("ProgramFiles(x86)", "")) / "Inno Setup 6" / "ISCC.exe"

# ffmpeg / ffprobe origen
FFMPEG_SRC = BASE_DIR / "Transcriptor" / "build_instalador" / "bin" / "ffmpeg.exe"
FFPROBE_SRC = BASE_DIR / "Transcriptor" / "build_instalador" / "bin" / "ffprobe.exe"

# Carpetas de salida
OUT_BASE = BASE_DIR / "Instaladores" / "01_Video_Booster"
OUT_PORTABLE_DIR = OUT_BASE / "Portable" / "OmniBoost_Studio_Portable"
OUT_PORTABLE_ZIP = OUT_BASE / "Portable" / "OmniBoost_Studio_Portable.zip"
OUT_INSTALLER_DIR = OUT_BASE / "Instalador"

WORK_DIR = APP_DIR / "build_work"
DIST_DIR = APP_DIR / "build_dist"


def main():
    print("================================================================")
    print("   EMPAQUETADO OFFLINE: OmniBoost Studio (Video Booster Ultra)  ")
    print("================================================================")

    OUT_PORTABLE_DIR.parent.mkdir(parents=True, exist_ok=True)
    OUT_INSTALLER_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Compilación con PyInstaller
    print("\n[1/5] Compilando ejecutable con PyInstaller...")
    cmd_pyinstaller = [
        str(PYTHON_EXE),
        "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--name", "OmniBoost_Studio",
        "--icon", str(ICON_ICO),
        "--add-data", f"{ICONOS_DIR};iconos",
        "--add-data", f"{THEME_FILE};.",
        "--paths", str(BASE_DIR),
        "--distpath", str(DIST_DIR),
        "--workpath", str(WORK_DIR),
        str(APP_DIR / "app_video_booster.py"),
    ]

    res = subprocess.run(cmd_pyinstaller)
    if res.returncode != 0:
        print("ERROR: Falló la compilación de PyInstaller.")
        sys.exit(1)

    built_app_dir = DIST_DIR / "OmniBoost_Studio"
    if not (built_app_dir / "OmniBoost_Studio.exe").exists():
        print("ERROR: No se encontró OmniBoost_Studio.exe compilado.")
        sys.exit(1)

    # 2. Copiar ffmpeg y ffprobe a la carpeta bin/ del ejecutable
    print("\n[2/5] Integrando ffmpeg.exe y ffprobe.exe para soporte offline 100%...")
    bin_target = built_app_dir / "bin"
    bin_target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(FFMPEG_SRC, bin_target / "ffmpeg.exe")
    shutil.copy2(FFPROBE_SRC, bin_target / "ffprobe.exe")
    print("   -> ffmpeg.exe y ffprobe.exe copiados en bin/")

    # 3. Preparar versión Portable
    print("\n[3/5] Creando versión Portable...")
    if OUT_PORTABLE_DIR.exists():
        shutil.rmtree(OUT_PORTABLE_DIR)
    shutil.copytree(built_app_dir, OUT_PORTABLE_DIR)

    # Agregar archivo LEEME_PORTABLE.txt
    leeme_content = """OmniBoost Studio — Versión Portable (100% Offline)
===================================================

• Esta versión NO requiere instalación ni conexión a internet.
• Podés copiar esta carpeta a cualquier pendrive o PC con Windows 10 u 11.
• Para iniciar el programa: hacé doble clic en "OmniBoost_Studio.exe".

Componentes integrados:
- Interfaz gráfica Tu Tiendita IA (Modo Noche Tinta Studio).
- Motor multimedia FFmpeg 9.0 con aceleración NVIDIA RTX (NVENC) y AMD Radeon (AMF).
- Filtros profesionales: CAS (Contrast Adaptive Sharpening), Unsharp, De-banding y HDR.
"""
    with open(OUT_PORTABLE_DIR / "LEEME_PORTABLE.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write(leeme_content)

    print(f"   -> Carpeta portable lista en: {OUT_PORTABLE_DIR}")

    # Comprimir a .zip
    print("   -> Comprimiendo a archivo .zip...")
    if OUT_PORTABLE_ZIP.exists():
        OUT_PORTABLE_ZIP.unlink()

    with zipfile.ZipFile(OUT_PORTABLE_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(OUT_PORTABLE_DIR):
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(OUT_PORTABLE_DIR.parent)
                zf.write(file_path, rel_path)

    print(f"   -> Archivo zip creado: {OUT_PORTABLE_ZIP} ({OUT_PORTABLE_ZIP.stat().st_size / (1024*1024):.1f} MB)")

    # 4. Crear script de Inno Setup y compilar instalador
    print("\n[4/5] Creando instalador .exe con Inno Setup...")
    iss_path = APP_DIR / "OmniBoost_Setup.iss"
    iss_content = f"""; Script de instalación para OmniBoost Studio
#define AppName "OmniBoost Studio"
#define AppVersion "1.0"
#define AppPublisher "Tu Tiendita IA"
#define AppExeName "OmniBoost_Studio.exe"
#define SourceDir "{OUT_PORTABLE_DIR}"
#define IconFile "{ICON_ICO}"
#define OutDir "{OUT_INSTALLER_DIR}"

[Setup]
AppId={{{{9B7C1A20-4E5F-4D8B-8A1C-7F2E3D4C5B6A}}}}
AppName={{#AppName}}
AppVersion={{#AppVersion}}
AppPublisher={{#AppPublisher}}
DefaultDirName={{localappdata}}\\Programs\\{{#AppName}}
DefaultGroupName={{#AppName}}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir={{#OutDir}}
OutputBaseFilename=OmniBoost_Studio_Instalador_{{#AppVersion}}
SetupIconFile={{#IconFile}}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={{app}}\\{{#AppExeName}}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"

[Files]
Source: "{{#SourceDir}}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\{{#AppName}}"; Filename: "{{app}}\\{{#AppExeName}}"
Name: "{{group}}\\{{cm:UninstallProgram,{{#AppName}}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\{{#AppName}}"; Filename: "{{app}}\\{{#AppExeName}}"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\{{#AppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(AppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent
"""
    with open(iss_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(iss_content)

    res_iscc = subprocess.run([str(ISCC_EXE), str(iss_path)])
    if res_iscc.returncode != 0:
        print("ERROR: Falló la compilación de Inno Setup.")
        sys.exit(1)

    installer_file = OUT_INSTALLER_DIR / "OmniBoost_Studio_Instalador_1.0.exe"
    print(f"   -> Instalador generado: {installer_file} ({installer_file.stat().st_size / (1024*1024):.1f} MB)")

    # 5. Limpieza de temporales
    print("\n[5/5] Limpiando archivos temporales de compilación...")
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    if iss_path.exists():
        iss_path.unlink()

    print("\n================================================================")
    print("   ¡COMPILACIÓN EXITOSA DE OMNIBOOST STUDIO!                    ")
    print(f"   1. Instalador .exe: {installer_file}")
    print(f"   2. Carpeta Portable: {OUT_PORTABLE_DIR}")
    print(f"   3. Portable .zip:   {OUT_PORTABLE_ZIP}")
    print("================================================================")


if __name__ == "__main__":
    main()
