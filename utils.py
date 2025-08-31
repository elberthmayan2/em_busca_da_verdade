# utils.py
import sys
import time
import os
import json
from path_handler import get_data_path
from colorama import Fore, init, Style

init(autoreset=True)

def slow_print(texto, delay=0.03):
    """Imprime o texto lentamente, simulando digitação."""
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  

def pause(segundos=2):
    time.sleep(segundos)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def c_print(text, color=Fore.WHITE):
    """Prints text in a given color."""
    print(color + text)

def print_menu(title, options):
    """Imprime um menu formatado com título e bordas."""
    print(Fore.CYAN + f"╔{'═' * (len(title) + 2)}╗")
    print(f"║ {title.upper()} ║")
    print(f"╚{'═' * (len(title) + 2)}╝" + Style.RESET_ALL)
    print("")
    for key, value in options.items():
        print(f"{key} - {value}")
    print("-" * (len(title) + 4))


def escolha(msg, opcoes):
    """
    Pergunta ao jogador até ele digitar uma opção válida.
    opcoes deve ser uma lista, ex: ["1", "2", "3"].
    """
    while True:
        resposta = input(msg).strip().lower()
        if resposta in opcoes:
            return resposta
        else:
            print(f"[!] Opcao invalida! Escolha entre {opcoes}.")

def load_all_items_data():
    """
    Carrega todos os dados de itens de items.json em um único dicionário
    para acesso rápido (lookup table).
    """
    try:
        with open(get_data_path("items.json"), "r", encoding="utf-8") as f:
            items_data = json.load(f)

        item_lookup = {}
        for category in items_data.values():
            for item in category:
                if isinstance(item, dict) and "name" in item:
                    item_lookup[item['name']] = item
        return item_lookup
    except FileNotFoundError:
        slow_print("Erro: Arquivo de dados 'data/items.json' não encontrado.")
        exit()
    except json.JSONDecodeError:
        slow_print("Erro: O arquivo 'data/items.json' está mal formatado.")
        exit()