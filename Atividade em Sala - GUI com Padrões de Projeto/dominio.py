"""
dominio.py - Classes de domínio da Clínica Veterinária "PetVida".

Aqui ficam TODAS as regras de validação. A tela nunca valida nada: ela só
repassa o texto digitado e, se algo estiver errado, o objeto de domínio
lança uma exceção específica que a tela captura e mostra ao usuário.
"""

import re



# Hierarquia de exceções do domínio
class DadoInvalidoError(Exception):
    """Base para qualquer dado recusado pelo domínio.

    Guarda o nome do campo para que a tela saiba onde colocar o foco,
    sem precisar conhecer a regra que falhou.
    """

    def __init__(self, campo, mensagem):
        super().__init__(mensagem)
        self.campo = campo


class NomeInvalidoError(DadoInvalidoError):
    def __init__(self, mensagem):
        super().__init__("nome", mensagem)


class IdadeInvalidaError(DadoInvalidoError):
    def __init__(self, mensagem):
        super().__init__("idade", mensagem)


class PesoInvalidoError(DadoInvalidoError):
    def __init__(self, mensagem):
        super().__init__("peso", mensagem)


class TelefoneInvalidoError(DadoInvalidoError):
    def __init__(self, mensagem):
        super().__init__("telefone", mensagem)


class EspecieInvalidaError(DadoInvalidoError):
    def __init__(self, mensagem):
        super().__init__("especie", mensagem)


class PacienteDuplicadoError(DadoInvalidoError):
    def __init__(self, mensagem):
        super().__init__("nome", mensagem)



# Animal e subclasses
class Animal:
    """Paciente da clínica. Valida os próprios dados nas properties."""

    ESPECIE = "Animal"
    IDADE_MAXIMA = 30      # anos
    PESO_MAXIMO = 100.0    # kg

    def __init__(self, nome, idade, peso, telefone_tutor):
        # Os setters fazem a validação, então o objeto nunca nasce inválido.
        self.nome = nome
        self.idade = idade
        self.peso = peso
        self.telefone_tutor = telefone_tutor

    # nome 
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise NomeInvalidoError("O nome do animal é obrigatório.")
        if len(valor) < 2 or len(valor) > 40:
            raise NomeInvalidoError("O nome deve ter entre 2 e 40 caracteres.")
        if not re.fullmatch(r"[A-Za-zÀ-ÿ' ]+", valor):
            raise NomeInvalidoError("O nome deve conter apenas letras e espaços.")
        self._nome = valor.title()

    # idade 
    @property
    def idade(self):
        return self._idade

    @idade.setter
    def idade(self, valor):
        try:
            idade = int(str(valor).strip())
        except ValueError:
            raise IdadeInvalidaError("A idade deve ser um número inteiro de anos.") from None
        if idade < 0 or idade > self.IDADE_MAXIMA:
            raise IdadeInvalidaError(
                f"A idade de um {self.ESPECIE.lower()} deve estar entre 0 e "
                f"{self.IDADE_MAXIMA} anos."
            )
        self._idade = idade

    #  peso 
    @property
    def peso(self):
        return self._peso

    @peso.setter
    def peso(self, valor):
        texto = str(valor).strip().replace(",", ".")  # aceita 4,5 e 4.5
        try:
            peso = float(texto)
        except ValueError:
            raise PesoInvalidoError("O peso deve ser um número (ex.: 4,5).") from None
        if peso <= 0 or peso > self.PESO_MAXIMO:
            raise PesoInvalidoError(
                f"O peso de um {self.ESPECIE.lower()} deve ser maior que 0 e "
                f"no máximo {self.PESO_MAXIMO:g} kg."
            )
        self._peso = round(peso, 2)

    # telefone 
    @property
    def telefone_tutor(self):
        return self._telefone_tutor

    @telefone_tutor.setter
    def telefone_tutor(self, valor):
        digitos = re.sub(r"\D", "", str(valor))  # ignora ( ) - e espaços
        if len(digitos) not in (10, 11):
            raise TelefoneInvalidoError(
                "O telefone do tutor deve ter DDD + número (10 ou 11 dígitos)."
            )
        self._telefone_tutor = digitos

    def telefone_formatado(self):
        d = self._telefone_tutor
        return f"({d[:2]}) {d[2:-4]}-{d[-4:]}"

    def __str__(self):
        peso = f"{self.peso:g}".replace(".", ",")
        return (f"{self.ESPECIE} {self.nome} | {self.idade} ano(s) | "
                f"{peso} kg | tutor {self.telefone_formatado()}")


class Cachorro(Animal):
    ESPECIE = "Cachorro"
    IDADE_MAXIMA = 25
    PESO_MAXIMO = 90.0


class Gato(Animal):
    ESPECIE = "Gato"
    IDADE_MAXIMA = 30
    PESO_MAXIMO = 15.0


class Coelho(Animal):
    ESPECIE = "Coelho"
    IDADE_MAXIMA = 15
    PESO_MAXIMO = 8.0


# Clínica: guarda os pacientes e avisa os interessados (Sujeito do Observer)
class Clinica:
    """Cadastro de pacientes. Também é o SUJEITO do padrão Observer
    (documentação completa do padrão está em observador.py)."""

    def __init__(self, nome):
        self.nome = nome
        self._pacientes = []
        self._observadores = []

    # parte do Observer 
    def adicionar_observador(self, observador):
        if observador not in self._observadores:
            self._observadores.append(observador)

    def remover_observador(self, observador):
        self._observadores.remove(observador)

    def _notificar(self, animal):
        for obs in self._observadores:
            obs.paciente_cadastrado(self, animal)

    # regras da clínica 
    def cadastrar(self, animal):
        for p in self._pacientes:
            if (p.nome == animal.nome and p.ESPECIE == animal.ESPECIE
                    and p.telefone_tutor == animal.telefone_tutor):
                raise PacienteDuplicadoError(
                    f"{animal.ESPECIE} {animal.nome} já está cadastrado para "
                    f"este tutor."
                )
        self._pacientes.append(animal)
        self._notificar(animal)

    @property
    def pacientes(self):
        return list(self._pacientes)  # cópia: ninguém mexe na lista por fora

    def total(self):
        return len(self._pacientes)
