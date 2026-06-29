from entities.user import User
from entities.event import Event
from entities.room import Room
from entities.session import Session
from entities.ticket import Ticket

from datetime import date, datetime, timedelta
import os


# Caminho base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

path_room_1 = os.path.join(
    BASE_DIR,
    "storage",
    "rooms",
    "room1.txt"
)


# Usuário
user = User(
    "João",
    date(2007, 6, 20),
    "123.456.789-00",
    "(54)99999-9999"
)


# Evento
event = Event(
    "Vingadores: Ultimato",
    181
)


# Sala
room = Room(path_room_1)


# Sessão (daqui 2 horas)
session = Session(
    event,
    room,
    datetime.now() + timedelta(hours=2),
    35.00
)


# Escolhe um assento da sala
seat = room.layout[0][0]

# Reserva o assento
session.reserve_seat(seat)


# Gera o ingresso
ticket = Ticket(
    user,
    session,
    seat,
    session.price
)


def menu():
    while True:
        print("\n====== INGRESSO.COM ======")
        print("1 - Mostrar usuário")
        print("2 - Mostrar evento")
        print("3 - Mostrar sessão")
        print("4 - Mostrar assento")
        print("5 - Mostrar ingresso")
        print("6 - Mostrar sala")
        print("0 - Sair")

        option = input("Escolha uma opção: ")

        match option:
            case "1":
                print("\n=== Usuário ===")
                print(f"Nome: {user.name}")
                print(f"Idade: {user.age}")
                print(f"CPF: {user.cpf}")
                print(f"Telefone: {user.phone_number}")
                print(f"Estado: {user.state}")

            case "2":
                print("\n=== Evento ===")
                print(f"Nome: {event.name}")
                print(f"Duração: {event.duration} minutos")

            case "3":
                print("\n=== Sessão ===")
                print(f"Evento: {session.event.name}")
                print(f"Início: {session.start_time}")
                print(f"Preço: R$ {session.price:.2f}")

            case "4":
                print("\n=== Assento ===")
                print(f"Linha: {seat.row}")
                print(f"Coluna: {seat.column}")
                print(f"Status: {seat.status}")

            case "5":
                print("\n=== Ingresso ===")
                print(f"Cliente: {ticket.user.name}")
                print(f"Evento: {ticket.session.event.name}")
                print(f"Assento: {ticket.seat.row}-{ticket.seat.column}")
                print(f"Preço: R$ {ticket.price:.2f}")
                print(f"Status: {ticket.status}")
            case "6":
                print("=== Sala ===")
                print(room)
            case "0":
                print("Encerrando sistema...")
                break

            case _:
                print("Opção inválida!")

def main():
    menu()

if __name__ == "__main__":
    main()