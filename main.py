import os
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageDraw, ImageFont, ImageTk

modelo_certificado = askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])

# Verificando se o modelo do certificado foi carregado

if not modelo_certificado:
    messagebox.showerror("Erro", "Carregue um modelo de certificado")
    exit()

modelo_certificado = Image.open(modelo_certificado)

# Dimensões da imagem original
largura_original, altura_original = modelo_certificado.size

largura_base = 500
proporcao = largura_base / modelo_certificado.width
nova_altura = int(modelo_certificado.height * proporcao)

# Redimensionando a imagem original para visualizar na interface gráfica

modelo_certificado_redimensionado = modelo_certificado.resize(
    (largura_base, nova_altura)
)

# Verificando se o arquivo como os nomes dos alunos foi carregado

alunos = askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
if not alunos:
    messagebox.showerror("Erro", "Carregue os nomes dos alunos")
    exit()


def gerar_certificados(posicao_texto):
    if not posicao_texto:
        return messagebox.showerror("Erro", "Selecione a posição do texto")

    with open(alunos, "r", encoding="utf-8") as arquivo:
        lista_alunos = arquivo.read().splitlines()

    os.makedirs("certificados", exist_ok=True)

    for aluno in lista_alunos:
        certificado = modelo_certificado.copy()
        d = ImageDraw.Draw(certificado)
        cor_texto = (18, 48, 134)

        fonte = ImageFont.truetype("arial.ttf", 75)

        d.text(posicao_texto, aluno, fill=cor_texto, font=fonte)

        arquivo_saida = "certificados/" + aluno.replace(" ", "") + ".png"

        certificado.save(arquivo_saida)

    messagebox.showinfo("Sucesso", "Certificados gerados com sucesso!")


def pegar_posicao(event):
    # Coordenadas da imagem redimensionada
    x_redimensionada, y_redimensionada = event.x, event.y

    # Converter para as coordenadas da imagem original
    x_original = int(x_redimensionada * (largura_original / largura_base))
    y_original = int(y_redimensionada * (altura_original / nova_altura))
    print(x_original, y_original)

    gerar_certificados((x_original, y_original))


root = tk.Tk()
root.title("Gerador de Certificados")
root.resizable(False, False)

# Centraliza a janela
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()

posicao_x = (largura_tela // 2) - (largura_base // 2)
posicao_y = (altura_tela // 2) - (nova_altura // 2)

root.geometry(f"{largura_base}x{nova_altura}+{posicao_x}+{posicao_y}")

tk_img = ImageTk.PhotoImage(modelo_certificado_redimensionado)

canvas_img = tk.Canvas(
    root, cursor="", bg="white", width=largura_base, height=nova_altura
)

canvas_img.create_image(0, 0, anchor="nw", image=tk_img)
canvas_img.pack(fill="both", expand=True)
canvas_img.bind("<Button-1>", pegar_posicao)

root.mainloop()
