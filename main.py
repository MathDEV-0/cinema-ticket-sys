from entities.user import User
from entities.event import Event
from entities.room import Room
from entities.session import Session
from entities.ticket import Ticket
from entities.event_factory import EventFactory
from entities.seat import  Seat
from storage.csv_manager import CSVManager
from datetime import date, datetime, timedelta
import os

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

for session in sessions:
    session.event = next((e for e in events if e.id == session.event_id), None)
    session.room = next((r for r in rooms if r.id == session.room_id), None)
    if session.event is None:
        print(f"AVISO: Sessão {session.id} não encontrou evento {session.event_id}")
    if session.room is None:
        print(f"AVISO: Sessão {session.id} não encontrou sala {session.room_id}")

for ticket in tickets:
    ticket.user = next((u for u in users if u.id == ticket.user_id), None)
    ticket.session = next((s for s in sessions if s.id == ticket.session_id), None)

for ticket in tickets:
    if ticket.status == "ativo": 
        session = ticket.session
        if session and session.room:
            try:
                row = ticket.seat.row
                col = ticket.seat.column
                if row < len(session.room.layout) and col < len(session.room.layout[row]):
                    seat = session.room.layout[row][col]
                    if isinstance(seat, Seat):
                        seat.status = "vendido"
            except Exception as e:
                print(f"Erro ao atualizar assento: {e}")

for event in events:
    event.sessions = [s for s in sessions if s.event_id == event.id]
for room in rooms:
    room.sessions = [s for s in sessions if s.room_id == room.id]

# Vincular tickets com usuários e sessões
# Atualizar assentos das salas com base nos tickets já vendidos
for ticket in tickets:
    if ticket.status in ["ativo", "sold"]:
        session = ticket.session
        if session and session.room:
            try:
                seat = session.room.get_seat(ticket.seat.label)  # ou use row/column
                if seat.status == "disponível":
                    seat.sell()  
            except Exception as e:
                print(f"Erro ao marcar assento {ticket.seat.label}: {e}")

current_user = None
current_session = None
current_ticket = None
current_seat = None


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

def menu():
    while True:
        print("\n====== RAEDER.COM ======")
        print("1 - Selecionar usuário")
        print("2 - Ver sessões disponíveis")
        print("3 - Mostrar assento atual")
        print("4 - Ver tickets do usuário")
        print("5 - Ver todas as salas")
        print("6 - Informações do usuário")
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
            case "0":
                break

            case _:
                print("Opção inválida")


def main():
    menu()


if __name__ == "__main__":
    main()