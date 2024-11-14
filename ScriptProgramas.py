import sys
import os
import shutil
import subprocess
import threading
import multiprocessing
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import icones



def executar_programas(programas_selecionados):
    for programa in programas_selecionados:
        try:
            subprocess.run([programa], check=True)
            print(f"{os.path.basename(programa)} executado com sucesso!")
        except subprocess.CalledProcessError:
            print(f"Erro ao executar o arquivo: {os.path.basename(programa)}")
        except FileNotFoundError:
            print(f"Arquivo {os.path.basename(programa)} não encontrado.")
    messagebox.showinfo("Conclusão", "Execução concluída.")

def copiar_pasta(caminho_origem, caminho_destino):
    """Copia uma pasta inteira em uma thread separada."""
    try:
        shutil.copytree(caminho_origem, caminho_destino)
        print(f"Pasta {os.path.basename(caminho_origem)} copiada com sucesso!")
    except FileExistsError:
        print(f"Pasta {os.path.basename(caminho_destino)} já existe. Ignorando cópia.")
    except Exception as e:
        print(f"Erro ao copiar a pasta {os.path.basename(caminho_origem)}: {e}")

def main():
    ProgramasPcGui = r'\\169.254.81.140\C$\Users\guilherme.salome\OneDrive - PATRIMAR ENGENHARIA S A\Área de Trabalho\ScriptProgramas-main\Programas'
    CaminhoAreaDeTrabalho = os.path.join(os.path.expanduser("~"), "Desktop")
    CaminhoPastaCopiada = os.path.join(CaminhoAreaDeTrabalho, "ProgramasSelecionados")

    os.makedirs(CaminhoPastaCopiada, exist_ok=True)

    programas = {
        "Adobe Reader": (os.path.join(ProgramasPcGui,"AdobeReader.exe"), icones.adobe),
        "AnyDesk": (os.path.join(ProgramasPcGui,"AnyDesk.exe"), icones.anydesk),
        "OpenVPN": (os.path.join(ProgramasPcGui,"OpenVPN.exe"), icones.openvpn),
        "LightShot": (os.path.join(ProgramasPcGui,"LightShot.exe"), icones.lightshot),
        "Google Chrome": (os.path.join(ProgramasPcGui,"GoogleChrome.exe"), icones.Chrome),
        "WinRar": (os.path.join(ProgramasPcGui,"WinRar.exe"), icones.winrar),
        "Bizagi": (os.path.join(ProgramasPcGui,"Bizagi.exe"), icones.bizagi),
        "DWG Visualizador": (os.path.join(ProgramasPcGui,"DWGVisualizador.exe"), icones.dwg),
        "AutoCAD LT": (os.path.join(ProgramasPcGui,"AutoCADLT.exe"), icones.autocadlt),
        "AutoCAD PRO": (os.path.join(ProgramasPcGui,"AutoCADPRO.exe"), icones.autocadpro),
        "Navisworks": (os.path.join(ProgramasPcGui,"Navisworks.exe"), icones.navisworks),
        "Revit": (os.path.join(ProgramasPcGui,"Revit.exe"), icones.revit),
        "SketchUp": (os.path.join(ProgramasPcGui,"SketchUp.exe"), icones.sketchup),
        "SketchUp Visualizador": (os.path.join(ProgramasPcGui,"SketchUpVisualizador.exe"), icones.sketchup),
        "Power BI": (os.path.join(ProgramasPcGui,"PowerBI.exe"), icones.powerbi),
        "SAP GUI": (os.path.join(ProgramasPcGui, "SAP", "PRES1", "GUI", "Windows", "Win64"), icones.sap),
    }


    root = tk.Tk()
    root.title("Instalador Megablaster do Gui V1")
    root.geometry("400x650")
    root.resizable(False, False)

    titulo = tk.Label(root, text="Selecione os programas", font=("TkHeadingFont", 14, "bold"))
    titulo.pack(pady=10)

    check_vars = {}
    icons = {}  # Armazena as referências das imagens para evitar descarte

    # Carrega ícones e cria checkboxes com ícones
    for nome, (caminho, icon_path) in programas.items():
        
        var = tk.BooleanVar()
        if (os.path.exists(icon_path)) or (isinstance(icon_path, bytes)):
            # Carrega e redimensiona o ícone
            if isinstance(icon_path, bytes):
                icon = Image.open(BytesIO(icon_path)).resize((20, 20))
            else:
                icon = Image.open(icon_path).resize((20, 20))
            
            icon_tk = ImageTk.PhotoImage(icon)


            icons[nome] = icon_tk  # Salva a referência do ícone redimensionado
            check = tk.Checkbutton(root, text=nome, variable=var, image=icon_tk, compound="left",
                                   borderwidth=0, highlightthickness=0, relief="flat", bd=0, font=("TkDefaultFont ", 13),
                                   fg="#333", bg="#f0f0f0", selectcolor="#ffffff", pady=3, padx=7)
        else:
            check = tk.Checkbutton(root, text=nome, variable=var, borderwidth=0, highlightthickness=0, relief="flat", bd=0,
                                    font=("TkDefaultFont ", 13), fg="#333", bg="#f0f0f0", selectcolor="#ffffff")
        check.pack(padx=10, pady=2, anchor="w")
        check_vars[caminho] = var

    # Função de callback para o botão de instalação
    def instalar_selecionados():
        selecionados = [caminho for caminho, var in check_vars.items() if var.get()]
        executaveis = []  # Lista para armazenar os caminhos dos executáveis copiados
        threads = []  # Lista para armazenar threads de cópia

        if selecionados:
            for caminho in selecionados:
                try:
                    if os.path.isdir(caminho):
                        destino_pasta = os.path.join(CaminhoPastaCopiada, os.path.basename(caminho))
                        if not os.path.exists(destino_pasta):
                            # Inicia uma thread para a cópia da pasta
                            thread = multiprocessing.Process(target=copiar_pasta, args=(caminho, destino_pasta))
                            thread.start()
                            threads.append((thread, os.path.join(destino_pasta, "SetupAll.exe")))
                    else:
                        shutil.copy2(caminho, CaminhoPastaCopiada)
                        programa_executavel = os.path.join(CaminhoPastaCopiada, os.path.basename(caminho))
                        executaveis.append(programa_executavel)
                        print(f"{os.path.basename(caminho)} copiado com sucesso!")
                    
                except FileNotFoundError:
                    print(f"Arquivo ou pasta {os.path.basename(caminho)} não encontrado.")
            
            # Espera todas as threads de cópia terminarem
            for thread, exec_path in threads:
                thread.join()
                executaveis.append(exec_path)

            # Executa os programas copiados
            executar_programas(executaveis)
        else:
            messagebox.showwarning("Aviso", "Nenhum programa selecionado.")

    # Botão para iniciar a instalação dos programas selecionados
    btn_instalar = tk.Button(root, text="Instalar", command=instalar_selecionados, 
                             font=("TkDefaultFont", 12,"bold"), bg="#e73c35", fg="white", relief="flat", highlightthickness=0, bd=0, height=2, width=14)
    btn_instalar.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
