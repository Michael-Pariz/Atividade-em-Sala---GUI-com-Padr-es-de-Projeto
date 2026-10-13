"""
fabrica.py - Padrão FACTORY METHOD aplicado à criação dos pacientes.


PADRÃO 1: FACTORY METHOD

NOME:
    Factory Method (padrão de criação, GoF).

PROBLEMA:
    A tela tem um combobox com a espécie (Cachorro, Gato, Coelho). Sem o
    padrão, o ouvinte do botão precisaria de um if/elif por espécie
    ("se for Gato faz Gato(...), senão se for Cachorro...") e importaria
    todas as subclasses de Animal. Cada espécie nova obrigaria a mexer na
    tela, que deveria só cuidar de interface.

SOLUÇÃO:
    Criei a classe abstrata CriadorAnimal com o método-fábrica
    criar_animal(). Cada subclasse (CriadorCachorro, CriadorGato,
    CriadorCoelho) decide qual Animal concreto instanciar. O método
    registrar() da classe base (operação que usa o método-fábrica) cria o
    animal e já o cadastra na clínica. A tela só pede um criador pelo
    nome da espécie em CRIADORES e chama registrar(), sem saber qual
    classe concreta saiu dali.

CONSEQUÊNCIAS NO MEU CÓDIGO:
    (+) tela.py não importa Cachorro, Gato nem Coelho e não tem nenhum
        if por espécie. Para adicionar "Coelho" só criei a classe em
        dominio.py e um criador aqui; a tela não mudou (o combobox lê as
        chaves de CRIADORES).
    (+) Cada espécie tem regras de validação próprias (peso e idade
        máximos) e o criador garante que o objeto certo é instanciado,
        então a regra certa é aplicada.
    (-) Para cada espécie existe uma classe a mais (CriadorX). Num
        domínio tão pequeno isso é um pouco "verboso"; um dicionário
        espécie -> classe resolveria com menos código, mas perderia o
        ponto de extensão registrar().
    (-) Uma espécie que não está em CRIADORES precisa ser tratada:
        obter_criador() lança EspecieInvalidaError.

"""

from abc import ABC, abstractmethod

from dominio import Cachorro, Gato, Coelho, EspecieInvalidaError


class CriadorAnimal(ABC):
    """Criador abstrato: define o método-fábrica."""

    @abstractmethod
    def criar_animal(self, nome, idade, peso, telefone):
        """Método-fábrica: cada subclasse devolve o Animal concreto."""

    def registrar(self, clinica, nome, idade, peso, telefone):
        """Operação comum que usa o método-fábrica.

        Se algum dado for inválido, a exceção do domínio sobe daqui
        direto para quem chamou (a tela), sem ser engolida.
        """
        animal = self.criar_animal(nome, idade, peso, telefone)
        clinica.cadastrar(animal)
        return animal


class CriadorCachorro(CriadorAnimal):
    def criar_animal(self, nome, idade, peso, telefone):
        return Cachorro(nome, idade, peso, telefone)


class CriadorGato(CriadorAnimal):
    def criar_animal(self, nome, idade, peso, telefone):
        return Gato(nome, idade, peso, telefone)


class CriadorCoelho(CriadorAnimal):
    def criar_animal(self, nome, idade, peso, telefone):
        return Coelho(nome, idade, peso, telefone)


# Catálogo de criadores: a tela usa as chaves para preencher o combobox.
CRIADORES = {
    "Cachorro": CriadorCachorro(),
    "Gato": CriadorGato(),
    "Coelho": CriadorCoelho(),
}


def obter_criador(especie):
    try:
        return CRIADORES[especie]
    except KeyError:
        raise EspecieInvalidaError("Escolha uma espécie da lista.") from None
