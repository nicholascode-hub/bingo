import random
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *


class JogoBingo:
    # Layouts por número de jogadores: (colunas, linhas_grade)
    GRADE_LAYOUT = {1: (1, 1), 2: (2, 1), 3: (2, 2), 4: (2, 2)}
    # Tamanho da janela por número de jogadores
    JANELA_SIZE = {1: "900x750", 2: "1400x750", 3: "1400x1050", 4: "1400x1050"}
    # Fonte das células por número de jogadores (header_bingo, celula, padding)
    FONTE_CARTELA = {1: (20, 16, 12), 2: (16, 13, 8), 3: (14, 11, 6), 4: (14, 11, 6)}

    def __init__(self, master):
        self.master = master
        self.master.title("Bingo")
        self.master.geometry("900x750")
        self.master.minsize(700, 500)

        # Estado do jogo
        self.num_jogadores = 1
        self.nomes_jogadores = []
        self.cartelas = []
        self.widgets_cartelas = []
        self.numeros_sorteados = set()
        self.numeros_disponiveis = list(range(1, 76))
        self.jogo_ativo = False

        self.tela_inicial()

    # ──────────────────────────────────────────────
    #  UTILITÁRIOS
    # ──────────────────────────────────────────────

    def limpar_janela(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def gerar_cartela(self):
        """Gera uma matriz 5×5 padrão de Bingo com espaço LIVRE no centro."""
        b = random.sample(range(1, 16), 5)
        i = random.sample(range(16, 31), 5)
        n = random.sample(range(31, 46), 4)
        n.insert(2, "LIVRE")
        g = random.sample(range(46, 61), 5)
        o = random.sample(range(61, 76), 5)

        return [[b[l], i[l], n[l], g[l], o[l]] for l in range(5)]

    # ──────────────────────────────────────────────
    #  TELA 1 — MENU INICIAL
    # ──────────────────────────────────────────────

    def tela_inicial(self):
        self.limpar_janela()
        self.jogo_ativo = False
        self.master.geometry("900x750")

        frame = tb.Frame(self.master, padding=30)
        frame.pack(expand=True)

        tb.Label(
            frame,
            text="🎱 BEM-VINDO AO BINGO",
            font=("Helvetica", 28, "bold"),
            bootstyle=PRIMARY,
        ).pack(pady=20)

        tb.Label(
            frame,
            text="Número de Jogadores:",
            font=("Helvetica", 12),
        ).pack(pady=5)

        self.spin_jogadores = tb.Spinbox(
            frame, from_=1, to=4, font=("Helvetica", 14), width=5, bootstyle=INFO
        )
        self.spin_jogadores.set(1)
        self.spin_jogadores.pack(pady=10)

        tb.Button(
            frame,
            text="Próximo →",
            bootstyle=(SUCCESS, OUTLINE),
            width=20,
            command=self.tela_nomes,
        ).pack(pady=30)

    # ──────────────────────────────────────────────
    #  TELA 2 — CADASTRO DE NOMES
    # ──────────────────────────────────────────────

    def tela_nomes(self):
        """Tela onde cada jogador digita o próprio nome antes de começar."""
        try:
            self.num_jogadores = int(self.spin_jogadores.get())
            if not (1 <= self.num_jogadores <= 4):
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Insira um número válido de jogadores (1 a 4).")
            return

        self.limpar_janela()

        frame = tb.Frame(self.master, padding=30)
        frame.pack(expand=True)

        tb.Label(
            frame,
            text="Como cada jogador quer ser chamado?",
            font=("Helvetica", 16, "bold"),
            bootstyle=INFO,
        ).pack(pady=(0, 20))

        self.entries_nomes = []

        for idx in range(self.num_jogadores):
            sub = tb.Frame(frame)
            sub.pack(fill=X, pady=6)

            tb.Label(
                sub,
                text=f"Jogador {idx + 1}:",
                font=("Helvetica", 12),
                width=12,
                anchor=W,
            ).pack(side=LEFT)

            entry = tb.Entry(sub, font=("Helvetica", 13), bootstyle=PRIMARY, width=22)
            entry.insert(0, f"Jogador {idx + 1}")   # valor padrão editável
            entry.pack(side=LEFT, padx=8)
            # Seleciona o texto padrão para facilitar substituição
            entry.bind("<FocusIn>", lambda e, en=entry: en.select_range(0, END))
            self.entries_nomes.append(entry)

        btn_frame = tb.Frame(frame)
        btn_frame.pack(pady=30)

        tb.Button(
            btn_frame,
            text="← Voltar",
            bootstyle=(SECONDARY, OUTLINE),
            width=12,
            command=self.tela_inicial,
        ).pack(side=LEFT, padx=10)

        tb.Button(
            btn_frame,
            text="Iniciar Jogo 🎉",
            bootstyle=(SUCCESS, OUTLINE),
            width=16,
            command=self.iniciar_jogo,
        ).pack(side=LEFT, padx=10)

    # ──────────────────────────────────────────────
    #  INICIAR JOGO
    # ──────────────────────────────────────────────

    def iniciar_jogo(self):
        # Lê e valida os nomes
        nomes = []
        for idx, entry in enumerate(self.entries_nomes):
            nome = entry.get().strip()
            if not nome:
                nome = f"Jogador {idx + 1}"
            nomes.append(nome)

        self.nomes_jogadores = nomes

        # Mensagem de boas-vindas personalizada
        if len(nomes) == 1:
            saudacao = f"Bem-vindo, {nomes[0]}! 🎱 Boa sorte!"
        else:
            lista = ", ".join(nomes[:-1]) + f" e {nomes[-1]}"
            saudacao = f"Bem-vindos, {lista}! 🎱 Que ganhe o melhor!"

        messagebox.showinfo("Bingo!", saudacao)

        # Prepara o estado do jogo
        self.cartelas = [self.gerar_cartela() for _ in range(self.num_jogadores)]
        self.numeros_sorteados = set()
        self.numeros_disponiveis = list(range(1, 76))
        random.shuffle(self.numeros_disponiveis)
        self.jogo_ativo = True

        self.tela_jogo()

    # ──────────────────────────────────────────────
    #  TELA 3 — JOGO
    # ──────────────────────────────────────────────

    def tela_jogo(self):
        self.limpar_janela()
        self.widgets_cartelas = []

        # Ajusta tamanho da janela conforme número de jogadores
        self.master.geometry(self.JANELA_SIZE[self.num_jogadores])

        # ── Painel superior ──
        painel_topo = tb.Frame(self.master, padding=(10, 8))
        painel_topo.pack(fill=X)

        self.lbl_ultimo_numero = tb.Label(
            painel_topo, text="--", font=("Helvetica", 42, "bold"), bootstyle=DANGER
        )
        self.lbl_ultimo_numero.pack(side=LEFT, padx=16)

        painel_botoes = tb.Frame(painel_topo)
        painel_botoes.pack(side=LEFT, padx=16)

        self.btn_sortear = tb.Button(
            painel_botoes,
            text="🎲 Sortear Número",
            bootstyle=PRIMARY,
            command=self.sortear_numero,
        )
        self.btn_sortear.pack(fill=X, pady=4)

        tb.Button(
            painel_botoes,
            text="↩ Voltar ao Menu",
            bootstyle=SECONDARY,
            command=self.tela_inicial,
        ).pack(fill=X, pady=4)

        self.lbl_historico = tb.Label(
            painel_topo,
            text="Sorteados: Nenhum",
            font=("Helvetica", 10),
            wraplength=500,
            justify=LEFT,
        )
        self.lbl_historico.pack(side=LEFT, padx=16, fill=X, expand=True)

        tb.Separator(self.master, orient=HORIZONTAL).pack(fill=X, padx=10)

        # ── Grade de cartelas ──
        cols_grade, _ = self.GRADE_LAYOUT[self.num_jogadores]
        fnt_header, fnt_celula, pad_celula = self.FONTE_CARTELA[self.num_jogadores]
        letras_bingo = ["B", "I", "N", "G", "O"]

        frame_grade = tb.Frame(self.master, padding=10)
        frame_grade.pack(fill=BOTH, expand=True)

        # Configurar pesos para células expandirem igualmente
        for c in range(cols_grade):
            frame_grade.columnconfigure(c, weight=1, uniform="col")
        for r in range((self.num_jogadores + cols_grade - 1) // cols_grade):
            frame_grade.rowconfigure(r, weight=1, uniform="row")

        for p_idx in range(self.num_jogadores):
            grade_row = p_idx // cols_grade
            grade_col = p_idx % cols_grade
            nome = self.nomes_jogadores[p_idx]

            # Container de cada jogador com borda e título
            frame_jogador = tb.LabelFrame(
                frame_grade,
                text=f"  🎴 {nome}  ",
                padding=10,
                bootstyle=INFO,
            )
            frame_jogador.grid(
                row=grade_row, column=grade_col,
                sticky="nsew", padx=8, pady=8,
            )
            frame_jogador.rowconfigure(0, weight=1)
            frame_jogador.columnconfigure(0, weight=1)

            frame_grid = tb.Frame(frame_jogador)
            frame_grid.grid(sticky="nsew")
            # Centralizar o grid dentro do LabelFrame
            frame_jogador.rowconfigure(0, weight=1)
            frame_jogador.columnconfigure(0, weight=1)

            matriz_widgets = []

            # Cabeçalho B-I-N-G-O
            for col, letra in enumerate(letras_bingo):
                tb.Label(
                    frame_grid,
                    text=letra,
                    font=("Helvetica", fnt_header, "bold"),
                    bootstyle=PRIMARY,
                    width=4,
                    anchor=CENTER,
                ).grid(row=0, column=col, pady=(2, 4), padx=3)

            # Células da cartela
            for linha in range(5):
                linha_widgets = []
                for col in range(5):
                    valor = self.cartelas[p_idx][linha][col]
                    estilo = SUCCESS if valor == "LIVRE" else SECONDARY

                    lbl = tb.Label(
                        frame_grid,
                        text=str(valor),
                        font=("Helvetica", fnt_celula),
                        bootstyle=(estilo, INVERSE),
                        width=4,
                        anchor=CENTER,
                        padding=pad_celula,
                    )
                    lbl.grid(row=linha + 1, column=col, padx=3, pady=3)
                    linha_widgets.append(lbl)
                matriz_widgets.append(linha_widgets)

            self.widgets_cartelas.append(matriz_widgets)

        # Se 3 jogadores, preenche célula vazia da grade com frame vazio
        if self.num_jogadores == 3:
            tb.Frame(frame_grade).grid(row=1, column=1, sticky="nsew", padx=8, pady=8)

    # ──────────────────────────────────────────────
    #  LÓGICA DO JOGO
    # ──────────────────────────────────────────────

    def sortear_numero(self):
        if not self.jogo_ativo or not self.numeros_disponiveis:
            messagebox.showinfo("Bingo", "Todos os números já foram sorteados!")
            return

        numero = self.numeros_disponiveis.pop()
        self.numeros_sorteados.add(numero)

        letra = (
            "B" if numero <= 15
            else "I" if numero <= 30
            else "N" if numero <= 45
            else "G" if numero <= 60
            else "O"
        )

        self.lbl_ultimo_numero.config(text=f"{letra}-{numero}")

        historico = ", ".join(str(n) for n in list(self.numeros_sorteados)[-15:])
        self.lbl_historico.config(text=f"Últimos Sorteados:\n{historico}")

        self.atualizar_cartelas(numero)
        self.verificar_vencedores()

    def atualizar_cartelas(self, numero_sorteado):
        for p_idx in range(self.num_jogadores):
            for linha in range(5):
                for col in range(5):
                    if self.cartelas[p_idx][linha][col] == numero_sorteado:
                        self.widgets_cartelas[p_idx][linha][col].configure(
                            bootstyle=(SUCCESS, INVERSE)
                        )

    def verificar_vencedores(self):
        def marcada(p, l, c):
            val = self.cartelas[p][l][c]
            return val == "LIVRE" or val in self.numeros_sorteados

        vencedores = []
        for p_idx in range(self.num_jogadores):
            ganhou = False

            # Linhas e colunas
            for i in range(5):
                if all(marcada(p_idx, i, j) for j in range(5)):
                    ganhou = True
                if all(marcada(p_idx, j, i) for j in range(5)):
                    ganhou = True

            # Diagonais
            if all(marcada(p_idx, i, i) for i in range(5)):
                ganhou = True
            if all(marcada(p_idx, i, 4 - i) for i in range(5)):
                ganhou = True

            if ganhou:
                vencedores.append(self.nomes_jogadores[p_idx])

        if vencedores:
            self.jogo_ativo = False
            self.btn_sortear.configure(state=DISABLED)

            if len(vencedores) == 1:
                msg = f"🎉 BINGO!!!\n\n{vencedores[0]} venceu! Parabéns!"
            else:
                lista = ", ".join(vencedores)
                msg = f"🎉 BINGO!!!\n\nEmpate entre: {lista}! Parabéns a todos!"

            messagebox.showinfo("Temos um Vencedor!", msg)


# ──────────────────────────────────────────────
#  ENTRADA
# ──────────────────────────────────────────────

if __name__ == "__main__":
    app = tb.Window(themename="litera")
    jogo = JogoBingo(app)
    app.mainloop()