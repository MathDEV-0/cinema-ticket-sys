from datetime import date
from utils.cpf import CPF
from utils.ddd import DDD

class User:

    def __init__(self, id: int,name:str, birthday:date, cpf: str, phone_number: str):
        self.id = id
        self.name = name
        self.birthday = birthday
        self.cpf = cpf
        self.phone_number =  phone_number
        self.created_at  = date.today()


    def _calculate_age(self, birthday: date) -> int:
        today = date.today()
        age = today.year - birthday.year
        if (today.month, today.day) < (birthday.month, birthday.day):
            age -= 1

        return age
    
    @property
    def birthday(self) -> date:
        return self._birthday

    @birthday.setter
    def birthday(self, birthday: date):
        if self._calculate_age(birthday) < 18:
            raise ValueError("O usuário deve ser maior de 18 anos.")
        self._birthday = birthday

    @property
    def age(self) -> int:
        return self._calculate_age(self.birthday)

    @property
    def cpf(self) -> str:
        return f"{self._cpf[:3]}.{self._cpf[3:6]}.{self._cpf[6:9]}-{self._cpf[9:]}"
    
    @cpf.setter
    def cpf(self, cpf: str):
        self._cpf = CPF.validate(cpf)

    @property
    def phone_number(self) -> str:
        return f"({self._phone_number[:2]}) {self._phone_number[2:7]}-{self._phone_number[7:]}"
    
    @phone_number.setter
    def phone_number(self, phone_number: str):
        phone_number = (
            phone_number
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )

        if not phone_number.isdigit():
            raise ValueError("Telefone inválido")

        if len(phone_number) not in (10, 11):
            raise ValueError("Telefone deve ter DDD e número")

        ddd = phone_number[:2]

        if not DDD.is_valid(ddd):
            raise ValueError("DDD inválido")

        self._phone_number = phone_number

    @property
    def state(self):
        return DDD.get_state(self._phone_number[:2])

    # CSV utils para user
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "birthday": self.birthday.isoformat(),
            "cpf": self._cpf,
            "phone_number": self._phone_number,
            "created_at": self.created_at.isoformat()
        }

    @staticmethod
    def from_dict(data):
        return User(
            id=int(data["id"]),
            name=data["name"],
            birthday=date.fromisoformat(data["birthday"]),
            cpf=data["cpf"],
            phone_number=data["phone_number"]
        )