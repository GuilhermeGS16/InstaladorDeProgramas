import os
path = r'C:\Users\guilherme.salome\OneDrive - PATRIMAR ENGENHARIA S A\Área de Trabalho\ScriptProgramas-main\Icons'

lista_imagens = ""

for image in os.listdir(path):
    image = os.path.join(path, image)
    if os.path.isfile(image):
        with open(image, 'rb') as _file:
            nome_file = os.path.basename(image).split('.')[0]
            lista_imagens += f"{nome_file} = {_file.read()}\n"


with open("icones.py", 'w') as _file:
    _file.write(lista_imagens)
