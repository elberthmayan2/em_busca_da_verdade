# API local que salva e carrega o progresso do jogo usando um arquivo JSON
import json
import os
from datetime import datetime

SAVE_FILE = "data/savegame.json"

def salvar_jogo(player):
    """Salva o progresso do jogador em JSON dentro de data/savegame.json"""
    data = {
        "name": player.name,
        "health": player.health,
        "hunger": player.hunger,
        "thirst": player.thirst,
        "age": player.age,
        "inventory": player.inventory,
        "location": player.location,
        "pet": player.pet,
        "clima": player.clima,
        "doenca": player.doenca,
        "veneno": player.veneno,
        "equipped_armor": player.equiped_armor,
        "has_fire": player.has_fire,
        "current_date": player.current_date.strftime("%Y-%m-%d %H:%M:%S"),
        "story_progress": player.story_progress,
        "forca": player.forca,
        "inteligencia": player.inteligencia,
        "sobrevivencia": player.sobrevivencia,
        "abrigo_nivel": player.abrigo_nivel
    }
    os.makedirs("data", exist_ok=True)
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print("💾 Jogo salvo com sucesso!")

def carregar_jogo():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data