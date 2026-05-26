# test_env_config.py
from app.core.config import settings
from sqlalchemy import create_engine, text

def test_config():
    print("=" * 60)
    print("VÉRIFICATION CONFIGURATION")
    print("=" * 60)
    
    print(f"\n📦 Application: {settings.PROJECT_NAME}")
    print(f"🗄️ Database: {settings.DATABASE_URL.split('@')[1]}")  # Cache le mot de passe
    print(f"📁 Upload dir: {settings.UPLOAD_DIR}")
    print(f"💾 Max file size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB")
    
    # Test connexion
    print(f"\n🔌 Test connexion à PostgreSQL...")
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database(), version()"))
            db_name, version = result.fetchone()
            print(f"  ✅ Base: {db_name}")
            print(f"  ✅ Version: {version.split(',')[0]}")
            
            # Vérifier les tables existantes
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema='public'
            """))
            count = result.scalar()
            print(f"  📋 Tables existantes: {count}")
            
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_config()
