"""
observador.py - Padrão OBSERVER: quem é avisado quando um paciente entra.


PADRÃO 2: OBSERVER
NOME:
    Observer (padrão comportamental, GoF), também chamado de
    Publish/Subscribe.

PROBLEMA:
    Quando um paciente é cadastrado, várias partes da janela precisam se
    atualizar: a lista de pacientes, o contador por espécie e a barra de
    status. Sem o padrão, o ouvinte do botão teria que lembrar de chamar
    cada uma delas na ordem certa (lista.insert, contador.config,
    status.config...), e a Clinica não teria como avisar ninguém se o
    cadastro viesse de outro lugar (por exemplo, dos dados de exemplo
    carregados na abertura).

SOLUÇÃO:
    A Clinica (em dominio.py) é o SUJEITO: mantém uma lista de
    observadores e, ao final de cadastrar(), chama
    paciente_cadastrado(clinica, animal) em cada um. ObservadorClinica
    é a interface. Os observadores concretos ficam na tela:
    PainelPacientes (Listbox), PainelContagem (contador por espécie) e
    BarraStatus. Cada um se atualiza sozinho.

CONSEQUÊNCIAS NO MEU CÓDIGO:
    (+) O ouvinte do botão ficou curto: só chama o criador e limpa o
        formulário. Ele não sabe quantos painéis existem.
    (+) Adicionei o PainelContagem depois que o resto já funcionava e
        não precisei mexer no ouvinte nem na Clinica, só registrar o
        observador em montar().
    (+) dominio.py não importa tkinter: a Clinica conversa com uma
        interface abstrata, então dá para testar o domínio sem janela.
    (-) O fluxo ficou menos óbvio: lendo o ouvinte do botão não dá para
        ver que a lista muda. Tive que procurar quem estava registrado.
    (-) A ordem de notificação depende da ordem de registro; se um
        observador lançar exceção, os seguintes não são avisados (não
        tratei isso porque os meus observadores só mexem em widgets).
    (-) Só avisa cadastro novo. Se um dia houver "remover paciente",
        a interface precisa ganhar outro método.

"""

from abc import ABC, abstractmethod


class ObservadorClinica(ABC):
    """Interface de quem quer ser avisado sobre a clínica."""

    @abstractmethod
    def paciente_cadastrado(self, clinica, animal):
        """Chamado pela Clinica logo depois de um cadastro com sucesso."""
