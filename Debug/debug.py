import os
import sys
import time
import webbrowser

def check_integrity():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    list_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_files_list.txt")
    
    github_url = "https://github.com/Nu4g3"
    
    if not os.path.exists(list_file):
        print(f"Erreur: Fichier de liste manquant ({list_file})")
        webbrowser.open(github_url)
        return

    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    
    missing_found = False
    
    try:
        with open(list_file, "r", encoding="utf-8") as f:
            paths = [line.strip() for line in f if line.strip()]
            
        print("Vérification de l'intégrité du projet...\n")
        
        for path in paths:
            time.sleep(0.05)
            full_path = os.path.join(base_path, path)
            if os.path.exists(full_path):
                print(f"{GREEN}[OK]{RESET} {path}")
            else:
                print(f"{RED}[MANQUANT]{RESET} {path}")
                missing_found = True
                
    except Exception as e:
        print(f"{RED}Erreur lors de la lecture: {e}{RESET}")
        missing_found = True

    if missing_found:
        print(f"\n{RED}Intégrité compromise. Redirection vers GitHub...{RESET}")
        time.sleep(3)
        webbrowser.open(github_url)
    else:
        print(f"\n{GREEN}Tous les fichiers sont présents. Intégrité OK.{RESET}")
        time.sleep(3)

if __name__ == "__main__":
    if sys.platform == "win32":
        os.system("color")
        
    check_integrity()
