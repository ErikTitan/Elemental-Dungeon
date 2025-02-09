from PyInstaller.__main__ import run
import os
import sys
import shutil
from datetime import datetime

def create_build_dirs():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build", f"build_{timestamp}")
    exe_dir = os.path.join(build_dir, "elemental_dungeon")
    work_dir = os.path.join(build_dir, "work")
    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(exe_dir, exist_ok=True)
    os.makedirs(work_dir, exist_ok=True)
    return build_dir, exe_dir, work_dir

def copy_assets(exe_dir):
    asset_directories = [
        "assets/map",
        "assets/decorations",
        "assets/audio",
        "assets/HUD",
        "assets/boss",
        "assets/projectiles",
        "assets/characters"
    ]

    for asset_dir in asset_directories:
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)), asset_dir)
        dst = os.path.join(exe_dir, asset_dir)
        if os.path.exists(src):
            print(f"Copying {asset_dir} to {dst}...")
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            print(f"Warning: {asset_dir} directory not found!")

def clean_pyinstaller_artifacts():
    paths_to_clean = ['__pycache__', '*.spec']
    for pattern in paths_to_clean:
        files = [f for f in os.listdir('.') if f.endswith(pattern.replace('*', ''))]
        for f in files:
            try:
                if os.path.isdir(f):
                    shutil.rmtree(f)
                else:
                    os.remove(f)
            except Exception as e:
                print(f"Warning: Could not remove {f}: {e}")

def build_executable():
    build_dir, exe_dir, work_dir = create_build_dirs()
    print(f"Created build directory: {build_dir}")

    project_root = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(project_root, "game.py")

    hidden_imports = [
        'pygame',
        'player',
        'enemy',
        'projectile',
        'game_settings'
    ]

    pyi_args = [
        main_file,
        "--onefile",
        "--noconsole",
        "--clean",
        "--name", "ElementalDungeon",
        "--distpath", exe_dir,
        "--workpath", work_dir,
        "--specpath", build_dir,
        "--add-data", f"{project_root}/assets;assets",
    ]

    for imp in hidden_imports:
        pyi_args.extend(["--hidden-import", imp])

    try:
        run(pyi_args)
        copy_assets(exe_dir)
        clean_pyinstaller_artifacts()
        print(f"\nBuild completed successfully!")
        print(f"Build directory: {build_dir}")
        print("Contents:")
        print(f"  - elemental_dungeon/")
        for item in os.listdir(exe_dir):
            print(f"    - {item}")
        print(f"  - work/")
        print(f"  - ElementalDungeon.spec")
    except Exception as e:
        print(f"Error during build: {e}")
        raise

if __name__ == "__main__":
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        os.system(f"{sys.executable} -m pip install pyinstaller")
    build_executable()