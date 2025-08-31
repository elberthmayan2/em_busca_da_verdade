# Em Busca da Verdade

> **RPG de sobrevivência em Python**. Você acorda em um mundo devastado e precisa lidar com **fome**, **sede**, **inimigos** e **mudanças climáticas**. A jornada começa em **06/12/1994**, aos **18 anos**. **Sobreviva até os 30** para recuperar suas memórias — e descobrir a verdade.

---

## 🎮 Destaques do Jogo

* **Narrativa + Tela Inicial**: introdução à história e menu com escolhas iniciais.
* **Inventário Completo**: gerencie itens, consuma recursos e use o sistema de *crafting*.
* **Combate e Sobrevivência**: enfrente inimigos, resista ao clima e ao passar do tempo.
* **API de Save/Load Local**: progresso salvo em `data/savegame.json` usando JSON.

---

## 🧠 Como funciona o Save/Load

* **Gerenciamento de estado**: estatísticas do jogador, inventário e progresso da história.
* **Persistência automática**: ao iniciar, o jogo detecta *save* existente e oferece continuar.
* **Tecnologia**: JSON + bibliotecas padrão do Python (sem dependências complexas).

---

## 🛠️ Tecnologias

* Python 3.x
* [colorama](https://pypi.org/project/colorama/)

---

## ▶️ Como executar

### Opção 1 — Executável (Windows)

1. Baixe/clique em `dist/main.exe`.
2. Execute e siga as instruções no console.

> Observação: o *save* será criado/atualizado em `data/savegame.json`.

### Opção 2 — Rodar pelo código-fonte

1. Instale o Python 3.x.
2. (Opcional) Crie e ative um *virtualenv*.
3. Instale dependências:

   ```bash
   pip install -r requirements.txt
   ```
4. Rode o jogo:

   ```bash
   python main.py
   ```

---

## 📦 Gerar o executável (PyInstaller)

> Gere um `.exe` autônomo incluindo a pasta `data/` (Windows).

```bash
pip install -r requirements.txt
pip install pyinstaller

# Na raiz do projeto
pyinstaller \
  --onefile \
  --name main \
  --add-data "data;data" \
  main.py
```

* O executável final ficará em `dist/main.exe`.
* Se usar Linux/macOS, troque `--add-data "data;data"` por `--add-data "data:data"`.

---

## 🗂️ Estrutura do Projeto

```
em-busca-da-verdade/
├── data/
│   ├── consumables.json
│   ├── enemies.json
│   ├── items.json
│   ├── recipes_cooking.json
│   ├── recipes_craft.json
│   └── savegame.json
├── dist/
│   └── main.exe
├── main.py
├── player.py
├── menus.py
├── narrativa.py
├── savegame.py
├── utils.py
├── path_handler.py
└── requirements.txt
```

**Arquivos principais**

* `main.py`: ponto de entrada do jogo.
* `player.py`: status do jogador (fome, sede, idade, etc.).
* `menus.py`: navegação e escolhas do usuário.
* `narrativa.py`: textos e eventos da história.
* `savegame.py`: leitura/escrita do `savegame.json`.
* `utils.py`: funções auxiliares (ex.: validação e formatação).
* `path_handler.py`: resolve caminhos (execução via `.py` ou `.exe`).

---

## 🕹️ Controles & Loop de jogo

* **Menu inicial** → iniciar novo jogo / continuar / sair.
* **Ações** → explorar, lutar, coletar, cozinhar, craftar, gerenciar inventário.
* **Passagem do tempo** → envelhecimento, clima e eventos impactam status.

> Dica: administre **comida** e **água** antes de enfrentar combates longos.

---

##  Dados de jogo (JSON)

* `items.json`: itens gerais (materiais, ferramentas, etc.).
* `consumables.json`: consumíveis (efeitos de fome/sede/saúde).
* `enemies.json`: atributos e comportamento básico dos inimigos.
* `recipes_craft.json`: receitas de *crafting* (entrada → saída).
* `recipes_cooking.json`: receitas de cozimento (cru → preparado).

---

## ❓ Perguntas frequentes (FAQ)

**Onde fica o arquivo de *save*?**
Em `data/savegame.json` (criado automaticamente na primeira execução).

**Posso resetar o progresso?**
Sim. Exclua `data/savegame.json` ou use a opção “Novo Jogo”.

**O executável fecha imediatamente. E agora?**
Execute pelo Terminal para ver o erro:

```bash
./dist/main.exe
```

Verifique se a pasta `data/` foi copiada junto do `.exe`.

---

## 📌 Roadmap (Ideias Futuras)

* Dificuldades configuráveis.
* Eventos climáticos dinâmicos por região.
* *Logs* de combate detalhados.
* *Achievements* e *endings* alternativos.

---

## 👥 Equipe

* Elberth Mayan
* Daiane Botelho
* Lais
* Isaque Felix
* Yasmin


