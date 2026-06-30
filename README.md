# Sistema de Vendas de Ingressos - Raeder.com

Sistema de reserva e venda de ingressos para eventos (cinema, shows, eventos esportivos) com persistência em arquivos CSV. Desenvolvido em Python, com foco em modularidade e orientação a objetos.

## Funcionalidades

- Seleção de usuários cadastrados
- Visualização de sessões disponíveis com horário, preço e sala
- Exibição do mapa da sala com assentos disponíveis (🟩), acessíveis (♿) e ocupados (🟥)
- Reserva e compra de assentos em sessões futuras
- Geração de ticket com ID único e persistência
- Listagem de tickets de um usuário específico
- Visualização de todas as salas e seus layouts
- Operações de CRUD (criar usuário, evento e sessão | cancelar ticket)

## Estrutura do Projeto

```
.\
├── entities
│ ├── event_child
│ │  ├── movie_event.py
│ │  ├── music_show_event.py
│ │  └── sports_game_event.py
│ ├── user.py
│ ├── event.py
│ ├── event_factory.py
│ ├── room.py
│ ├── seat.py
│ ├── session.py
│ └── ticket.py
├── storage
│ ├── csv_manager.py
│ └── data
│   ├── users.csv
│   ├── events.csv
│   ├── sessions.csv
│   ├── rooms.csv
│   ├── tickets.csv
└── rooms
│   ├── sala1.txt
│   ├── sala2.txt
│   └── sala3.txt
├── main.py
└── README.md
```

text

### Entidades

- **User**: Representa um usuário com nome, CPF e e-mail.
- **Event**: Evento abstrato (filme, show, esporte) com atributos específicos.
- **EventFactory**: Fábrica para criar eventos a partir do CSV, conforme o tipo.
- **Room**: Sala com nome, arquivo de layout e matriz de assentos.
- **Seat**: Assento com posição (linha, coluna), acessibilidade e status (disponível, reservado, vendido).
- **Session**: Sessão de um evento em uma sala, com data/hora e preço.
- **Ticket**: Ingresso vinculado a um usuário, sessão, assento, com status (ativo, cancelado, usado).

## 💾 Persistência

Os dados são armazenados em arquivos CSV no diretório `storage/data/`. Os layouts das salas são arquivos de texto com matrizes numéricas:

- `0` = assento normal
- `4` = assento acessível
- outros números = corredor (sem assento)

O sistema carrega os dados na inicialização e salva alterações após cada compra.

## ⚙️ Configuração

1. Clone o repositório.
2. Certifique-se de que os arquivos CSV e de layout estão no local correto (veja estrutura acima).
3. Instale Python 3.8+ (nenhuma biblioteca externa necessária).

## ▶️ Como Executar

```bash
python main.py
```

O menu interativo será exibido no terminal.

## 📝 Exemplo de Uso

1.  Selecione um usuário (opção 1).

2.  Veja as sessões disponíveis (opção 2).

3.  Escolha uma sessão, visualize a sala e selecione um assento.

4.  Confirme a compra.

5.  Verifique os tickets do usuário (opção 4).

## 🧪 Dados de Exemplo

O projeto inclui dados de exemplo:

- Usuários: Mateus, João, Ana, Lucas

- Eventos: Interestelar, GRE-nal 445, Coldplay Live

- Salas: 3 salas com layouts diferentes

- Sessões: em datas futuras (ajuste conforme necessário)

## 📄 Licença

Este projeto é apenas para fins educacionais.

```

```
