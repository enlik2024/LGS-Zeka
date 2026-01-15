"""
LGS-Zeka Platform - Kurulum Doğrulama Scripti
Bu script, projenin doğru şekilde kurulup kurulmadığını kontrol eder.
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Renkli çıktı için ANSI kodları
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Başlık yazdırır."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")


def print_success(text: str):
    """Başarı mesajı yazdırır."""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text: str):
    """Hata mesajı yazdırır."""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_warning(text: str):
    """Uyarı mesajı yazdırır."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def check_python_version() -> bool:
    """Python versiyonunu kontrol eder."""
    print_header("Python Versiyonu Kontrolü")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 9:
        print_success(f"Python versiyonu: {version_str} ✓")
        return True
    else:
        print_error(f"Python versiyonu: {version_str}")
        print_error("Python 3.9 veya üzeri gereklidir!")
        return False


def check_required_packages() -> Tuple[bool, List[str]]:
    """Gerekli paketleri kontrol eder."""
    print_header("Paket Kontrolü")
    
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'google.generativeai',
        'streamlit_option_menu',
        'gspread',
        'oauth2client',
        'supabase',
        'PIL'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'google.generativeai':
                __import__('google.generativeai')
                package_name = 'google-generativeai'
            elif package == 'PIL':
                __import__('PIL')
                package_name = 'Pillow'
            else:
                __import__(package)
                package_name = package
            
            print_success(f"{package_name} yüklü")
        except ImportError:
            print_error(f"{package_name} eksik!")
            missing_packages.append(package_name)
    
    return len(missing_packages) == 0, missing_packages


def check_file_structure() -> bool:
    """Dosya yapısını kontrol eder."""
    print_header("Dosya Yapısı Kontrolü")
    
    root = Path(__file__).parent
    
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'PROJECT_ROADMAP.md',
        '.gitignore',
        '.streamlit/config.toml',
        '.streamlit/secrets.toml.example',
        'utils/__init__.py',
        'utils/db_manager.py',
        'pages/__init__.py',
    ]
    
    required_dirs = [
        'utils',
        'pages',
        'assets',
        '.streamlit'
    ]
    
    all_ok = True
    
    # Dizinleri kontrol et
    for dir_name in required_dirs:
        dir_path = root / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print_success(f"Dizin mevcut: {dir_name}/")
        else:
            print_error(f"Dizin eksik: {dir_name}/")
            all_ok = False
    
    # Dosyaları kontrol et
    for file_name in required_files:
        file_path = root / file_name
        if file_path.exists() and file_path.is_file():
            print_success(f"Dosya mevcut: {file_name}")
        else:
            print_error(f"Dosya eksik: {file_name}")
            all_ok = False
    
    return all_ok


def check_secrets_file() -> bool:
    """Secrets dosyasını kontrol eder."""
    print_header("Secrets Yapılandırması Kontrolü")
    
    root = Path(__file__).parent
    secrets_path = root / '.streamlit' / 'secrets.toml'
    example_path = root / '.streamlit' / 'secrets.toml.example'
    
    if not example_path.exists():
        print_error("secrets.toml.example dosyası bulunamadı!")
        return False
    else:
        print_success("secrets.toml.example dosyası mevcut")
    
    if not secrets_path.exists():
        print_warning("secrets.toml dosyası bulunamadı!")
        print_warning("Lütfen secrets.toml.example dosyasını kopyalayıp düzenleyin:")
        print(f"  {Colors.YELLOW}cp .streamlit/secrets.toml.example .streamlit/secrets.toml{Colors.RESET}")
        return False
    else:
        print_success("secrets.toml dosyası mevcut")
        
        # İçeriği kontrol et
        try:
            import tomli
            with open(secrets_path, 'rb') as f:
                secrets = tomli.load(f)
            
            required_keys = ['gcp_service_account', 'gemini', 'spreadsheet_key']
            for key in required_keys:
                if key in secrets:
                    print_success(f"  {key} yapılandırılmış")
                else:
                    print_warning(f"  {key} eksik!")
        except ImportError:
            print_warning("tomli paketi yüklü değil, secrets içeriği kontrol edilemedi")
        except Exception as e:
            print_warning(f"secrets.toml okunamadı: {str(e)}")
        
        return True


def check_imports() -> bool:
    """Kritik import'ları test eder."""
    print_header("Import Testleri")
    
    all_ok = True
    
    # utils.db_manager
    try:
        from utils.db_manager import DatabaseManager, get_db_manager
        print_success("utils.db_manager import edildi")
    except Exception as e:
        print_error(f"utils.db_manager import hatası: {str(e)}")
        all_ok = False
    
    # Streamlit
    try:
        import streamlit as st
        print_success("streamlit import edildi")
    except Exception as e:
        print_error(f"streamlit import hatası: {str(e)}")
        all_ok = False
    
    # Plotly
    try:
        import plotly.express as px
        print_success("plotly import edildi")
    except Exception as e:
        print_error(f"plotly import hatası: {str(e)}")
        all_ok = False
    
    return all_ok


def print_summary(results: dict):
    """Özet rapor yazdırır."""
    print_header("Kurulum Özeti")
    
    total_checks = len(results)
    passed_checks = sum(1 for v in results.values() if v)
    
    print(f"Toplam Kontrol: {total_checks}")
    print(f"Başarılı: {Colors.GREEN}{passed_checks}{Colors.RESET}")
    print(f"Başarısız: {Colors.RED}{total_checks - passed_checks}{Colors.RESET}")
    
    print("\n" + "="*60)
    
    if all(results.values()):
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Tüm kontroller başarılı!{Colors.RESET}")
        print(f"\n{Colors.GREEN}Projeyi çalıştırmak için:{Colors.RESET}")
        print(f"  {Colors.BLUE}streamlit run app.py{Colors.RESET}\n")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Bazı kontroller başarısız!{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Lütfen yukarıdaki hataları düzeltin.{Colors.RESET}\n")
        
        # Eksik paketler varsa kurulum komutu göster
        if 'packages' in results and not results['packages']:
            print(f"{Colors.YELLOW}Eksik paketleri yüklemek için:{Colors.RESET}")
            print(f"  {Colors.BLUE}pip install -r requirements.txt{Colors.RESET}\n")


def main():
    """Ana kontrol fonksiyonu."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         LGS-Zeka Platform - Kurulum Kontrolü              ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    results = {}
    
    # Kontrolleri çalıştır
    results['python'] = check_python_version()
    
    packages_ok, missing = check_required_packages()
    results['packages'] = packages_ok
    
    results['files'] = check_file_structure()
    results['secrets'] = check_secrets_file()
    results['imports'] = check_imports()
    
    # Özet rapor
    print_summary(results)
    
    # Exit code
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()
