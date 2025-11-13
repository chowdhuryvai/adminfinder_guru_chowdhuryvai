import requests
from threading import Thread
import queue
import argparse
from pathlib import Path
import sys
import signal
from urllib.parse import urljoin
import os
import time

# Try to import colorama for cross-platform colored text
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Define basic color constants if colorama is not available
    class Fore:
        RED = ''
        GREEN = ''
        YELLOW = ''
        BLUE = ''
        MAGENTA = ''
        CYAN = ''
        WHITE = ''
        RESET = ''
    
    class Back:
        RED = ''
        GREEN = ''
        YELLOW = ''
        BLUE = ''
        MAGENTA = ''
        CYAN = ''
        WHITE = ''
        RESET = ''
    
    class Style:
        BRIGHT = ''
        RESET_ALL = ''

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOOL_VERSION = "1.0"
DEVELOPER = "Chowdhuryvai"

def color_text(text, color, style=""):
    """Apply colors to text if colorama is available"""
    if COLORAMA_AVAILABLE:
        return f"{style}{color}{text}{Style.RESET_ALL}"
    return text

def handle_interrupt(signal, frame):
    print(f"\n{color_text('[INFO]', Fore.YELLOW)} Scan interrupted by user. Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_interrupt)

def check_internet_connection():
    """Check if there's an active internet connection."""
    try:
        requests.get("https://www.google.com", timeout=5)
        print(f"{color_text('[SUCCESS]', Fore.GREEN)} Internet connection verified.")
        return True
    except requests.ConnectionError:
        print(f"{color_text('[ERROR]', Fore.RED)} No internet connection. Please check your connection and try again.")
        return False

def print_banner():
    """Print the main banner with colors and styling"""
    banner = rf"""{color_text(r"""
 ██████╗██╗  ██╗ ██████╗ ██╗    ██╗██╗   ██╗██████╗ ██████╗ ██╗   ██╗██╗   ██╗ █████╗ ██╗
██╔════╝██║  ██║██╔═══██╗██║    ██║██║   ██║██╔══██╗██╔══██╗╚██╗ ██╔╝██║   ██║██╔══██╗██║
██║     ███████║██║   ██║██║ █╗ ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ ██║   ██║███████║██║
██║     ██╔══██║██║   ██║██║███╗██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██║   ██║██╔══██║██║
╚██████╗██║  ██║╚██████╔╝╚███╔███╔╝╚██████╔╝██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║███████╗
 ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝
""", Fore.CYAN, Style.BRIGHT)}"""
    print(banner)
    
    print(color_text(f"╔{'═' * 58}╗", Fore.MAGENTA))
    print(color_text(f"║ {f'Admin Panel Finder v{TOOL_VERSION}':^56} ║", Fore.MAGENTA))
    print(color_text(f"╚{'═' * 58}╝", Fore.MAGENTA))
    
    # Hacked by text with glowing effect
    hacked_text = r"""
 _   _            _             _ ____            _                                 
| | | | __ _  ___| | _____     | | __ )  __ _ _ __| | __   _   _ _   _ _ __ ___   __ _ 
| |_| |/ _` |/ __| |/ / __|_   | |  _ \ / _` | '__| |/ /  | | | | | | | '_ ` _ \ / _` |
|  _  | (_| | (__|   <\__ \ |__| | |_) | (_| | |  |   <   | |_| | |_| | | | | | | (_| |
|_| |_|\__,_|\___|_|\_\___/\____/|____/ \__,_|_|  |_|\_\   \__, |\__,_|_| |_| |_|\__,_|
                                                           |___/                      
    """
    print(color_text(hacked_text, Fore.RED, Style.BRIGHT))
    print(color_text(f"✨ Developer: {DEVELOPER} ✨", Fore.YELLOW, Style.BRIGHT))
    
    print(color_text(f"\n{'═' * 60}", Fore.CYAN))
    print(color_text("📞 Contact Information:", Fore.GREEN, Style.BRIGHT))
    print(color_text(f"{'═' * 60}", Fore.CYAN))
    print(color_text("📱 Telegram ID: ", Fore.WHITE) + color_text("https://t.me/darkvaiadmin", Fore.CYAN))
    print(color_text("📢 Telegram Channel: ", Fore.WHITE) + color_text("https://t.me/windowspremiumkey", Fore.CYAN))
    print(color_text("🌐 Website: ", Fore.WHITE) + color_text("https://crackyworld.com/", Fore.CYAN))
    print(color_text(f"{'═' * 60}", Fore.CYAN))

def load_admin_paths(filepath="wordlist/admin_paths.txt"):
    """Load admin paths from a file."""
    if not Path(filepath).exists():
        raise FileNotFoundError(f"{color_text('[ERROR]', Fore.RED)} Admin paths file not found: {filepath}")
    
    with open(filepath, "r") as f:
        paths = [line.strip() for line in f if line.strip()]
    
    print(f"{color_text('[INFO]', Fore.BLUE)} Loaded {color_text(len(paths), Fore.YELLOW)} paths from wordlist")
    return paths

def scan_url(target_url, path_queue, results, timeout=5):
    """Scan a single URL."""
    while not path_queue.empty():
        path = path_queue.get()
        url = urljoin(target_url, path)
        try:
            response = requests.get(url, timeout=timeout, allow_redirects=True, verify=False)
            status_code = response.status_code
            page_content = response.text.lower()

            if status_code in [200, 301, 302] and ("admin" in page_content or "login" in page_content):
                result_text = f"🎯 [FOUND] Admin panel: {url} (Status: {status_code})"
                print(color_text(result_text, Fore.GREEN, Style.BRIGHT))
                results.append((url, status_code))
            else:
                print(f"{color_text('[SCANNING]', Fore.BLUE)} Testing: {url}")
        except requests.RequestException:
            print(f"{color_text('[ERROR]', Fore.RED)} Could not access: {url}")
        finally:
            path_queue.task_done()

def admin_finder(target, threads, paths_file, output_file):
    """Main admin panel finder function."""
    print(f"\n{color_text('🎯 [INFO]', Fore.CYAN)} Starting admin panel scan on: {color_text(target, Fore.YELLOW)}")
    print(f"{color_text('🔧 [INFO]', Fore.CYAN)} Threads: {color_text(threads, Fore.YELLOW)}")
    print(f"{color_text('📁 [INFO]', Fore.CYAN)} Wordlist: {color_text(paths_file, Fore.YELLOW)}")
    
    admin_paths = load_admin_paths(paths_file)
    path_queue = queue.Queue()

    for path in admin_paths:
        path_queue.put(path)

    results = []
    thread_list = []

    output_dir = Path(output_file).parent
    if not output_dir.exists():
        print(f"{color_text('[INFO]', Fore.BLUE)} Creating directory: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{color_text('🚀 [INFO]', Fore.CYAN, Style.BRIGHT)} Starting scan with {color_text(threads, Fore.YELLOW)} threads...")
    print(f"{color_text('⏳ [INFO]', Fore.BLUE)} Please wait while scanning...")
    
    start_time = time.time()
    
    for _ in range(threads):
        thread = Thread(target=scan_url, args=(target, path_queue, results))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()
    
    end_time = time.time()
    scan_duration = end_time - start_time

    print(f"\n{color_text('📊 [STATS]', Fore.MAGENTA)} Scan completed in {color_text(f'{scan_duration:.2f} seconds', Fore.YELLOW)}")

    if results:
        print(f"\n{color_text('🎉 [RESULTS]', Fore.GREEN, Style.BRIGHT)} Found {color_text(len(results), Fore.YELLOW)} admin panels:")
        print(color_text("─" * 80, Fore.CYAN))
        for i, (url, status_code) in enumerate(results, 1):
            status_color = Fore.GREEN if status_code == 200 else Fore.YELLOW
            print(f"{color_text(f'{i:2d}.', Fore.WHITE)} {color_text('🔗', Fore.CYAN)} {url}")
            print(f"    {color_text('Status:', Fore.WHITE)} {color_text(status_code, status_color)}")
        
        with open(output_file, "w") as f:
            for url, status_code in results:
                f.write(f"{url} | Status: {status_code}\n")
        
        print(color_text("─" * 80, Fore.CYAN))
        print(f"{color_text('💾 [INFO]', Fore.BLUE)} Results saved to: {color_text(output_file, Fore.YELLOW)}")
    else:
        print(f"\n{color_text('😞 [INFO]', Fore.YELLOW)} No admin panels found.")

def main_menu():
    """Display main menu and get user input."""
    print(f"\n{color_text('╔' + '═' * 58 + '╗', Fore.MAGENTA)}")
    print(f"{color_text('║' + f'{Fore.CYAN}🏠 ADMIN PANEL FINDER - MAIN MENU{Fore.MAGENTA}'.center(58) + '║', Fore.MAGENTA)}")
    print(f"{color_text('╚' + '═' * 58 + '╝', Fore.MAGENTA)}")
    
    menu_items = [
        f"{color_text('1.', Fore.GREEN)} {color_text('🎯 Start Scan', Fore.CYAN)}",
        f"{color_text('2.', Fore.GREEN)} {color_text('ℹ️  About Tool', Fore.CYAN)}",
        f"{color_text('3.', Fore.GREEN)} {color_text('📞 Contact Info', Fore.CYAN)}",
        f"{color_text('4.', Fore.GREEN)} {color_text('🚪 Exit', Fore.CYAN)}"
    ]
    
    for item in menu_items:
        print(f"   {item}")
    
    print(f"{color_text('─' * 60, Fore.MAGENTA)}")
    
    while True:
        try:
            choice = input(f"\n{color_text('📝', Fore.YELLOW)} Enter your choice {color_text('(1-4)', Fore.GREEN)}: ").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            else:
                print(f"{color_text('❌', Fore.RED)} Invalid choice! Please enter 1, 2, 3, or 4.")
        except KeyboardInterrupt:
            print(f"\n\n{color_text('👋', Fore.YELLOW)} Goodbye!")
            sys.exit(0)

def get_scan_parameters():
    """Get scan parameters from user."""
    print(f"\n{color_text('╔' + '═' * 58 + '╗', Fore.BLUE)}")
    print(f"{color_text('║' + f'{Fore.CYAN}⚙️  SCAN CONFIGURATION{Fore.BLUE}'.center(58) + '║', Fore.BLUE)}")
    print(f"{color_text('╚' + '═' * 58 + '╝', Fore.BLUE)}")
    
    # Target URL
    while True:
        target = input(f"{color_text('🎯', Fore.YELLOW)} Enter target URL {color_text('(e.g., https://example.com)', Fore.WHITE)}: ").strip()
        if target.startswith(('http://', 'https://')):
            break
        else:
            print(f"{color_text('❌', Fore.RED)} Please enter a valid URL with http:// or https://")
    
    # Threads
    while True:
        try:
            threads = input(f"{color_text('🔧', Fore.YELLOW)} Enter number of threads {color_text('(default 10)', Fore.WHITE)}: ").strip()
            if not threads:
                threads = 10
                break
            threads = int(threads)
            if 1 <= threads <= 50:
                break
            else:
                print(f"{color_text('❌', Fore.RED)} Please enter a number between 1 and 50")
        except ValueError:
            print(f"{color_text('❌', Fore.RED)} Please enter a valid number")
    
    # Wordlist file
    while True:
        paths_file = input(f"{color_text('📁', Fore.YELLOW)} Enter path to wordlist file {color_text('(default: wordlist/admin_paths.txt)', Fore.WHITE)}: ").strip()
        if not paths_file:
            paths_file = "wordlist/admin_paths.txt"
        
        if Path(paths_file).exists():
            break
        else:
            print(f"{color_text('❌', Fore.RED)} File not found: {paths_file}")
            create_default = input(f"{color_text('❓', Fore.YELLOW)} Create default wordlist file? {color_text('(y/n)', Fore.WHITE)}: ").strip().lower()
            if create_default == 'y':
                create_default_wordlist()
                break
            else:
                print(f"{color_text('⚠️', Fore.YELLOW)} Please provide a valid wordlist file path")
    
    # Output file
    output_file = input(f"{color_text('💾', Fore.YELLOW)} Enter output file {color_text('(default: results/scan_results.txt)', Fore.WHITE)}: ").strip()
    if not output_file:
        output_file = "results/scan_results.txt"
    
    return target, threads, paths_file, output_file

def create_default_wordlist():
    """Create default wordlist file if it doesn't exist."""
    default_paths = [
        "admin", "administrator", "login", "panel", "admin/login", 
        "adminpanel", "cp", "controlpanel", "manager", "webadmin",
        "admincp", "administrator/login", "wp-admin", "user/login",
        "backend", "dashboard", "admin/dashboard", "admin_area",
        "admin1", "admin2", "admin3", "admin4", "admin5"
    ]
    
    os.makedirs("wordlist", exist_ok=True)
    with open("wordlist/admin_paths.txt", "w") as f:
        for path in default_paths:
            f.write(path + "\n")
    print(f"{color_text('✅', Fore.GREEN)} Default wordlist created: {color_text('wordlist/admin_paths.txt', Fore.YELLOW)}")

def about_tool():
    """Display about information."""
    print(f"\n{color_text('╔' + '═' * 58 + '╗', Fore.CYAN)}")
    print(f"{color_text('║' + f'{Fore.CYAN}ℹ️  ABOUT ADMIN PANEL FINDER{Fore.CYAN}'.center(58) + '║', Fore.CYAN)}")
    print(f"{color_text('╚' + '═' * 58 + '╝', Fore.CYAN)}")
    
    print(f"{color_text('📋', Fore.YELLOW)} {color_text('Description:', Fore.GREEN, Style.BRIGHT)}")
    print("   This tool helps security researchers and penetration testers")
    print("   find admin panels and login pages on websites.")
    
    print(f"\n{color_text('⚡', Fore.YELLOW)} {color_text('Features:', Fore.GREEN, Style.BRIGHT)}")
    features = [
        "Multi-threaded scanning for faster results",
        "Customizable wordlist support",
        "Colorful and interactive interface",
        "Results export to file",
        "Simple menu-based navigation"
    ]
    for i, feature in enumerate(features, 1):
        print(f"   {color_text(f'{i}.', Fore.CYAN)} {feature}")
    
    print(f"\n{color_text('⚠️', Fore.RED)} {color_text('Disclaimer:', Fore.RED, Style.BRIGHT)}")
    print("   This tool is for educational and authorized testing purposes only.")
    print("   Misuse of this tool is strictly prohibited.")

def contact_info():
    """Display contact information."""
    print(f"\n{color_text('╔' + '═' * 58 + '╗', Fore.GREEN)}")
    print(f"{color_text('║' + f'{Fore.CYAN}📞 CONTACT INFORMATION{Fore.GREEN}'.center(58) + '║', Fore.GREEN)}")
    print(f"{color_text('╚' + '═' * 58 + '╝', Fore.GREEN)}")
    
    contacts = [
        ("📱 Telegram ID", "https://t.me/darkvaiadmin", Fore.CYAN),
        ("📢 Telegram Channel", "https://t.me/windowspremiumkey", Fore.BLUE),
        ("🌐 Website", "https://crackyworld.com/", Fore.MAGENTA),
        ("💻 Developer", "Chowdhuryvai", Fore.YELLOW)
    ]
    
    for label, value, color in contacts:
        print(f"   {color_text(label, Fore.WHITE)}: {color_text(value, color)}")

if __name__ == "__main__":
    print_banner()
    
    if not check_internet_connection():
        sys.exit(1)
    
    # Check for colorama
    if not COLORAMA_AVAILABLE:
        print(f"{color_text('[INFO]', Fore.YELLOW)} For better colors, install colorama: pip install colorama")
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            try:
                target, threads, paths_file, output_file = get_scan_parameters()
                admin_finder(target, threads, paths_file, output_file)
                
                # Ask if user wants to continue
                continue_scan = input(f"\n{color_text('🔄', Fore.YELLOW)} Do you want to perform another scan? {color_text('(y/n)', Fore.WHITE)}: ").strip().lower()
                if continue_scan != 'y':
                    print(f"{color_text('👋', Fore.CYAN)} Thank you for using Admin Panel Finder!")
                    break
                    
            except Exception as e:
                print(f"{color_text('❌', Fore.RED)} Error: {str(e)}")
                continue
                
        elif choice == '2':
            about_tool()
            input(f"\n{color_text('📝', Fore.YELLOW)} Press Enter to continue...")
            
        elif choice == '3':
            contact_info()
            input(f"\n{color_text('📝', Fore.YELLOW)} Press Enter to continue...")
            
        elif choice == '4':
            print(f"{color_text('👋', Fore.CYAN)} Thank you for using Admin Panel Finder!")
            break
