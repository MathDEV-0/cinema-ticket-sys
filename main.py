from entities.user import User
from entities.event import Event
from entities.room import Room
from entities.session import Session
from entities.ticket import Ticket
from entities.event_factory import EventFactory
from entities.seat import  Seat
from entities.event_child.movie_event import MovieEvent
from entities.event_child.music_show_event import MusicShowEvent
from entities.event_child.sports_game_event import SportsGameEvent
from storage.csv_manager import CSVManager

from datetime import date, datetime, timedelta
import os
import copy

# Caminho base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


DATA_DIR = os.path.join(BASE_DIR, "storage", "data")
TICKETS_PATH = os.path.join(DATA_DIR, "tickets.csv")
USERS_PATH = os.path.join(DATA_DIR, "users.csv")
EVENTS_PATH = os.path.join(DATA_DIR, "events.csv")
SESSIONS_PATH = os.path.join(DATA_DIR, "sessions.csv")
ROOMS_PATH = os.path.join(DATA_DIR, "rooms.csv")

rooms = CSVManager.load(ROOMS_PATH, Room.from_dict)
users = CSVManager.load(USERS_PATH, User.from_dict)
events = CSVManager.load(EVENTS_PATH, EventFactory.from_dict)
sessions = CSVManager.load(SESSIONS_PATH, Session.from_dict)
tickets = CSVManager.load(TICKETS_PATH, Ticket.from_dict)


import copy

# Criar uma sala a partir da cópia de um arquivo Room, mas com os Tickets da sessão populados.
# Usei deepcopy porque preciso fazer uma duplicata exata, mas independente da referência na lista de Rooms
def build_session_room(session, rooms, tickets):
    base_room = next((r for r in rooms if r.id == session.room_id), None) # Procura ba  
    if not base_room:
        return None
    room_copy = copy.deepcopy(base_room)
    for ticket in tickets:
        if ticket.status in ["ativo", "vendido"] and ticket.session_id == session.id:
            try:
                seat = room_copy.get_seat(ticket.seat.label)
                seat.status = "vendido"
            except Exception as e:
                print(f"Erro ao marcar assento {ticket.seat.label}: {e}")
    return room_copy

for session in sessions:
    session.event = next((e for e in events if e.id == session.event_id), None)
    session.room = build_session_room(session, rooms,tickets)

    if session.event is None:
        print(f"AVISO: Sessão {session.id} não encontrou evento {session.event_id}")
    if session.room is None:
        print(f"AVISO: Sessão {session.id} não encontrou sala {session.room_id}")

# Associar ticket a usuário e sessão
for ticket in tickets:
    ticket.user = next((u for u in users if u.id == ticket.user_id), None)
    ticket.session = next((s for s in sessions if s.id == ticket.session_id), None)

for event in events:
    event.sessions = [s for s in sessions if s.event_id == event.id]
for room in rooms:
    room.sessions = [s for s in sessions if s.room_id == room.id]


current_user = None
current_session = None
current_ticket = None
current_seat = None


# Operações a nível de usuário
def select_user():
    global current_user
    print("\n=== USUÁRIOS ===")
    for i, u in enumerate(users):
        print(f"{i} - {u.name} | {u.cpf}")
    idx = int(input("Escolha o usuário: "))
    current_user = users[idx]
    print(f"Usuário selecionado: {current_user.name}")

def user_data():
    global current_user
    if not current_user:
        print("Selecione um usuário primeiro.")
        return
    
    print(f"Usuário selecionado: {current_user.name}")
    print(f"Idade: {current_user.age}")
    print(f"Telefone: {current_user.phone_number}")
    print(f"CPF: {current_user.cpf}")

def select_session_flow():
    global current_session, current_ticket, current_seat, tickets

    if not current_user:
        print("Selecione um usuário primeiro.")
        return

    print("\n=== SESSÕES DISPONÍVEIS ===")

    for i, s in enumerate(sessions):
        print(f"\n[{i}] {s.event.name}")
        print(f"    Início: {s.start_time}")
        print(f"    Preço: R$ {s.price:.2f}")

    try:
        idx = int(input("\nEscolha a sessão: "))
        if idx < 0 or idx >= len(sessions):
            print("Sessão inválida")
            return
    except ValueError:
        print("Entrada inválida")
        return

    
    current_session = sessions[idx]

    if not current_session.can_sell():
        print("A sessão já começou. Venda cancelada.")
        return

    print("\n=== SALA ===")
    print(current_session.room)

    seat_code = input("\nEscolha o assento (ex: A1): ")

    try:
        seat = current_session.room.get_seat(seat_code)
    except Exception as e:
        print(f"Erro: {e}")
        return

    confirm = input(f"Confirmar compra do assento {seat.label}? (s/n): ")

    if confirm.lower() != "s":
        print("Cancelado.")
        return

    try:
        current_session.reserve_seat(seat)
        current_seat = seat

        if current_seat.sell():
            current_seat.sell()
        # garante ID seq
        ticket = Ticket(
            id=CSVManager.get_next_id(TICKETS_PATH),
            user=current_user,
            session=current_session,
            seat=seat,
            price=current_session.price
        )
    
        current_ticket = ticket
        tickets.append(ticket)

        CSVManager.save(
            TICKETS_PATH,
            ["id", "user_id", "session_id", "seat_row", "seat_col", "price", "status"],
            tickets
        )
        
        print("Compra realizada com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")

def show_current_seat():
    if not current_seat:
        print("Nenhum assento selecionado.")
        return

    print("\n=== ASSENTO ===")
    print(f"Assento: {current_seat.label}")
    print(f"Status: {current_seat.status}")

def show_user_tickets():
    if not current_user:
        print("Selecione um usuário primeiro.")
        return

    print("\n=== TICKETS ===")

    user_tickets = [
        t for t in tickets
        if t.user.id == current_user.id
    ]

    if not user_tickets:
        print("Nenhum ticket encontrado.")
        return

    for t in user_tickets:
        print("\n---")
        print(f"Evento: {t.session.event.name}")
        print(f"Assento: {t.seat.label}")
        print(f"Status: {t.status}")
        print(f"Preço: R$ {t.price}")

def show_all_rooms():
    print("\n=== SALAS DISPONÍVEIS ===")
    for room in rooms:
        print(f"\nSala: {room.name} (ID: {room.id})")
        print(room)

#Operações a nível de CRUD
def create_user():
    global users

    print("\n=== CRIAR USUÁRIO ===")

    name = input("Nome: ")
    birthday_str = input("Data de nascimento (YYYY-MM-DD): ")
    cpf = input("CPF: ")
    phone = input("Telefone: ")

    birthday = datetime.strptime(birthday_str, "%Y-%m-%d").date()

    new_user = User(
        id=CSVManager.get_next_id(USERS_PATH),
        name=name,
        birthday=birthday,
        cpf=cpf,
        phone_number=phone
    )

    users.append(new_user)

    CSVManager.save(
        USERS_PATH,
        ["id", "name", "birthday", "cpf", "phone_number", "created_at"],
        users
    )

    print("Usuário criado com sucesso!")

def create_event():
    global events

    print("\n=== CRIAR EVENTO ===")

    print("Tipo de evento:")
    print("1 - Movie")
    print("2 - Music")
    print("3 - Sports")
    print("4 - Generic")

    option = input("Escolha o tipo: ")

    name = input("Nome do evento: ")
    duration = int(input("Duração (min): "))

    event_id = CSVManager.get_next_id(EVENTS_PATH)

    if option == "1":
        genre = input("Gênero: ")
        age_rating = int(input("Classificação indicativa: "))

        new_event = MovieEvent(
            id=event_id,
            name=name,
            duration=duration,
            genre=genre,
            age_rating=age_rating
        )

    elif option == "2":
        artist = input("Artista: ")
        tour = input("Turnê: ")

        new_event = MusicShowEvent(
            id=event_id,
            name=name,
            duration=duration,
            artist=artist,
            tour=tour
        )

    elif option == "3":
        home_team = input("Time da casa: ")
        away_team = input("Time visitante: ")
        championship = input("Campeonato: ")

        new_event = SportsGameEvent(
            id=event_id,
            name=name,
            duration=duration,
            home_team=home_team,
            away_team=away_team,
            championship=championship
        )

    else:
        new_event = Event(
            id=event_id,
            name=name,
            duration=duration,
            event_type="generic"
        )

    events.append(new_event)

    CSVManager.save(
        EVENTS_PATH,
        [
            "id",
            "name",
            "duration",
            "event_type",
            "genre",
            "age_rating",
            "artist",
            "tour",
            "home_team",
            "away_team",
            "championship"
        ],
        events
    )

    print("Evento criado com sucesso!")

def create_session():
    global sessions

    print("\n=== CRIAR SESSÃO ===")
    # mostra eventos
    for i, e in enumerate(events):
        print(f"{i} - {e.name}")
    event_idx = int(input("Escolha o evento: "))
    event = events[event_idx]
    # mostra salas
    for i, r in enumerate(rooms):
        print(f"{i} - {r.name}")

    room_idx = int(input("Escolha a sala: "))
    room = rooms[room_idx]
    start_str = input("Data/hora (YYYY-MM-DD HH:MM): ")
    start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
    price = float(input("Preço: "))

    new_session = Session(
        id=CSVManager.get_next_id(SESSIONS_PATH),
        event_id=event.id,
        room_id=room.id,
        start_time=start_time,
        price=price
    )

    new_session.event = event
    new_session.room = room
    
    sessions.append(new_session)

    CSVManager.save(
        SESSIONS_PATH,
        ["id", "event_id", "room_id", "start_time", "price"],
        sessions
    )

    print("Sessão criada com sucesso!")

def cancel_ticket():
    global tickets

    print("\n=== CANCELAR TICKET ===")
    if not current_user:
        print("Selecione um usuário primeiro.")
        return
    user_tickets = [t for t in tickets if t.user.id == current_user.id]
    if not user_tickets:
        print("Nenhum ticket encontrado.")
        return
    for i, t in enumerate(user_tickets):
        print(f"{i} - {t.session.event.name} | {t.seat.label} | {t.status}")

    idx = int(input("Escolha o ticket: "))
    ticket = user_tickets[idx]

    ticket.status = "cancelado"
    if ticket.session and ticket.session.room:
        seat = ticket.session.room.get_seat(ticket.seat.label)
        seat.status = "disponível"

    CSVManager.save(
        TICKETS_PATH,
        ["id", "user_id", "session_id", "seat_row", "seat_col", "price", "status"],
        tickets
    )

    print("Ticket cancelado com sucesso!")

def menu():
    while True:
        print("\n====== RAEDER.COM ======")
        print("1 - Selecionar usuário")
        print("2 - Ver sessões disponíveis")
        print("3 - Mostrar assento atual")
        print("4 - Ver tickets do usuário")
        print("5 - Ver todas as salas")
        print("6 - Informações do usuário")
        print("======== ADMIN ========")
        print("7 - Criar usuário")
        print("8 - Criar evento")
        print("9 - Criar sessão")
        print("10 - Cancelar ticket")
        print("0 - Sair")

        option = input("Escolha uma opção: ")

        match option:
            case "1":
                select_user()

            case "2":
                select_session_flow()

            case "3":
                show_current_seat()

            case "4":
                show_user_tickets()

            case "5":
                show_all_rooms()

            case "6":
                user_data()

            case "7":
                create_user()

            case "8":
                create_event()

            case "9":
                create_session()

            case "10":
                cancel_ticket()

            case "0":
                break

            case _:
                print("Opção inválida")


def main():
    menu()


if __name__ == "__main__":
    main()