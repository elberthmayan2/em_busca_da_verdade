from player import Player
from menus import inventario_menu, pet_menu
from narrativa import start_intro, narrativa_floresta, narrativa_cidade, narrativa_montanhas, construir_abrigo, mudar_clima_aleatoriamente
from utils import slow_print, pause, clear, load_all_items_data, print_menu # Importa a nova função
from savegame import salvar_jogo, carregar_jogo
from colorama import Fore, Style
import sys # Importa a biblioteca sys para uma saída mais limpa

FINAL_AGE = 30
# Carrega todos os dados dos itens uma única vez no início do jogo
ALL_ITEMS = load_all_items_data() 

def main_menu():
    """
    Menu inicial do jogo.
    """
    while True:
        clear()
        # Título simplificado
        print(Fore.YELLOW + "========================================")
        print(Style.RESET_ALL + "          EM BUSCA DA VERDADE          ")
        print(Fore.YELLOW + "========================================" + Style.RESET_ALL)
        
        print("\nO que deseja fazer?")
        print("1 - Novo Jogo")
        print("2 - Carregar Jogo")
        print("3 - Sair")

        choice = input("> ")
        if choice == "1":
            start_new_game()
            break
        elif choice == "2":
            load_existing_game()
            break
        elif choice == "3":
            print("Até a próxima!")
            sys.exit() # Fecha o jogo
        else:
            print("Opção inválida.")
            pause(1)

def start_new_game():
    """
    Inicia um novo jogo.
    """
    nome = input("Digite o nome do seu personagem: ")
    # Passa a tabela de consulta de itens ao criar um novo jogador
    player = Player(nome, ALL_ITEMS) 
    start_intro(player)
    game_loop(player)

def load_existing_game():
    """
    Carrega um jogo salvo.
    """
    save_data = carregar_jogo()
    if save_data:
        # Cria a instância do jogador, passando a tabela de itens
        player = Player(save_data["name"], ALL_ITEMS) 
        
        # Carrega os atributos salvos no objeto do jogador
        # É importante fazer isso depois da inicialização para garantir que todos os atributos existam
        player.health = save_data.get("health", 100)
        player.hunger = save_data.get("hunger", 50)
        player.thirst = save_data.get("thirst", 50)
        player.age = save_data.get("age", 18)
        player.inventory = save_data.get("inventory", {})
        player.location = save_data.get("location", "Floresta")
        player.pet = save_data.get("pet", None) # Carrega os dados do pet
        player.clima = save_data.get("clima", "Ensolarado")
        player.doenca = save_data.get("doenca", False)
        player.veneno = save_data.get("veneno", False)
        player.equiped_armor = save_data.get("equipped_armor", None)
        player.has_fire = save_data.get("has_fire", False)
        player.story_progress = save_data.get("story_progress", 0)
        player.forca = save_data.get("forca", 10)
        player.inteligencia = save_data.get("inteligencia", 10)
        player.sobrevivencia = save_data.get("sobrevivencia", 10)
        player.abrigo_nivel = save_data.get("abrigo_nivel", 0)
        
        # Converte a data de volta para o objeto datetime
        from datetime import datetime
        player.current_date = datetime.strptime(save_data["current_date"], "%Y-%m-%d %H:%M:%S")

        print("Jogo carregado com sucesso!")
        pause(1)
        game_loop(player)
    else:
        print("Nenhum jogo salvo encontrado.")
        pause(1)
        main_menu() # Volta para o menu se não encontrar save

def game_loop(player):
    """
    Loop principal do jogo.
    """
    while player.vivo:
        player.status()
        
        menu_title = "O QUE DESEJA FAZER?"
        menu_options = {
            "1": "Inventário",
            "2": "Menu do Pet",
            "3": "Explorar a cidade",
            "4": "Explorar a floresta",
            "5": "Explorar as montanhas",
            "6": "Construir/Melhorar Abrigo",
            "7": "Salvar jogo",
            "8": "Sair do jogo"
        }
        
        print_menu(menu_title, menu_options)
        choice = input("> ")

        if choice == "1":
            inventario_menu(player)
        elif choice == "2":
            pet_menu(player) # CHAMA O NOVO MENU
        elif choice == "3":
            narrativa_cidade(player)
        elif choice == "4":
            narrativa_floresta(player)
        elif choice == "5":
            narrativa_montanhas(player)
        elif choice == "6":
            construir_abrigo(player)
        elif choice == "7":
            salvar_jogo(player)
            pause(1)
        elif choice == "8":
            print("Tem certeza que deseja sair sem salvar? (s/n)")
            confirm = input("> ").lower()
            if confirm == "s":
                break
        else:
            print("Opção inválida.")
            pause(1)

        # Atualiza o tempo e o clima após cada ação que não seja salvar ou menus
        if choice not in ["1", "2", "7", "8"]:
            player.update_time(hours=2)
            mudar_clima_aleatoriamente(player)

        # Verifica se o jogador atingiu idade final para o desfecho
        if player.age >= FINAL_AGE:
            final_story(player)
            player.vivo = False # Encerra o jogo para mostrar o menu de game over
            break

    # Quando o loop termina (jogador morreu ou saiu)
    if not player.vivo:
        game_over_menu(player)
    else:
        main_menu()


def final_story(player):
    """
    Função que exibe o desfecho da história com base no progresso do playerr.
    """
    clear()
    print("\n\n=== A VERDADE REVELADA ===")
    pause(2)
    print("Você fez 30 anos e, de repente, as memórias perdidas voltam. As imagens de sua família e os eventos que levaram ao apocalipse se misturam na sua mente. Você finalmente entende a verdade.")
    pause(3)

    # Desfecho com base no progresso da história
    if player.story_progress >= 5:
        print("\n[Final Perfeito]: A verdade se revela por completo.")
        print("Você reuniu todos os fragmentos da história. A verdade é que o governo, para evitar uma superpopulação, usou uma arma biológica para controlar a memória da humanidade. Mas algo deu errado, a arma biológica se tornou um vírus devastador. Seu pai, um cientista, escondeu a família em um abrigo subterrâneo e você foi o único que conseguiu escapar e ter a memória restaurada.")
    elif player.story_progress >= 3:
        print("\n[Final Bom]: Você se lembra de algumas coisas, mas não de tudo.")
        print("Você lembra que o mundo foi devastado por algo causado pelo homem. Você e sua família fugiram para um abrigo, mas algo deu errado e você foi o único a escapar. A verdade completa ainda é um mistério para você, mas você entende o que aconteceu.")
    else:
        print("\n[Final Triste]: Você não conseguiu se lembrar de nada.")
        print("As memórias de sua família nunca retornaram. A sua jornada chega ao fim sem uma resposta. Você continua a viver na esperança de um dia encontrar a verdade que tanto procurou.")

    pause(5)

def game_over_menu(player):
    """
    Exibe o menu de fim de jogo com a causa da morte.
    """
    clear()
    print("\n--- Fim de Jogo ---")
    if player.causa_morte:
        print(f"Causa da morte: Você {player.causa_morte}.")
    
    print(f"Você sobreviveu até os {player.age} anos.")
    
    while True:
        print("\nO que você deseja fazer?")
        print("1 - Reiniciar o jogo")
        print("2 - Sair do jogo")
        choice = input("> ")
        if choice == "1":
            main_menu() 
            break
        elif choice == "2":
            print("Até a próxima!")
            sys.exit() 
        else:
            print("Opção inválida.")
            pause(1)

if __name__ == "__main__":
    main_menu()