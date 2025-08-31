import json
from utils import slow_print, pause, clear, c_print
from player import Player
from narrativa import construir_abrigo
from path_handler import get_data_path
from colorama import Fore, Style

# ------------------- CARREGAR DADOS -------------------
try:
    with open(get_data_path("items.json"), "r", encoding="utf-8") as f:
        ITEMS_DATA = json.load(f)
    with open(get_data_path("consumables.json"), "r", encoding="utf-8") as f:
        CONSUMABLE_EFFECTS = json.load(f)
    with open(get_data_path("recipes_cooking.json"), "r", encoding="utf-8") as f:
        CULINARY_RECIPES = json.load(f)
    with open(get_data_path("recipes_craft.json"), "r", encoding="utf-8") as f:
        CRAFT_RECIPES = json.load(f)

    FOODS = [item.get("name") for item in ITEMS_DATA.get("foods", []) if item.get("name")]
    # Adiciona os consumíveis que não são comidas (remédios) à lista de consumíveis gerais
    ALL_CONSUMABLES = {**CONSUMABLE_EFFECTS, **{item['name']: {} for item in ITEMS_DATA.get("medicine", [])}}


except FileNotFoundError:
    c_print("Erro: Arquivos de dados não encontrados.", Fore.RED)
    exit()

# ------------------- MENU DO PET -------------------
def pet_menu(player: Player):
    """
    Exibe o menu de interação com o pet.
    """
    if not player.pet:
        c_print("Voce nao tem um companheiro animal.", Fore.YELLOW)
        pause()
        return

    while True:
        clear()
        pet = player.pet
        c_print(f"--- Menu de {pet['nome']} ---", Fore.MAGENTA)
        
        pet_humor_bar = player._create_progress_bar(pet['humor'], 100, cor=Fore.MAGENTA)
        xp_necessario = pet['level'] * 10
        pet_xp_bar = player._create_progress_bar(pet['xp'], xp_necessario, cor=Fore.CYAN)

        print(f"Nome: {pet['nome']} ({pet['tipo'].capitalize()})")
        print(f"Nivel: {pet['level']}")
        print(f"XP: {pet_xp_bar}")
        print(f"Humor: {pet_humor_bar}")

        print("\n1 - Alimentar")
        print("2 - Voltar")
        choice = input("> ")

        if choice == "1":
            clear()
            c_print(f"O que voce quer dar para {pet['nome']}?", Fore.YELLOW)
            
            # Filtra apenas os itens de comida do inventário
            food_in_inventory = {item: qty for item, qty in player.inventory.items() if item in FOODS}

            if not food_in_inventory:
                c_print("Voce nao tem nenhuma comida na mochila.", Fore.LIGHTBLACK_EX)
                pause()
                continue
            
            food_list = list(food_in_inventory.keys())
            for i, item in enumerate(food_list):
                print(f"{i+1} - {item} x{food_in_inventory[item]}")
            
            print("0 - Voltar")
            food_choice = input("> ")
            
            try:
                food_index = int(food_choice) - 1
                if food_index == -1:
                    continue
                if 0 <= food_index < len(food_list):
                    item_escolhido = food_list[food_index]
                    player.alimentar_pet(item_escolhido)
                    pause()
                else:
                    c_print("Opção inválida.", Fore.RED)
                    pause()
            except ValueError:
                c_print("Digite um número.", Fore.RED)
                pause()

        elif choice == "2":
            break
        else:
            c_print("Opção inválida.", Fore.RED)
            pause(1)


# ------------------- INVENTÁRIO E ITENS -------------------
def inventario_menu(player: Player):
    """
    Exibe o menu de inventário principal com cores.
    """
    while True:
        clear()
        c_print("\nInventario:", Fore.YELLOW)
        print("1 - Mochila")
        print("2 - Consumir / Usar Remédio / Equipar")
        print("3 - Cozinha (Receitas de Comida)")
        print("4 - Craft (Construção/Armas/Roupas/Remédios)")
        print("5 - Voltar") 
        choice = input("> ")

        if choice == "1":
            if player.inventory:
                c_print("Sua mochila contém:", Fore.YELLOW)
                for item, qty in player.inventory.items():
                    print(f" - {item} x{qty}")
            else:
                c_print("Sua mochila está vazia.", Fore.LIGHTBLACK_EX)
            pause()
        elif choice == "2":
            use_items(player)
        elif choice == "3":
            show_crafting_menu(player, CULINARY_RECIPES, "Cozinha")
        elif choice == "4":
            show_crafting_menu(player, CRAFT_RECIPES, "Craft")
        elif choice == "5":
            break
        else:
            c_print("Opção inválida.", Fore.RED)
            pause(1)


def use_items(player: Player):
    """
    Menu para usar, consumir ou equipar itens, com cores.
    """
    clear()
    if not player.inventory:
        c_print("Mochila vazia.", Fore.LIGHTBLACK_EX)
        pause()
        return
    
    items_list = list(player.inventory.keys())
    for i, item in enumerate(items_list):
        print(f"{i+1} - {item} x{player.inventory[item]}")

    c_print("\nEscolha um item para usar/consumir/equipar ou 0 para voltar:", Fore.YELLOW)
    choice = input("> ")
    if choice == "0":
        return
    
    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(items_list):
            item = items_list[choice_index]
            
            if item in ALL_CONSUMABLES:
                if player.remove_item(item):
                    effects = CONSUMABLE_EFFECTS.get(item, {})
                    player.apply_effects(effects)
                    c_print(f"Você consumiu {item}. Efeitos aplicados.", Fore.GREEN)
            
            elif item == "antibiotico":
                if player.remove_item(item):
                    player.doenca = False
                    player.health = min(100, player.health + 20)
                    c_print("Você tomou antibiótico e se sentiu melhor.", Fore.GREEN)
            elif item == "antidoto":
                if player.remove_item(item):
                    player.veneno = False
                    c_print("Você tomou antídoto e curou o veneno.", Fore.GREEN)
            
            elif "roupa" in item or "armadura" in item:
                player.equiped_armor = item
                c_print(f"Você equipou {item}.", Fore.CYAN)
            else:
                c_print("Não é possível usar este item agora.", Fore.YELLOW)
        else:
            c_print("Opção inválida.", Fore.RED)
            
    except ValueError:
        c_print("Por favor, digite um número válido.", Fore.RED)
    
    pause()


def show_crafting_menu(player: Player, recipes_data: dict, menu_title: str):
    """
    Função unificada para mostrar menus de criação com cores.
    """
    clear()
    c_print(f"=== {menu_title} ===", Fore.YELLOW)
    
    receitas_disponiveis = [
        recipe for recipe in recipes_data if player.has_items(recipes_data[recipe])
    ]

    if not receitas_disponiveis:
        c_print("Você não tem ingredientes suficientes para criar nada.", Fore.LIGHTBLACK_EX)
        pause()
        return

    c_print("\nReceitas disponíveis:", Fore.YELLOW)
    for i, recipe_name in enumerate(receitas_disponiveis):
        ingredients_str = ", ".join([f"{item} x{qty}" for item, qty in recipes_data[recipe_name].items()])
        print(f"{i+1} - {recipe_name} (Requer: {ingredients_str})")

    c_print("\nEscolha uma receita para criar ou 0 para voltar:", Fore.YELLOW)
    choice = input("> ")

    if choice == "0":
        return

    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(receitas_disponiveis):
            recipe_name = receitas_disponiveis[choice_index]
            
            for item, qty in recipes_data[recipe_name].items():
                player.remove_item(item, qty)
                
            player.add_item(recipe_name)
            c_print(f"[SUCESSO] Voce criou {recipe_name}!", Fore.GREEN)
        else:
            c_print("Opção inválida.", Fore.RED)

    except ValueError:
        c_print("Por favor, digite um número válido.", Fore.RED)

    pause()