"""
Script de inicialización para crear el primer usuario administrador
Ejecutar: python init_db.py
"""

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from getpass import getpass

# Importar modelos
SQLALCHEMY_DATABASE_URL = "sqlite:///./el_rincon_de_la_sole.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Importar el modelo User desde main
try:
    from main import Base, User
    Base.metadata.create_all(bind=engine)
except ImportError:
    print("Error: Asegúrate de que main.py esté en el mismo directorio")
    sys.exit(1)

def create_admin_user():
    """Crea un usuario administrador"""
    db = SessionLocal()
    
    try:
        print("\n=== Crear Usuario Administrador ===\n")
        
        username = input("Nombre de usuario: ").strip()
        if not username:
            print("Error: El nombre de usuario no puede estar vacío")
            return
        
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"Error: El usuario '{username}' ya existe")
            return
        
        email = input("Email: ").strip()
        if not email or '@' not in email:
            print("Error: Email inválido")
            return
        
        # Verificar si el email ya existe
        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            print(f"Error: El email '{email}' ya está registrado")
            return
        
        password = getpass("Contraseña: ")
        password_confirm = getpass("Confirmar contraseña: ")
        
        if password != password_confirm:
            print("Error: Las contraseñas no coinciden")
            return
        
        if len(password) < 6:
            print("Error: La contraseña debe tener al menos 6 caracteres")
            return
        
        # Crear usuario
        hashed_password = pwd_context.hash(password)
        new_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        
        print(f"\n✓ Usuario '{username}' creado exitosamente!")
        print(f"  Email: {email}")
        print(f"\nPuedes iniciar sesión en: http://localhost:8000/login")
        
    except Exception as e:
        print(f"\nError al crear usuario: {e}")
        db.rollback()
    finally:
        db.close()

def list_users():
    """Lista todos los usuarios"""
    db = SessionLocal()
    
    try:
        users = db.query(User).all()
        
        if not users:
            print("\nNo hay usuarios registrados")
            return
        
        print("\n=== Usuarios Registrados ===\n")
        for user in users:
            print(f"ID: {user.id}")
            print(f"Usuario: {user.username}")
            print(f"Email: {user.email}")
            print("-" * 40)
        
    except Exception as e:
        print(f"\nError al listar usuarios: {e}")
    finally:
        db.close()

def main():
    """Menú principal"""
    print("\n" + "="*50)
    print("  El Rincón de la Sole - Inicialización")
    print("="*50)
    
    while True:
        print("\nOpciones:")
        print("1. Crear usuario administrador")
        print("2. Listar usuarios")
        print("3. Salir")
        
        choice = input("\nSelecciona una opción (1-3): ").strip()
        
        if choice == "1":
            create_admin_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            print("\n¡Hasta luego!")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()