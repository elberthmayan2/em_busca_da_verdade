import random
from time import sleep
from utils import slow_print, pause, clear, c_print
from player import Player, PET_STATS
import json
from path_handler import get_data_path
from colorama import Fore, Style

# Carrega os dados do jogo a partir dos arquivos JSON
try:
    with open(get_data_path("items.json"), "r", encoding="utf-8") as f:
        ITEMS_DATA = json.load(f)
    with open(get_data_path("enemies.json"), "r", encoding="utf-8") as f:
        ENEMIES_DATA = json.load(f)
except FileNotFoundError as e:
    c_print(f"Erro: Arquivo de dados nao encontrado: {e.filename}", Fore.RED)
    exit()

def mudar_clima_aleatoriamente(player: Player):
    """
    Muda o clima atual do jogo de forma aleatoria.
    """
    opcoes_clima = ["Ensolarado", "Chuvoso", "Nublado", "Frio", "Quente"]
    novo_clima = random.choice(opcoes_clima)
    if novo_clima != player.clima:
        player.clima = novo_clima
        c_print(f"\nO tempo mudou para {novo_clima}!", Fore.CYAN)
        pause()

# ------------------- INTRODUCAO -------------------
def start_intro(player: Player):
    slow_print("Voce acorda em uma floresta densa, sem memoria do que aconteceu.")
    slow_print("Sua garganta esta seca e o estomago roncando — voce precisa de agua e comida.")
    slow_print("Ao longe, voce avista uma cidade semi-destruida e um caminho que leva ate ela.")
    pause()
    slow_print("Essa sera a sua busca pela verdade... o que aconteceu com o mundo e sua familia.")
    pause()

# ------------------- FUNCOES DE EVENTOS -------------------

def get_event_data(event_type: str, location_name: str):
    """
    Retorna os dados para um tipo de evento em um local especifico.
    """
    data = {
        "explore_item": {
            "Floresta": ITEMS_DATA.get("foods", []) + ITEMS_DATA.get("materials", []),
            "Cidade": ITEMS_DATA.get("materials", []) + ITEMS_DATA.get("tools", []) + ITEMS_DATA.get("medicine", []),
            "Montanhas": ITEMS_DATA.get("rare_materials", []) + ITEMS_DATA.get("gems", []) + ITEMS_DATA.get("tools", [])
        },
        "animal_encounter": {
            "Floresta": ["cobra", "lobo", "urso", "raposa"],
            "Cidade": ["rato", "cao_selvagem"],
            "Montanhas": ["lobo", "urso_da_montanha", "leao_da_montanha"]
        },
        "find_water": {"Floresta": True, "Cidade": False, "Montanhas": True},
        "find_lake": {"Floresta": True, "Cidade": False, "Montanhas": True},
        "find_diary": {"Floresta": True, "Cidade": True, "Montanhas": False},
        "meet_npc": {"Floresta": True, "Cidade": True, "Montanhas": True},
        "find_pet": {"Floresta": ["lobo", "corvo"], "Cidade": ["gato_selvagem"], "Montanhas": ["aguia"]},
        "find_landmark": {"Floresta": False, "Cidade": False, "Montanhas": True}
    }
    return data.get(event_type, {}).get(location_name, None)

def explore_item(player: Player, location_items: list):
    """
    Logica para encontrar e pegar itens em um local.
    """
    if not location_items:
        return
    if random.random() < (0.5 + player.inteligencia * 0.02):
        item_data = random.choice(location_items)
        item_name = item_data.get("name")
        if not item_name: return
        c_print(f"Voce encontrou {item_name}. Deseja pegar? (s/n)", Fore.YELLOW)
        if input("> ").lower() == "s":
            if player.add_item(item_name):
                c_print(f"[+] {item_name} adicionado a mochila.", Fore.GREEN)
                player.aumentar_habilidade("inteligencia", 1)
    else:
        c_print("Voce procurou mas nao encontrou nada de util.", Fore.LIGHTBLACK_EX)


def combat_system(player: Player, opponent_name: str, opponent_data: dict):
    """
    Sistema de combate por turnos, com participação do pet.
    """
    clear()
    c_print(f"Um {opponent_name} selvagem aparece e te ataca!", Fore.RED)
    pause()

    opponent_health = opponent_data.get("strength", 30) * 2
    opponent_damage = opponent_data.get("damage", 15)
    is_defending = False
    pet_stun_turns = 0

    while player.health > 0 and opponent_health > 0:
        clear()
        print(f"--- BATALHA: {player.name} vs {opponent_name.capitalize()} ---")
        print(f"Sua Vida: {Fore.GREEN}{player.health}/100{Style.RESET_ALL}")
        print(f"Vida do {opponent_name}: {Fore.YELLOW}{opponent_health}{Style.RESET_ALL}")
        if is_defending:
            c_print("Voce esta em posicao de defesa.", Fore.CYAN)
        print("----------------------------------")

        print("\nO que voce deseja fazer?:")
        print("1 - Ataque Rapido")
        print("2 - Ataque Forte")
        print("3 - Defender")
        print("4 - Tentar Fugir")
        choice = input("> ")

        is_defending = False # Reseta a defesa a cada turno do jogador

        if choice == "1":
            hit_chance = 0.8 + (player.inteligencia * 0.01)
            if random.random() < hit_chance:
                damage = int(player.forca * 0.8)
                opponent_health -= damage
                c_print(f"Voce acerta um ataque rapido e causa {damage} de dano!", Fore.YELLOW)
            else:
                c_print("Voce errou o ataque rapido!", Fore.LIGHTBLACK_EX)
        elif choice == "2":
            hit_chance = 0.5 + (player.forca * 0.01)
            if random.random() < hit_chance:
                damage = int(player.forca * 1.5)
                opponent_health -= damage
                c_print(f"Voce acerta um golpe poderoso e causa {damage} de dano!", Fore.YELLOW)
            else:
                c_print("Voce errou o ataque forte!", Fore.LIGHTBLACK_EX)
        elif choice == "3":
            is_defending = True
            c_print("Voce se prepara para defender o proximo ataque.", Fore.CYAN)
        elif choice == "4":
            if random.random() < (0.5 + player.sobrevivencia * 0.02):
                c_print("Voce conseguiu escapar!", Fore.GREEN)
                return
            else:
                c_print("A fuga falhou!", Fore.RED)
        else:
            c_print("Opcao invalida! Voce perdeu seu turno.", Fore.RED)
        pause()

        # --- TURNO DO PET ---
        if player.pet and opponent_health > 0:
            pet_damage = player.get_dano_pet()
            opponent_health -= pet_damage
            c_print(f"[PET] {player.pet['nome']} ataca e causa {pet_damage} de dano!", Fore.MAGENTA)
            
            # Habilidade especial do pet (chance de 20%)
            if random.random() < 0.2:
                pet_info = PET_STATS.get(player.pet['tipo'])
                if pet_info and pet_info['habilidade_especial'] == 'stun':
                    pet_stun_turns = 1 # Atordoa por 1 turno
                    c_print(f"[PET] {player.pet['nome']} uiva e atordoa o inimigo!", Fore.MAGENTA)
            pause()

        # --- TURNO DO INIMIGO ---
        if opponent_health > 0:
            if pet_stun_turns > 0:
                c_print(f"O {opponent_name} esta atordoado e nao consegue atacar!", Fore.YELLOW)
                pet_stun_turns -= 1
            else:
                c_print(f"O {opponent_name} ataca!", Fore.RED)
                damage_taken = opponent_damage
                if is_defending:
                    damage_taken = max(1, int(opponent_damage / 2))
                    c_print("Sua defesa absorveu parte do impacto!", Fore.CYAN)
                player.health -= damage_taken
                c_print(f"Voce recebeu {damage_taken} de dano.", Fore.RED)
            pause()

    clear()
    if player.health <= 0:
        c_print(f"Voce foi derrotado pelo {opponent_name}...", Fore.RED)
        player.vivo = False
        player.causa_morte = f"foi morto(a) por um(a) {opponent_name}" # Define a causa da morte
    else:
        c_print(f"[VITORIA] Voce derrotou o {opponent_name}!", Fore.GREEN)
        player.aumentar_habilidade("forca", 2)
        player.aumentar_habilidade("sobrevivencia", 1)
        
        # Pet ganha XP
        xp_ganho = opponent_data.get("strength", 30) // 2
        player.ganhar_xp_pet(xp_ganho)

        if opponent_data.get("loot"):
            for item, qty in opponent_data["loot"].items():
                if player.add_item(item, qty):
                    c_print(f"Voce pegou {qty}x {item} do corpo do {opponent_name}.", Fore.GREEN)
    pause()

def handle_event(player: Player, event_type: str, location_name: str):
    """
    Processa um evento especifico que ocorre durante a exploracao.
    """
    event_data = get_event_data(event_type, location_name)

    if event_type == "explore_item":
        explore_item(player, event_data)
    elif event_type == "animal_encounter":
        animal = random.choice(event_data)
        enemy_stats = ENEMIES_DATA.get(animal, {})
        if animal == "cobra":
            c_print(f"Voce encontra uma {animal}!", Fore.YELLOW)
            c_print("A cobra te mordeu! Voce esta envenenado.", Fore.RED)
            player.veneno = True
            player.health -= enemy_stats.get("damage", 10)
            if player.health <= 0 and player.vivo:
                player.vivo = False
                player.causa_morte = "morreu pela picada de uma cobra venenosa"
        else:
            combat_system(player, animal, enemy_stats)
    elif event_type == "find_water":
        c_print("Voce encontra um riacho. Deseja beber? (s/n)", Fore.CYAN)
        if input("> ").lower() == "s":
            player.thirst = min(100, player.thirst + 30)
            c_print("Voce bebeu agua fresca.", Fore.GREEN)
            player.aumentar_habilidade("sobrevivencia", 1)

    elif event_type == "find_lake":
        c_print("Voce encontra um lago. Deseja tentar pescar? (s/n)", Fore.CYAN)
        if input("> ").lower() == "s":
            if player.inventory.get("vara_de_pesca", 0) > 0:
                if player.inventory.get("pao", 0) > 0 or any("carne" in k for k in player.inventory):
                    slow_print("Voce usa isca para pescar...")
                    if random.random() < 0.7:
                        player.add_item("peixe")
                        c_print("Voce pescou um peixe!", Fore.GREEN)
                        player.aumentar_habilidade("sobrevivencia", 2)
                    else:
                        c_print("Nao conseguiu pescar nada...", Fore.LIGHTBLACK_EX)
                else:
                    c_print("Voce nao tem isca suficiente (pao ou carne).", Fore.YELLOW)
            else:
                c_print("Voce nao possui vara de pesca.", Fore.YELLOW)
    
    elif event_type == "find_diary":
        if player.story_progress < 5:
            diary_texts = {
                0: "[DIARIO] Voce encontra um diario velho. Ele descreve um apocalipse que devastou o mundo...",
                1: "[DIARIO] Voce encontra mais uma pagina. Ela fala sobre como as pessoas comecaram a perder a memoria...",
                2: "[DIARIO] Outra pagina, mais perturbadora. O autor menciona que sua familia precisava fugir para as montanhas...",
                3: "[DIARIO] A penultima anotacao. O autor escreve sobre como a floresta esconde muitos segredos...",
                4: "[DIARIO] A ultima pagina, quase apagada. Uma ultima frase: 'A verdade esta nas memorias. Encontre as suas.'"
            }
            c_print(diary_texts.get(player.story_progress), Fore.YELLOW)
            player.story_progress += 1
            c_print(f"O seu progresso na historia e de {player.story_progress}/5.", Fore.YELLOW)
            player.aumentar_habilidade("inteligencia", 3)
        else:
            slow_print("Voce encontrou um livro em branco.")

    elif event_type == "meet_npc":
        npc_warnings = [
            "Cuidado! Este lugar nao e seguro. Evite as cidades grandes.",
            "Nao confie em ninguem, mas eu posso te dar uma dica: as montanhas ao sul sao mais seguras.",
            "Se voce for para o centro da cidade, procure por um abrigo... o ar la e toxico."
        ]
        warning = random.choice(npc_warnings)
        slow_print("Voce encontra um sobrevivente perdido.")
        c_print(f"NPC: '{warning}'", Fore.LIGHTBLUE_EX)
        pause()
        player.aumentar_habilidade("inteligencia", 1)

    elif event_type == "find_pet":
        if not player.pet:
            pet_type = random.choice(event_data)
            c_print(f"Voce encontra um {pet_type} solitario. Deseja tentar domesticar? (s/n)", Fore.CYAN)
            if input("> ").lower() == "s":
                c_print(f"[PET] Voce agora tem um {pet_type} como companheiro. Qual nome deseja dar?", Fore.GREEN)
                nome = input("> ")
                player.domesticar_pet(nome, pet_type) # CORRIGIDO: Usa a função de domesticação
                player.aumentar_habilidade("sobrevivencia", 3)

    elif event_type == "find_landmark":
        c_print("[LOCAL] Voce encontrou um ponto de referencia nas montanhas. O ar aqui e mais limpo.", Fore.CYAN)
        slow_print("Voce se sente mais revigorado.")
        player.health = min(100, player.health + 15)


def construir_abrigo(player: Player):
    """
    Permite ao jogador construir ou melhorar seu abrigo.
    """
    clear()
    c_print("--- Construir/Melhorar Abrigo ---", Fore.YELLOW)

    if player.abrigo_nivel == 0:
        recipe = {"madeira": 5, "galho": 3, "pano": 2}
        if player.has_items(recipe):
            c_print("Voce tem os itens necessarios para construir um Abrigo Basico.", Fore.YELLOW)
            print(f"Requisitos: {recipe}")
            slow_print("Deseja construir? (s/n)")
            if input("> ").lower() == "s":
                for item, qty in recipe.items():
                    player.remove_item(item, qty)
                player.abrigo_nivel = 1
                c_print("[SUCESSO] Voce construiu um Abrigo Basico! Agora voce esta mais protegido.", Fore.GREEN)
                player.aumentar_habilidade("sobrevivencia", 5)
        else:
            c_print("Voce nao tem itens suficientes para construir um abrigo.", Fore.RED)
            print(f"Requisitos: {recipe}")

    elif player.abrigo_nivel == 1:
        recipe = {"madeira": 10, "pedra": 5, "tecido": 3}
        if player.has_items(recipe):
            c_print("Voce tem os itens para melhorar para um Abrigo Melhorado.", Fore.YELLOW)
            print(f"Requisitos: {recipe}")
            slow_print("Deseja melhorar? (s/n)")
            if input("> ").lower() == "s":
                for item, qty in recipe.items():
                    player.remove_item(item, qty)
                player.abrigo_nivel = 2
                c_print("[SUCESSO] Seu abrigo foi melhorado! Voce agora tem bonus contra o clima.", Fore.GREEN)
                player.aumentar_habilidade("sobrevivencia", 5)
        else:
            c_print("Voce nao tem itens suficientes para melhorar o abrigo.", Fore.RED)
            print(f"Requisitos: {recipe}")
    
    elif player.abrigo_nivel == 2:
        c_print("Seu abrigo ja esta no nivel maximo.", Fore.CYAN)

    pause()


# Pesos de probabilidade para cada tipo de evento por local
FLORESTA_EVENTS_WEIGHTS = {
    "explore_item": 0.25, "animal_encounter": 0.2, "find_water": 0.15,
    "find_lake": 0.1, "find_diary": 0.1, "meet_npc": 0.1, "find_pet": 0.1
}
CIDADE_EVENTS_WEIGHTS = {
    "explore_item": 0.4, "animal_encounter": 0.2, "find_water": 0.1,
    "find_diary": 0.1, "meet_npc": 0.2
}
MONTANHAS_EVENTS_WEIGHTS = {
    "explore_item": 0.3, "animal_encounter": 0.2, "find_water": 0.1,
    "find_lake": 0.1, "meet_npc": 0.1, "find_pet": 0.1, "find_landmark": 0.1
}

def explore_location(player: Player, location_name: str, events_weights: dict):
    """
    Funcao principal que rege a exploracao de um local.
    """
    player.location = location_name
    # Animação de exploração
    c_print(f"\nExplorando {location_name}", Fore.CYAN)
    for i in range(5):
        print(".", end='', flush=True)
        sleep(0.3)
    print("\n")
    
    num_events = random.randint(2, 4)
    for _ in range(num_events):
        if not player.vivo: break # Interrompe a exploracao se o jogador morrer
        
        event_type = random.choices(list(events_weights.keys()), weights=list(events_weights.values()), k=1)[0]
        
        handle_event(player, event_type, location_name)
        
        # Reduz a chance de o mesmo evento ocorrer novamente em sequencia
        events_weights[event_type] = max(0.01, events_weights[event_type] * 0.5)

        player.update_time(hours=2)
        
def narrativa_floresta(player: Player):
    temp_weights = FLORESTA_EVENTS_WEIGHTS.copy()
    explore_location(player, "Floresta", temp_weights)

def narrativa_cidade(player: Player):
    temp_weights = CIDADE_EVENTS_WEIGHTS.copy()
    explore_location(player, "Cidade", temp_weights)

def narrativa_montanhas(player: Player):
    temp_weights = MONTANHAS_EVENTS_WEIGHTS.copy()
    explore_location(player, "Montanhas", temp_weights)