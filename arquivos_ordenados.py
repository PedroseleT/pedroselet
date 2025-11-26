import os
from tkinter.filedialog import askdirectory

caminho = askdirectory(title='Selecione uma pasta: ') # ABRE O POP-UP

lista_arquivos = os.listdir(caminho) # LISTA TOTAL DE ARQUIVOS DESORGANIZADOS

# PREPARO DA ORDENAÇÃO
locais = {
    'imagens': ['.png', '.jpeg', '.jpg', '.jfif', '.gif', '.svg', '.webp', '.eps'],
    'audio': ['.mp3', '.wav'],
    'video': ['.mp4', '.wmv'],
    'documentos': ['.txt', '.pdf', '.docx', '.xls', '.html', '.xml', '.json'],
    'compactados': ['.zip', '.rar', '.7z'],
    'executaveis': ['.exe', '.msi', '.jar', '.apk', '.py'],
    'sistema': ['.ini', '.lnk'],
    'torrent': ['.torrent'],
    'temas': ['.rmskin']
}

# ATUANDO NA ORDENAÇÃO
for arquivo in lista_arquivos:
    nome, ext = os.path.splitext(f'{caminho}/{arquivo}')
    for pasta in locais:
        if ext in locais[pasta]:
            if not os.path.exists(f'{caminho}/{pasta}'):
                os.mkdir(f'{caminho}/{pasta}')
            os.rename(f'{caminho}/{arquivo}', f'{caminho}/{pasta}/{arquivo}')

print('\033[32mOrganização realizada com sucesso.\033[m')