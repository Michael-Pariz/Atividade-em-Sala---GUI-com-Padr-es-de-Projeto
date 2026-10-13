"""
tela.py - Janela Tkinter da clínica PetVida.

Regra que segui: NENHUMA validação aqui. A tela só lê o texto dos campos,
entrega para o criador (Factory Method) e, se o domínio recusar, captura
a exceção e mostra a mensagem dela. Layout 100% com grid (sem place e sem
coordenadas fixas).
"""

import tkinter as tk
from tkinter import ttk, messagebox

from dominio import Clinica, DadoInvalidoError
from fabrica import CRIADORES, obter_criador
from observador import ObservadorClinica



# Observadores concretos (padrão Observer, ver observador.py)
class PainelPacientes(ttk.LabelFrame, ObservadorClinica):
    """Lista de pacientes cadastrados."""

    def __init__(self, master):
        super().__init__(master, text="Pacientes cadastrados", padding=8)
        self.lista = tk.Listbox(self, height=10, width=60)
        barra = ttk.Scrollbar(self, orient="vertical", command=self.lista.yview)
        self.lista.configure(yscrollcommand=barra.set)
        self.lista.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def paciente_cadastrado(self, clinica, animal):
        self.lista.insert(tk.END, str(animal))
        self.lista.see(tk.END)


class PainelContagem(ttk.LabelFrame, ObservadorClinica):
    """Quantidade de pacientes por espécie."""

    def __init__(self, master, especies):
        super().__init__(master, text="Por espécie", padding=8)
        self._rotulos = {}
        for linha, especie in enumerate(especies):
            ttk.Label(self, text=f"{especie}:").grid(row=linha, column=0, sticky="w")
            rotulo = ttk.Label(self, text="0", width=4, anchor="e")
            rotulo.grid(row=linha, column=1, sticky="e")
            self._rotulos[especie] = rotulo

    def paciente_cadastrado(self, clinica, animal):
        qtd = sum(1 for p in clinica.pacientes if p.ESPECIE == animal.ESPECIE)
        self._rotulos[animal.ESPECIE].configure(text=str(qtd))


class BarraStatus(ttk.Label, ObservadorClinica):
    """Rodapé com a última ação."""

    def __init__(self, master):
        super().__init__(master, text="Pronto.", relief="sunken", anchor="w",
                         padding=(6, 2))

    def paciente_cadastrado(self, clinica, animal):
        self.configure(text=f"{animal.ESPECIE} {animal.nome} cadastrado. "
                            f"Total na {clinica.nome}: {clinica.total()}.")


# Janela principal
class JanelaCadastro:
    def __init__(self, raiz, clinica):
        self.raiz = raiz
        self.clinica = clinica
        raiz.title(f"{clinica.nome} - Cadastro de Pacientes")
        raiz.minsize(620, 420)
        self.montar()

    def montar(self):
        conteudo = ttk.Frame(self.raiz, padding=12)
        conteudo.grid(row=0, column=0, sticky="nsew")
        self.raiz.columnconfigure(0, weight=1)
        self.raiz.rowconfigure(0, weight=1)

        # Formulário 
        form = ttk.LabelFrame(conteudo, text="Novo paciente", padding=10)
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        especies = list(CRIADORES.keys())
        self.var_especie = tk.StringVar(value=especies[0])
        self.var_nome = tk.StringVar()
        self.var_idade = tk.StringVar()
        self.var_peso = tk.StringVar()
        self.var_telefone = tk.StringVar()

        ttk.Label(form, text="Espécie:").grid(row=0, column=0, sticky="w", pady=3)
        cmb = ttk.Combobox(form, textvariable=self.var_especie, values=especies,
                           state="readonly", width=22)
        cmb.grid(row=0, column=1, sticky="ew", pady=3)

        # Campos de texto: (rótulo, variável, chave usada em DadoInvalidoError.campo)
        definicoes = [
            ("Nome:", self.var_nome, "nome"),
            ("Idade (anos):", self.var_idade, "idade"),
            ("Peso (kg):", self.var_peso, "peso"),
            ("Telefone do tutor:", self.var_telefone, "telefone"),
        ]
        self.campos = {"especie": cmb}
        for linha, (rotulo, var, chave) in enumerate(definicoes, start=1):
            ttk.Label(form, text=rotulo).grid(row=linha, column=0, sticky="w", pady=3)
            entrada = ttk.Entry(form, textvariable=var, width=24)
            entrada.grid(row=linha, column=1, sticky="ew", pady=3)
            self.campos[chave] = entrada
        form.columnconfigure(1, weight=1)

        botoes = ttk.Frame(form)
        botoes.grid(row=5, column=0, columnspan=2, sticky="e", pady=(10, 0))
        ttk.Button(botoes, text="Limpar", command=self.limpar).grid(row=0, column=0, padx=4)
        ttk.Button(botoes, text="Cadastrar", command=self.ao_cadastrar).grid(row=0, column=1)

        # Observadores 
        self.painel_contagem = PainelContagem(conteudo, especies)
        self.painel_contagem.grid(row=0, column=1, sticky="new")

        self.painel_pacientes = PainelPacientes(conteudo)
        self.painel_pacientes.grid(row=1, column=0, columnspan=2, sticky="nsew",
                                   pady=(10, 0))

        self.status = BarraStatus(self.raiz)
        self.status.grid(row=1, column=0, sticky="ew")

        conteudo.columnconfigure(0, weight=1)
        conteudo.rowconfigure(1, weight=1)

        for obs in (self.painel_pacientes, self.painel_contagem, self.status):
            self.clinica.adicionar_observador(obs)

        self.raiz.bind("<Return>", lambda _e: self.ao_cadastrar())
        self.campos["nome"].focus_set()

    # Ouvinte do botão 
    def ao_cadastrar(self):
        """Ouvinte: repassa o texto cru e traduz exceções em diálogos.

        Não há nenhum "if idade < 0" aqui: quem decide o que é válido é o
        domínio. A tela só sabe que DadoInvalidoError tem mensagem e campo.
        """
        try:
            criador = obter_criador(self.var_especie.get())
            criador.registrar(
                self.clinica,
                self.var_nome.get(),
                self.var_idade.get(),
                self.var_peso.get(),
                self.var_telefone.get(),
            )
        except DadoInvalidoError as erro:
            messagebox.showerror("Dado inválido", str(erro), parent=self.raiz)
            campo = self.campos.get(erro.campo)
            if campo is not None:
                campo.focus_set()
                if isinstance(campo, ttk.Entry):
                    campo.select_range(0, tk.END)
        except Exception as erro:  # rede de segurança: a janela não pode travar
            messagebox.showerror("Erro inesperado",
                                 f"Algo deu errado: {erro}", parent=self.raiz)
        else:
            self.limpar()
        # Observação: atualizar lista/contador/status NÃO é feito aqui,
        # é responsabilidade dos observadores.

    def limpar(self):
        for var in (self.var_nome, self.var_idade, self.var_peso, self.var_telefone):
            var.set("")
        self.campos["nome"].focus_set()


def iniciar(nome_clinica="Clínica PetVida"):
    raiz = tk.Tk()
    JanelaCadastro(raiz, Clinica(nome_clinica))
    raiz.mainloop()
