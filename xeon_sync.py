import os
import subprocess

def sync_to_github(commit_message="XEON NEXUS Update v1.4"):
    print("🚀 [XEON SYNC] Iniciando subida para o GitHub...")
    try:
        # Adiciona todos os arquivos alterados
        subprocess.run(["git", "add", "."], check=True)
        # Cria o ponto de controle (Commit)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        # Sobe para a nuvem
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ [SUCESSO] Código soberano no GitHub.")
    except Exception as e:
        print(f"❌ [ERRO] Falha na sincronização: {e}")
        print("Dica: Verifique se você já deu 'git init' na pasta.")

# sync_to_github()
