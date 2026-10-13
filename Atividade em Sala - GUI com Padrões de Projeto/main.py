"""

Atividade em Sala - GUI com Padrões de Projeto
"Uma Tela que Não Tolera Erros"
Disciplina: Programação Orientada a Objetos
Aluno(a): Michael Pariz Pereira          RA: 2321653
Linguagem: Python 3 + Tkinter
Como rodar:  python main.py



PASSO 1 - PLANO

DOMÍNIO:
    Cadastro de pacientes de uma clínica veterinária ("Clínica PetVida").
    O recepcionista escolhe a espécie, digita nome, idade, peso e o
    telefone do tutor e clica em "Cadastrar".

CLASSES DE DOMÍNIO (dominio.py):
    - Animal (base) com as validações nas properties
    - Cachorro, Gato, Coelho (cada uma com idade e peso máximos próprios)
    - Clinica: guarda a lista de pacientes e recusa duplicados
    - Exceções: DadoInvalidoError (base) e suas filhas

CLASSES DA TELA (tela.py):
    - JanelaCadastro: monta a janela com grid e tem o ouvinte do botão
    - PainelPacientes, PainelContagem, BarraStatus: partes da tela que
      se atualizam sozinhas (observadores)

DADOS VALIDADOS E EXCEÇÃO DE CADA REGRA:
    | Dado      | Regra                                         | Exceção                 |
    |-----------|-----------------------------------------------|-------------------------|
    | espécie   | tem que estar na lista de criadores           | EspecieInvalidaError    |
    | nome      | obrigatório, 2 a 40 caracteres, só letras     | NomeInvalidoError       |
    | idade     | inteiro, de 0 até o máximo da espécie         | IdadeInvalidaError      |
    | peso      | número (aceita vírgula), > 0 e <= máx espécie | PesoInvalidoError       |
    | telefone  | DDD + número = 10 ou 11 dígitos               | TelefoneInvalidoError   |
    | cadastro  | mesmo nome+espécie+tutor não pode repetir     | PacienteDuplicadoError  |
    Todas herdam de DadoInvalidoError, que guarda o nome do campo, para
    a tela poder colocar o foco no campo errado sem conhecer a regra.

PADRÕES QUE PRETENDO APLICAR:
    1) Factory Method (fabrica.py): a tela recebe a espécie como texto
       do combobox e não quero um if/elif por espécie dentro do ouvinte.
       Cada criador sabe qual Animal instanciar.
    2) Observer (observador.py + Clinica): quando um paciente entra,
       a lista, o contador e a barra de status precisam mudar. Quero que
       o ouvinte do botão não precise saber disso.

PARA QUE PRETENDO USAR IA:
    Para revisar se os comentários dos padrões estão com os quatro
    elementos, tirar dúvida de layout com grid (sticky/weight) e sugerir
    casos de teste de entradas inválidas.


REGISTRO DAS PARADAS DO PASSO 2

    Parada dos 35 min: janela abria com o formulário em grid e o botão
        só fazia print dos campos. No prazo, sem ajuste de escopo.
    Parada dos 70 min: Animal validando e o ouvinte com try/except
        mostrando messagebox. Factory pronto; Observer ainda não.
        Ajuste de escopo: desisti de "editar/remover paciente" e de
        salvar em arquivo, para garantir o Observer e a autoavaliação.
        O PainelContagem entrou no fim, porque sobrou tempo.

"""

from tela import iniciar


if __name__ == "__main__":
    iniciar("Clínica PetVida")


"""

PASSO 3 - AUTOAVALIAÇÃO
Executei o programa e testei estas entradas (critério 6):
    Cachorro "rex", 5, "12,5", "(43) 99876-5432" -> cadastrado como "Rex"
    Gato "Mia", 3, 20 kg                         -> erro: peso máx. do gato é 15 kg
    nome vazio                                   -> erro: nome obrigatório
    nome "M1a"                                   -> erro: só letras
    idade "abc"                                  -> erro: idade inteira
    Coelho com 20 anos                           -> erro: coelho até 15 anos
    peso "-1"                                    -> erro: peso > 0
    telefone "1234"                              -> erro: DDD + número
    Cachorro "Rex" de novo, mesmo tutor          -> erro: já cadastrado
    Em todos os erros apareceu o diálogo, o foco foi para o campo errado
    e a janela continuou funcionando. Nas entradas válidas o paciente
    apareceu na lista, o contador da espécie subiu e a barra de status
    mudou.

CRITÉRIOS:
    1. Janela com layout sem coordenadas fixas ............ ATINGIDO
       (só grid com sticky/weight; a janela pode ser redimensionada)
    2. Classe de domínio que valida e lança exceção ....... ATINGIDO
       (Animal e Clinica)
    3. Ouvinte captura e traduz, sem repetir a regra ...... ATINGIDO
       (ao_cadastrar só tem try/except; nenhum if de validação na tela)
    4. Dois padrões aplicados ............................. ATINGIDO
       (Factory Method e Observer)
    5. Padrões documentados com os 4 elementos ............ ATINGIDO
       (cabeçalhos de fabrica.py e observador.py)
    6. Programa roda: válido chega ao domínio, inválido
       vira diálogo sem travar a janela .................... ATINGIDO
    Não atingi o que cortei no ajuste de escopo (editar/remover e
    persistência), mas isso não era critério.

TRECHO QUE DEU MAIS TRABALHO:
    Fazer a tela não validar nada. No começo eu fazia float(peso) no
    ouvinte e o ValueError estourava antes de chegar no domínio, ou seja,
    a regra "peso é número" estava na tela. Resolvi passando o texto cru
    para o Animal e fazendo a conversão dentro do setter, que transforma
    o ValueError em PesoInvalidoError (com "from None" para não poluir a
    mensagem). Outro ponto chato foi saber qual campo focar: resolvi
    colocando o atributo "campo" na exceção base.
    Também tive um susto com herança múltipla (ttk.LabelFrame +
    ObservadorClinica, que é ABC), mas funcionou porque o metaclass ABCMeta
    é filho de type.

AS CONSEQUÊNCIAS APARECERAM MESMO?
    Factory Method: sim. Coloquei o Coelho depois e só mexi em dominio.py
    e fabrica.py; o combobox já mostrou a espécie nova. O lado negativo
    também apareceu: três classes Criador quase iguais, de uma linha.
    Observer: sim. O PainelContagem foi adicionado no fim só com uma
    linha de registro, sem tocar no ouvinte. E o lado negativo também:
    quando a lista não atualizava (eu tinha esquecido de registrar o
    observador), demorei para achar o problema porque o ouvinte não
    mostra quem é avisado.

USO DE IA:
    Ajudou: a montar a tabela de regras/exceções, a lembrar do
    "from None" e a pensar em casos de teste que eu não teria testado
    (nome com número, peso com vírgula, telefone com máscara).
    Atrapalhou: sugeriu coisas além do escopo (persistência, mais
    padrões) que eu precisei cortar para caber no tempo, e precisei
    conferir se o texto das consequências batia com o MEU código e
    não com um exemplo genérico.

"""
