Projeto Conexo
Rede social front-end. Uma plataforma para conectar pessoas, compartilhar ideias e criar comunidades, com foco em interatividade e em um ambiente acolhedor.

✨ Funcionalidades Principais
Feed Interativo & Notificações: compartilhe momentos e fique por dentro das novidades.

Chat em Tempo Real: converse de forma privada e segura com seus amigos.

Perfis e Busca: crie seu perfil, personalize-o e encontre outros usuários.

Comunidades e Workshops: participe de grupos e aprenda em eventos online.

Salas de Chamada Temáticas: conecte-se por voz em espaços seguros e segmentados.

Game Center Integrado: relaxe e divirta-se com um jogo casual na plataforma.

🧠 Como Funciona
Gerenciamento de Estado: a interação do usuário é gerenciada via JavaScript, manipulando o DOM para criar uma experiência dinâmica e responsiva.

Navegação Estática: o projeto utiliza múltiplos arquivos HTML para simular a navegação entre diferentes seções da plataforma (feed, chat, perfil, etc.).

Tecnologia: construído com tecnologias web padrões, sem a necessidade de frameworks complexos ou dependências de backend.

🛠️ Tecnologias
HTML5

CSS3

JavaScript (ES6+)

▶️ Como executar
Rodar pelo código-fonte
Instale o Git se ainda não tiver.

Clone o repositório para sua máquina local:

git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)

Navegue até a pasta do projeto:

cd conexo-main

Abra o arquivo index.html no seu navegador.

Dica: para uma melhor experiência, use a extensão Live Server no VS Code. Ela recarrega a página automaticamente a cada alteração, agilizando o desenvolvimento.

🗂️ Estrutura do Projeto
conexo-main/
├── css/
│   └── style.css
├── js/
│   ├── chat.js
│   ├── game.js
│   ├── main.js
│   └── ... (outros scripts)
├── images/
│   └── ... (imagens do projeto)
├── music/
│   └── ... (arquivos de áudio)
├── index.html
├── feed.html
├── chat.html
├── profile.html
├── game.html
└── ... (outras páginas HTML)

Arquivos principais

index.html: ponto de entrada da aplicação (página de login/cadastro).

feed.html: página principal após o login, onde o conteúdo é exibido.

chat.html: interface de mensagens diretas.

css/style.css: folha de estilo principal que define a aparência do projeto.

js/main.js / script.js: scripts principais que controlam a lógica geral e interatividade.

js/chat.js / game.js: scripts com a lógica específica de suas respectivas seções.

🕹️ Navegação & Uso
Menu Inicial → acesse pelo index.html para simular o login ou cadastro.

Ações → navegue pelas seções usando os links do menu: Feed, Chat, Comunidades, Jogo, etc.

Interatividade → as funcionalidades de cada página (enviar mensagem, jogar, etc.) são controladas pelos seus respectivos arquivos JavaScript.

Dica: explore as diferentes páginas HTML para visualizar todas as funcionalidades implementadas no front-end.

❓ Perguntas Frequentes (FAQ)
Preciso de um servidor para rodar o projeto?
Não. O projeto é 100% front-end e pode ser executado diretamente abrindo os arquivos HTML no navegador.

Os chats, posts e perfis são salvos de verdade?
Não. Como este é um protótipo focado na interface (UI/UX), os dados não são salvos em um banco de dados. Toda a informação é perdida ao recarregar a página.

Posso adaptar este projeto para usar um backend?
Sim! A estrutura HTML/CSS/JS é uma excelente base para ser integrada com um backend (Node.js, Python, etc.) e um banco de dados (Firebase, MongoDB, SQL) para torná-lo totalmente funcional.

📌 Roadmap (Ideias Futuras)
Integração com backend para persistência de dados.

Sistema de autenticação de usuários real.

Notificações push em tempo real.

Upload de imagens e arquivos no feed e no chat.

Otimização para dispositivos móveis (responsividade).

🤝 Como Contribuir
Contribuições são muito bem-vindas! Se quiser melhorar o projeto, siga os passos:

Faça um Fork do projeto.

Crie uma Branch para sua feature (git checkout -b feature/NovaFuncionalidade).

Commit suas mudanças (git commit -m 'Adiciona NovaFuncionalidade').

Faça o Push para a Branch (git push origin feature/NovaFuncionalidade).

Abra um Pull Request.
