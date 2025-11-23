import pyautogui
import keyboard
import time
import pyperclip

# FUNÇÃO
def tarefa():
    print('PARA INICIAR APERTE CTRL + V')
    time.sleep(1)
    # ABRIR NAVEGADOR
    pyautogui.press('win')
    time.sleep(1)
    pyautogui.write('chrome')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.click(x=256, y=63)

    # ENTRAR NO GMAIL
    time.sleep(1)
    pyautogui.write('https://gmail.com/')
    pyautogui.press('enter')

    # ABRIR UM NOVO E-MAIL
    time.sleep(3)
    pyautogui.click(x=22, y=217)

    # DESTINATÁRIO
    time.sleep(2)
    pyautogui.write('E-MAIL')
    time.sleep(2)
    pyautogui.press('enter')
    pyautogui.press('tab')

    # ASSUNTO E-MAIL 
    time.sleep(1)
    pyperclip.copy('TESTE AUTOMAÇÃO')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)
    pyautogui.press('tab')

    # MENSAGEM E-MAIL
    pyperclip.copy('TEXTO')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('tab')
    pyautogui.press('enter')
# HOTKEY'S
keyboard.add_hotkey("ctrl+alt+a", tarefa)
keyboard.wait("esc")



