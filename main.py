"""
Aplicativo Open Source (Free) gerador de comprovação de radiação do Salamandra Rádio.
Desenvolvido por Daniel Soares Lima.
Versão 0.1 - Pt_Br.

Requisitos:
pip install reportlab
"""

import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import pagesizes
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image, ImageTk
import sys

# ==============================
# CONFIGURAÇÕES VISUAIS
# ==============================

COR_AZUL = "#0B3C5D"
COR_BRANCO = "#FFFFFF"
COR_CINZA = "#E5E5E5"
COR_PRETO = "#000000"

# ==============================
# FUNÇÕES UTILITÁRIAS
# ==============================

def resource_path(relative_path):
    """
    Isso evita erro após imagem ou icone virar .exe
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

caminho_imagem = resource_path("assets/imagem.png")

def caminho_recurso(caminho_relativo):
    """
    Retorna o caminho absoluto para um recurso.
    """
    return os.path.join(os.path.dirname(__file__), caminho_relativo)

def carregar_imagem_redimensionada(caminho, largura=200, altura=200):
    """
    Carrega uma imagem e força redimensionamento fixo em 200x200.
    Retorna objeto compatível com Tkinter.
    """

    imagem = Image.open(caminho)
    imagem = imagem.resize((largura, altura), Image.LANCZOS)
    return ImageTk.PhotoImage(imagem)

# ==============================
# FUNÇÃO SPLASH SCREEN
# ==============================

def mostrar_splash(root):
    """
    Exibe a tela inicial (SplashScreen) centralizada com:
    - Logo
    - Título em negrito
    - Descrição do aplicativo
    """

    splash = tk.Toplevel(root)
    splash.overrideredirect(True)

    largura = 500
    altura = 300
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)

    splash.geometry(f"{largura}x{altura}+{x}+{y}")
    splash.configure(bg=COR_BRANCO)

    # Logo    
    logo = tk.PhotoImage(file=caminho_recurso("assets/logo.png"))
    label_logo = tk.Label(splash, image=logo, bg=COR_BRANCO)
    label_logo.image = logo
    label_logo.pack(pady=10)
    
    # Título
    titulo = tk.Label(
        splash,
        text="Comprovação de Radiação - Salamandra Rádio",
        font=("Arial", 14, "bold"),
        bg=COR_BRANCO,
        fg=COR_AZUL,
    )
    titulo.pack()

    # Descrição
    descricao = tk.Label(
        splash,
        text=" Aplicativo Open Source (Free) gerador de comprovação de radiação do Salamandra Rádio.\n"
             "Desenvolvido por Daniel Soares Lima.\nVersão 0.1 - Pt_Br.\n Todos direitos reservados ®.",
        font=("Arial", 9),
        bg=COR_BRANCO,
        fg=COR_PRETO,
        justify="center",
    )
    descricao.pack(pady=10)

    splash.after(3000, splash.destroy)

# ==============================
# CLASSE PRINCIPAL
# ==============================

class Aplicativo:

    def __init__(self, root):
        """
        Inicializa a janela principal:
        - 800x600
        - Centralizada
        - Não maximizada
        - Bloqueio de redimensionamento
        """
        self.root = root
        self.root.title("Comprovação de Radiação - Salamandra Rádio")
        
        # Define ícone da aplicação
        self.root.iconphoto(True, tk.PhotoImage (file = caminho_recurso("assets/logo.png")))
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        
        # Centralizar
        largura = 800
        altura = 600
        x = (root.winfo_screenwidth() // 2) - (largura // 2)
        y = (root.winfo_screenheight() // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

        self.pasta_logs = ""
        self.resultados = []

        self.criar_layout()

    # ==============================
    # CRIAÇÃO DO LAYOUT
    # ==============================

    def criar_layout(self):
        """
        Cria o layout principal da aplicação.
        """
        # ==============================
        # TOPO PADRÃO CORPORATIVO
        # ==============================

        frame_topo = tk.Frame(self.root, bg=COR_AZUL, height=50)
        frame_topo.pack(fill="x")

        titulo = tk.Label(
            frame_topo,
            text="Gerador de Comprovação de Radiação",
            font=("Arial", 14, "bold"),
            bg=COR_AZUL,
            fg=COR_BRANCO,
        )
        titulo.pack(pady=10)

        # ==============================
        # NOTEBOOK (ABAS)
        # ==============================

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # ==============================
        # ABA 1 - CLIENTE
        # ==============================

        aba_cliente = tk.Frame(notebook)
        notebook.add(aba_cliente, text="Cliente / Contratante")

        frame_cliente = ttk.LabelFrame(aba_cliente, text="Dados do Cliente / Contratante")
        frame_cliente.pack(fill="both", expand=True, padx=20, pady=20)

        self.campos_cliente = self.criar_campos(frame_cliente)

        # Imagem Cliente
        img_cliente = carregar_imagem_redimensionada(
        caminho_recurso("assets/aba_cliente.png"),
        200,
        200
        )

        label_img_cliente = tk.Label(aba_cliente, image=img_cliente, bg="white")
        label_img_cliente.image = img_cliente
        label_img_cliente.place(relx=0.97, rely=0.95, anchor="se")

        # ==============================
        # ABA 2 - EMISSORA
        # ==============================

        aba_emissora = tk.Frame(notebook)
        notebook.add(aba_emissora, text="Emissora")

        frame_emissora = ttk.LabelFrame(aba_emissora, text="Dados da Emissora")
        frame_emissora.pack(fill="both", expand=True, padx=20, pady=20)

        self.campos_emissora = self.criar_campos(frame_emissora)

        # Imagem Emissora
        img_emissora = carregar_imagem_redimensionada(
        caminho_recurso("assets/aba_emissora.png"),
        150,
        200
        )

        label_img_emissora = tk.Label(aba_emissora, image=img_emissora, bg="white")
        label_img_emissora.image = img_emissora
        label_img_emissora.place(relx=0.97, rely=0.95, anchor="se")

        # ==============================
        # ABA 3 - RESULTADO DA PESQUISA
        # ==============================

        aba_resultado = tk.Frame(notebook)
        notebook.add(aba_resultado, text="Resultado da Pesquisa")

        # --- Filtros ---
        frame_filtros = ttk.LabelFrame(aba_resultado, text="Filtros de Pesquisa")
        frame_filtros.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_filtros, text="Palavra-chave / Mídia:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_palavra = tk.Entry(frame_filtros, width=30)
        self.entry_palavra.grid(row=0, column=1, padx=5)

        tk.Button(
            frame_filtros,
            text="Selecionar Pasta Logs",
            command=self.selecionar_pasta
        ).grid(row=0, column=2, padx=5)

        tk.Label(frame_filtros, text="Data Inicial (AAAAMMDD):").grid(row=1, column=0, padx=5)
        self.entry_data_ini = tk.Entry(frame_filtros, width=15)
        self.entry_data_ini.grid(row=1, column=1, sticky="w")

        tk.Label(frame_filtros, text="Data Final (AAAAMMDD):").grid(row=1, column=2, padx=5)
        self.entry_data_fim = tk.Entry(frame_filtros, width=15)
        self.entry_data_fim.grid(row=1, column=3, sticky="w")

        # --- Botões ---
        frame_botoes = tk.Frame(aba_resultado)
        frame_botoes.pack(fill="x", padx=10, pady=5)

        tk.Button(
            frame_botoes,
            text="Pesquisar",
            bg=COR_AZUL,
            fg=COR_BRANCO,
            width=15,
            command=self.pesquisar_logs
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botoes,
            text="Gerar PDF",
            bg=COR_PRETO,
            fg=COR_BRANCO,
            width=15,
            command=self.gerar_pdf
        ).pack(side="left", padx=5)

        # --- Barra de Progresso ---
        self.progresso = ttk.Progressbar(
            aba_resultado,
            orient="horizontal",
            length=750,
            mode="determinate"
        )
        self.progresso.pack(pady=5)

        # --- Tabela de Resultados ---
        frame_tabela = ttk.LabelFrame(aba_resultado, text="Resultados Encontrados")
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=5)

        colunas = ("Data de Execução", "Hora de Execução", "Título da Mídia")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True)
        
        # Imagem Resultado
        img_resultado = carregar_imagem_redimensionada(
        caminho_recurso("assets/aba_resultado.png"),
        48,
        48
        )

        label_img_resultado = tk.Label(aba_resultado, image=img_resultado, bg="white")
        label_img_resultado.image = img_resultado
        label_img_resultado.place(relx=0.98, rely=0.15, anchor="se")

    # ==============================
    # BOTÃO FECHAR FIXO (fora das abas)
    # ==============================

        frame_rodape = tk.Frame(self.root, bg=COR_CINZA, height=40)
        frame_rodape.pack(fill="x")

        botao_fechar = tk.Button(
            frame_rodape,
            text="Fechar",
            bg="#8B0000",
            fg="white",
            width=12,
            command=self.root.destroy
        )
        botao_fechar.pack(side="right", padx=15, pady=5)

    # ==============================
    # FUNÇÕES AUXILIARES
    # ==============================

    def criar_campos(self, frame):
        """
        Cria campos padrão para Cliente e Emissora.
        """
        labels = ["Nome Completo", "Endereço Completo", "CPF/CNPJ", "Cidade", "Estado", "Fone (DDD)", "Email"]
        entradas = {}

        for i, label in enumerate(labels):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky="w")
            entry = tk.Entry(frame, width=40)
            entry.grid(row=i, column=1)
            entradas[label] = entry

        return entradas

    def selecionar_pasta(self):
        """
        Permite ao usuário selecionar a pasta onde estão os logs.
        """
        self.pasta_logs = filedialog.askdirectory()

    def pesquisar_logs(self):
        """
        Pesquisa arquivos .log ou .txt
        - Insensível a maiúscula/minúscula
        - Filtra intervalo de datas
        - Apenas 1 resultado por hora por dia
        """
        if not self.pasta_logs:
            messagebox.showwarning("Aviso", "Selecione a pasta de logs.")
            return

        palavra = self.entry_palavra.get().lower()
        data_ini = self.entry_data_ini.get()
        data_fim = self.entry_data_fim.get()

        self.tree.delete(*self.tree.get_children())
        self.resultados.clear()

        arquivos = [f for f in os.listdir(self.pasta_logs) if f.endswith((".log", ".txt"))]
        total = len(arquivos)
        self.progresso["maximum"] = total

        registros_unicos = set()

        for i, arquivo in enumerate(arquivos):
            self.progresso["value"] = i + 1
            self.root.update_idletasks()

            match_data = re.search(r"(\d{8})", arquivo)
            if not match_data:
                continue

            data_arquivo = match_data.group(1)

            if not (data_ini <= data_arquivo <= data_fim):
                continue

            caminho = os.path.join(self.pasta_logs, arquivo)

            with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                for linha in f:
                    if palavra in linha.lower():
                        hora_match = re.match(r"(\d{2}:\d{2}:\d{2})", linha)
                        if hora_match:
                            hora = hora_match.group(1)
                            chave = (data_arquivo, hora[:2])
                            if chave not in registros_unicos:
                                registros_unicos.add(chave)
                                self.resultados.append((data_arquivo, hora, palavra))

        self.resultados.sort()

        for r in self.resultados:
            self.tree.insert("", "end", values=r)

    # ==============================
    # GERAR PDF
    # ==============================

    def gerar_pdf(self):
        """
        Gera PDF profissional contendo:

        - Cabeçalho completo com dados do Cliente / Contratante
        - Cabeçalho completo com dados da Emissora
        - Tabela numerada e ordenada
        - Cores corporativas
        - Rodapé com numeração automática
        - Dimensionamento correto para A4
        """

        if not self.resultados:
            messagebox.showwarning("Aviso", "Nenhum resultado para gerar PDF.")
            return

        arquivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivo PDF", "*.pdf")]
        )

        if not arquivo:
            return

        # Documento A4 com margens adequadas
        doc = SimpleDocTemplate(
            arquivo,
            pagesize=pagesizes.A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm
        )

        elementos = []

        # ==============================
        # ESTILOS
        # ==============================

        estilo_titulo = ParagraphStyle(
            name="Titulo",
            fontSize=14,
            spaceAfter=10
        )

        estilo_normal = ParagraphStyle(
            name="Normal",
            fontSize=9,
            spaceAfter=3
        )

        # ==============================
        # CABEÇALHO PRINCIPAL
        # ==============================

        elementos.append(Paragraph("<b>COMPROVAÇÃO DE RADIAÇÃO</b>", estilo_titulo))
        elementos.append(Spacer(1, 0.5 * cm))

        # ==============================
        # DADOS CLIENTE
        # ==============================

        elementos.append(Paragraph("<b>CLIENTE / CONTRATANTE</b>", estilo_normal))

        for campo, entry in self.campos_cliente.items():
            valor = entry.get()
            elementos.append(Paragraph(f"<b>{campo}:</b> {valor}", estilo_normal))

        elementos.append(Spacer(1, 0.4 * cm))

        # ==============================
        # DADOS EMISSORA
        # ==============================

        elementos.append(Paragraph("<b>EMISSORA</b>", estilo_normal))

        for campo, entry in self.campos_emissora.items():
            valor = entry.get()
            elementos.append(Paragraph(f"<b>{campo}:</b> {valor}", estilo_normal))

        elementos.append(Spacer(1, 0.7 * cm))

        # ==============================
        # TABELA DE RESULTADOS
        # ==============================

        # Ordenação crescente
        self.resultados.sort()

        dados = [["Nº", "Data de Execução\n (Ano,Mês e Dia) ", "Hora de Execução\n (Hora, Minuto e Segundos) ", "Título da Mídia"]]

        for i, linha in enumerate(self.resultados, start=1):
            dados.append([i, linha[0], linha[1], linha[2]])

        # Larguras ajustadas para A4
        largura_total = pagesizes.A4[0] - 4 * cm
        col_widths = [
            largura_total * 0.07,
            largura_total * 0.20,
            largura_total * 0.20,
            largura_total * 0.53,
        ]

        tabela = Table(dados, colWidths=col_widths, repeatRows=1)

        tabela.setStyle(TableStyle([

            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0B3C5D")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),

            # Corpo
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),
            ('ALIGN', (3, 0), (3, -1), 'LEFT'),

        ]))

        elementos.append(tabela)

        # ==============================
        # RODAPÉ COM NUMERAÇÃO
        # ==============================

        def adicionar_rodape(canvas, doc):
            canvas.saveState()
            canvas.setFont("Helvetica", 8)
            texto = f"Página {doc.page}"
            canvas.drawRightString(
                pagesizes.A4[0] - 2 * cm,
                1.5 * cm,
                texto
            )
            canvas.restoreState()

        doc.build(elementos, onFirstPage=adicionar_rodape, onLaterPages=adicionar_rodape)

        messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")

# ==============================
# EXECUÇÃO
# ==============================

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    mostrar_splash(root)
    root.after(3000, lambda: root.deiconify())
    app = Aplicativo(root)
    root.mainloop()
