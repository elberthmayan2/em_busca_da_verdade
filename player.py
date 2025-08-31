# player.py

import random
from datetime import datetime, timedelta
from utils import slow_print, clear, c_print
from colorama import Fore, Style

# Define as características de cada tipo de pet
PET_STATS = {
    "lobo": {"habilidade": "sobrevivencia", "bonus": 2, "dano_base": 5, "habilidade_especial": "stun"},
    "corvo": {"habilidade": "inteligencia", "bonus": 2, "dano_base": 3, "habilidade_especial": "find_item"},
    "gato_selvagem": {"habilidade": "inteligencia", "bonus": 2, "dano_base": 4, "habilidade_especial": "bleed"},
    "aguia": {"habilidade": "sobrevivencia", "bonus": 2, "dano_base": 4, "habilidade_especial": "distract"}
    # Adicione outros pets aqui
}

# Define as comidas favoritas de cada pet
PET_FOODS = {
    "lobo": ["carne_crua", "carne_de_lobo", "carne_de_urso"],
    "corvo": ["fruta_silvestre", "milho"],
    "gato_selvagem": ["peixe", "carne_de_rato"],
    "aguia": ["peixe", "carne_de_cobra"]
}


class Player:
    def __init__(self, name, all_items_data):
        """
        Inicializa um novo jogador com os atributos basicos e o novo sistema de pet.
        """
        self.name = name
        self.health = 100
        self.hunger = 50
        self.thirst = 50
        self.start_date = datetime(1994, 12, 6, 8, 0)
        self.current_date = self.start_date
        self.age = 18
        self.inventory = {}
        
        # --- SISTEMA DE PET APRIMORADO ---
        self.pet = None # Agora será um dicionário: {"nome": str, "tipo": str, "level": int, "xp": int, "humor": int}
        
        self.doenca = False
        self.veneno = False
        self.equiped_armor = None
        self.has_fire = False
        self.vivo = True
        self.clima = "Ensolarado"
        self.location = "Floresta"
        self.story_progress = 0
        self.age_milestones_met = {20: False, 25: False, 28: False}
        
        self.forca = 10
        self.inteligencia = 10
        self.sobrevivencia = 10
        
        self.abrigo_nivel = 0
        self.has_fire = False

        self.max_weight = 50.0
        self.ALL_ITEMS = all_items_data
        
        # --- NOVO ATRIBUTO ---
        self.causa_morte = None # Armazena a causa da morte

    def domesticar_pet(self, nome, tipo):
        """
        Adiciona um novo pet ao jogador e aplica seu bônus passivo.
        """
        self.pet = {"nome": nome, "tipo": tipo, "level": 1, "xp": 0, "humor": 100}
        stats = PET_STATS.get(tipo)
        if stats:
            self.aumentar_habilidade(stats["habilidade"], stats["bonus"])
            c_print(f"A companhia de {nome} te deixa mais confiante!", Fore.MAGENTA)

    def alimentar_pet(self, item_comida):
        """
        Alimenta o pet, aumentando seu humor.
        """
        if not self.pet:
            c_print("Voce nao tem um pet para alimentar.", Fore.YELLOW)
            return

        if self.remove_item(item_comida):
            bonus_humor = 15
            comidas_favoritas = PET_FOODS.get(self.pet["tipo"], [])
            if item_comida in comidas_favoritas:
                bonus_humor = 30
                c_print(f"{self.pet['nome']} adorou a comida!", Fore.MAGENTA)
            else:
                c_print(f"{self.pet['nome']} comeu {item_comida}.", Fore.MAGENTA)
            
            self.pet["humor"] = min(100, self.pet["humor"] + bonus_humor)
        else:
            # Este caso não deve acontecer se a lógica do menu estiver correta
            c_print(f"Voce nao tem {item_comida} no inventario.", Fore.RED)


    def ganhar_xp_pet(self, quantidade):
        """
        Adiciona XP ao pet e verifica se ele subiu de nível.
        """
        if not self.pet:
            return
            
        self.pet["xp"] += quantidade
        xp_necessario = self.pet["level"] * 10 # Ex: Nível 1 precisa de 10 XP, Nível 2 de 20 XP, etc.
        
        if self.pet["xp"] >= xp_necessario:
            self.pet["level"] += 1
            self.pet["xp"] = 0 # Reseta o XP para o próximo nível
            c_print(f"[LVL UP!] {self.pet['nome']} parece mais forte e experiente! Ele atingiu o Nivel {self.pet['level']}!", Fore.MAGENTA)

    def get_dano_pet(self):
        """
        Calcula o dano do pet com base no tipo, nível e humor.
        """
        if not self.pet:
            return 0
        
        stats = PET_STATS.get(self.pet["tipo"])
        if not stats:
            return 0
            
        dano_base = stats["dano_base"]
        bonus_nivel = (self.pet["level"] - 1) * 2 # +2 de dano por nível
        # O humor afeta o dano. Humor baixo (0) = 50% do dano. Humor alto (100) = 100% do dano.
        modificador_humor = 0.5 + (self.pet["humor"] / 200) 
        
        return int((dano_base + bonus_nivel) * modificador_humor)

    def get_item_weight(self, item):
        return self.ALL_ITEMS.get(item, {}).get("weight", 1.0)

    def get_current_weight(self):
        total_weight = 0
        for item, qty in self.inventory.items():
            total_weight += self.get_item_weight(item) * qty
        return total_weight

    def add_item(self, item, qty=1):
        item_weight = self.get_item_weight(item)
        if self.get_current_weight() + (item_weight * qty) <= self.max_weight:
            self.inventory[item] = self.inventory.get(item, 0) + qty
            return True
        else:
            c_print("A sua mochila esta muito pesada.", Fore.YELLOW)
            return False

    def remove_item(self, item, qty=1):
        if self.inventory.get(item, 0) >= qty:
            self.inventory[item] -= qty
            if self.inventory[item] == 0:
                del self.inventory[item]
            return True
        return False

    def has_items(self, recipe):
        return all(self.inventory.get(k, 0) >= v for k, v in recipe.items())

    def apply_effects(self, effects):
        self.hunger += effects.get("hunger", 0)
        self.thirst += effects.get("thirst", 0)
        self.health += effects.get("health", 0)

    def age_from_time(self):
        years = (self.current_date - self.start_date).days // 365
        return 18 + years

    def aumentar_habilidade(self, habilidade, valor=1):
        if hasattr(self, habilidade):
            setattr(self, habilidade, getattr(self, habilidade) + valor)
            c_print(f"[+] Sua habilidade de {habilidade} aumentou!", Fore.CYAN)

    def update_time(self, hours=1):
        old_age = self.age
        self.current_date += timedelta(hours=hours)
        
        # Taxas de declínio base
        # FOME E SEDE MAIS LENTAS
        fome_decay = 1 * hours
        sede_decay = 1 * hours

        # --- EFEITOS DO CLIMA ---
        if self.clima == "Quente":
            sede_decay *= 1.5  # 50% mais sede
        elif self.clima == "Frio":
            fome_decay *= 1.5  # 50% mais fome
        elif self.clima == "Chuvoso":
            # Sem um bom abrigo, a chuva causa perda de saúde e chance de doença
            if self.abrigo_nivel < 2:
                self.health -= 1 * hours
            if self.abrigo_nivel < 1 and random.random() < 0.1: # 10% de chance de ficar doente sem abrigo
                if not self.doenca:
                    self.doenca = True
        
        self.hunger -= fome_decay
        self.thirst -= sede_decay

        # Humor do pet diminui com o tempo
        if self.pet:
            self.pet["humor"] = max(0, self.pet["humor"] - (1 * hours))

        # Efeitos de status negativos
        if self.doenca:
            self.health -= 4 * hours
        if self.veneno:
            self.health -= 6 * hours

        self.age = self.age_from_time()
        if self.age > old_age:
            self.check_age_milestone()

        if self.hunger <= 0: self.health -= 10
        if self.thirst <= 0: self.health -= 15
        
        if self.health <= 0 and self.vivo:
            self.vivo = False
            # Define a causa da morte com base na prioridade
            if self.thirst <= 0:
                self.causa_morte = "morreu de sede"
            elif self.hunger <= 0:
                self.causa_morte = "morreu de fome"
            elif self.veneno:
                self.causa_morte = "sucumbiu ao veneno"
            elif self.doenca:
                self.causa_morte = "sucumbiu a uma doença"
            elif self.clima == "Tempestade":
                self.causa_morte = "foi pego em uma tempestade mortal"
            else:
                self.causa_morte = "morreu de causas desconhecidas"
    
    def check_age_milestone(self):
        if self.age == 20 and not self.age_milestones_met[20]:
            c_print("\n[IDADE] Voce fez 20 anos!", Fore.YELLOW)
            self.health += 15
            self.age_milestones_met[20] = True
        elif self.age == 25 and not self.age_milestones_met[25]:
            c_print("\n[IDADE] Voce fez 25 anos.", Fore.YELLOW)
            self.health -= 5
            self.age_milestones_met[25] = True
        elif self.age == 28 and not self.age_milestones_met[28]:
            c_print("\n[IDADE] Voce fez 28 anos. Uma estranha sensacao toma conta de voce...", Fore.CYAN)
            self.age_milestones_met[28] = True
    
    def _create_progress_bar(self, current, max_val, length=10, fill_char='=', empty_char='-', cor=Fore.WHITE):
        current = max(0, current)
        percent = current / max_val
        filled_length = int(length * percent)
        bar = f"{cor}{fill_char * filled_length}{Style.RESET_ALL}{empty_char * (length - filled_length)}"
        return f"[{bar}] {current}/{max_val}"

    def status(self):
        clear()
        print(f"\n[DATA] {self.current_date.strftime('%d/%m/%Y %H:%M')} | Idade: {self.age}")
        print(f"[LOCAL] {self.location} | Clima: {self.clima}")
        
        health_bar = self._create_progress_bar(self.health, 100, cor=Fore.GREEN)
        hunger_bar = self._create_progress_bar(self.hunger, 100, cor=Fore.YELLOW)
        thirst_bar = self._create_progress_bar(self.thirst, 100, cor=Fore.CYAN)
        
        print(f"[+] Saude: {health_bar}")
        print(f"[=] Fome:  {hunger_bar}")
        print(f"[o] Sede:  {thirst_bar}")
        
        print(f"\n--- Habilidades ---")
        print(f"Forca: {self.forca}")
        print(f"Inteligencia: {self.inteligencia}")
        print(f"Sobrevivencia: {self.sobrevivencia}")

        print(f"\n--- Condicao ---")
        print(f"Abrigo: Nivel {self.abrigo_nivel}")
        
        doenca_status = f"{Fore.RED}Sim{Style.RESET_ALL}" if self.doenca else "Nao"
        veneno_status = f"{Fore.RED}Sim{Style.RESET_ALL}" if self.veneno else "Nao"
        print(f"Doenca: {doenca_status} | Veneno: {veneno_status}")
        
        print(f"Peso: {self.get_current_weight():.2f}/{self.max_weight}")
        
        if self.pet:
            pet_humor_bar = self._create_progress_bar(self.pet['humor'], 100, cor=Fore.MAGENTA)
            print(f"\n--- Companheiro ---")
            print(f"Pet: {self.pet['nome']} ({self.pet['tipo'].capitalize()}) (Nivel {self.pet['level']}) | Humor: {pet_humor_bar}")

        progress_bar = f"[{Fore.YELLOW}{'=' * self.story_progress}{Style.RESET_ALL}{'-' * (5 - self.story_progress)}]"
        print(f"\n[HISTORIA] Progresso: {self.story_progress}/5 {progress_bar}")