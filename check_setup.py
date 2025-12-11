"""
Script para verificar que todos los archivos y configuraciones estén correctos
Ejecutar: python check_setup.py
"""

import os
import sys

def check_files():
    """Verifica que todos los archivos necesarios existan"""
    required_files = [
        'main.py',
        'requirements.txt',
        'render.yaml',
        '.gitignore',
        'init_db.py',
        'README.md',
        'static/css/style.css',
        'static/js/dashboard.js',
        'templates/index.html',
        'templates/login.html',
        'templates/forgot_password.html',
        'templates/reset_password.html',
        'templates/dashboard.html'
    ]
    
    print("\n=== Verificando Archivos ===\n")
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - FALTA")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠ Faltan {len(missing_files)} archivo(s)")
        return False
    else:
        print("\n✓ Todos los archivos están presentes")
        return True

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("\n=== Verificando Dependencias ===\n")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'passlib',
        'jose',
        'pydantic',
        'jinja2'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NO INSTALADO")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠ Faltan {len(missing_packages)} paquete(s)")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ Todas las dependencias están instaladas")
        return True

def check_structure():
    """Verifica la estructura de directorios"""
    print("\n=== Verificando Estructura ===\n")
    
    required_dirs = [
        'static',
        'static/css',
        'static/js',
        'templates'
    ]
    
    missing_dirs = []
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"✓ {directory}/")
        else:
            print(f"✗ {directory}/ - FALTA")
            missing_dirs.append(directory)
    
    if missing_dirs:
        print(f"\n⚠ Faltan {len(missing_dirs)} directorio(s)")
        print("Crea los directorios faltantes:")
        for d in missing_dirs:
            print(f"  mkdir -p {d}")
        return False
    else:
        print("\n✓ Estructura de directorios correcta")
        return True

def check_env():
    """Verifica las variables de entorno"""
    print("\n=== Verificando Configuración ===\n")
    
    env_vars = [
        'SECRET_KEY',
        'SMTP_SERVER',
        'SMTP_PORT',
        'SMTP_USER',
        'SMTP_PASSWORD',
        'BASE_URL'
    ]
    
    missing_vars = []
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if var == 'SMTP_PASSWORD':
                print(f"✓ {var} = ****")
            else:
                print(f"✓ {var} = {value}")
        else:
            print(f"⚠ {var} - NO CONFIGURADO (se usará valor por defecto)")
            missing_vars.append(var)
    
    if missing_vars:
        print("\nNota: Puedes configurar estas variables en un archivo .env")
        print("Copia .env.example a .env y edita los valores")
        return True  # No es crítico en desarrollo
    else:
        print("\n✓ Todas las variables de entorno configuradas")
        return True

def main():
    """Ejecuta todas las verificaciones"""
    print("\n" + "="*60)
    print("  El Rincón de la Sole - Verificación de Setup")
    print("="*60)
    
    files_ok = check_files()
    structure_ok = check_structure()
    deps_ok = check_dependencies()
    env_ok = check_env()
    
    print("\n" + "="*60)
    
    if files_ok and structure_ok and deps_ok and env_ok:
        print("\n✓ ¡Todo está listo! Puedes ejecutar:")
        print("\n  1. Crear usuario admin:")
        print("     python init_db.py")
        print("\n  2. Iniciar la aplicación:")
        print("     uvicorn main:app --reload")
        print("\n  3. Abrir en el navegador:")
        print("     http://localhost:8000")
    else:
        print("\n⚠ Hay problemas que resolver antes de continuar")
        print("Revisa los mensajes arriba para más detalles")
        sys.exit(1)
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()