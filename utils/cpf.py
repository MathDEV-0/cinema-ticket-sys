class CPF:
    @staticmethod
    def validate(cpf: str) -> str:
        cpf = cpf.replace(".", "").replace("-", "")
        if not cpf.isdigit() or len(cpf) != 11:
            raise ValueError("CPF inválido")
        return cpf