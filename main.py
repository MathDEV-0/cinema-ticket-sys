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



def menu():
    while True:
        print("\n====== RAEDER.COM ======")
        print("1 - Ver evento")
        print("2 - Reservar assento")
        print("3 - Mostrar sessão")
        print("4 - Mostrar assento")
        print("5 - Mostrar ingresso")
        print("6 - Mostrar sala")
        print("0 - Sair")

        option = input("Escolha uma opção: ")

        match option:
            case "1":
                print("\n=== EVENTO ===")
                print(f"Nome: {session.event.name}")
                print(f"Duração: {session.event.duration} minutos")
                print(f"Início: {session.start_time}")
                print(f"Preço: R$ {session.price:.2f}")

                print("\nMapa da sala:")
                print(room)


            case "2":
                print(room)
                try:
                    seat = room.get_seat(
                        input("Escolha o assento (Ex: A1): ")
                    )

                    session.reserve_seat(seat)

                    print(f"Assento {seat.label} reservado!")

                except Exception as e:
                    print(e)

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
                pass
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