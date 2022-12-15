from tkinter import filedialog as fd, Tk, Button, Label, Text, DISABLED, NORMAL, END
import threading
import cli

root = Tk ()
root.title (u'\U0001f4f0  Exporting Datasheet Healthcheck Info  	\U0001fa7a')
root.resizable (False, False)

screen_width = root.winfo_screenwidth () # + 3500
screen_height = root.winfo_screenheight ()
root_width = 500
root_height = 600
root.geometry (f'{root_width}x{root_height}+{int ((screen_width / 2) - (root_width / 2))}+{int ((screen_height / 2) - (root_height / 2))}')


def main_btn_event_handler ():
  file_name = fd.askopenfilename (defaultextension = '.xlsx')

  if not file_name:
    feedback_label.config (text = 'Erro desconhecido')
    return
  else:
    feedback_label.config (text = 'Iniciando Extração das Informações...')
  
  def run_sub ():
    try:
      wb = cli.open_wb (file_name)
      output_text = cli.format_message (wb.active)
      emojized_output = cli.emojize (output_text)
    
    except FileNotFoundError:
      feedback_label.config (text = 'Erro! Não foi possível abrir o arquivo.')

    except:
      feedback_label.config (text = 'Erro ao fazer o parser do arquivo selecionado.\nVerificar se a planilha está no formato que foi desenvolvido.')
    
    else:
      feedback_label.config (text = 'Healthcheck Gerado com Sucesso!!')


    text_box_output.delete ('1.0', END)
    text_box_output.insert (END, emojized_output)
  
  threading.Thread (target = run_sub).start ()

def send_msg_btn_event_handler (event = None):
  def run_sub ():
    if send_msg_btn ['state'] == DISABLED:
        feedback_label.config (text = 'O envio de mensagens ao Teams está desabilitado.\nNão foi possível ler o arquivo de configuração.')
        return

    try:
      feedback_label.config (text = 'Enviando mensagem...')
      cli.send_teams_message (text_box_output.get ('1.0', END))
      feedback_label.config (text = 'Mensagem enviada!')

    except:
      feedback_label.config (text = 'Erro ao enviar mensagem ao Teams.\nVerifique sua URL do Webhook no arquivo de configuração ou suas configurações de rede.')

  threading.Thread (target = run_sub).start ()

def copy_btn_event_handler ():
  try:
    if len (text_box_output.get ('1.0', END)) == 1:
      feedback_label.config (text = 'Não há nada para ser copiado!')
      return
    
    root.clipboard_clear ()
    root.clipboard_append (text_box_output.get ('1.0', END))

  except:
    feedback_label.config (text = 'Erro ao copiar para a área de transferência.')

  else:
    feedback_label.config (text = 'Mensagem copiada!!')
  
def quit_btn_event_handler ():
  root.destroy ()



main_btn = Button (
  root,
  text = 'Selecionar Planilha',
  width = 65,
  height = 2,
  command = main_btn_event_handler
)
main_btn.place (x = 15, y = 60)
main_btn.pack (pady = 20)


feedback_label = Label (
  root,
  text = ''
)
feedback_label.pack (pady = 20)


text_box_output = Text (
  root,
  width = 57,
  height = 20
)
text_box_output.place (x = 15, y = 150)


send_msg_btn = Button (
  root,
  text = 'Enviar Mensagem Teams',
  width = 30,
  height = 2,
  state = DISABLED,
  command = send_msg_btn_event_handler
)
send_msg_btn.bind ('<Button-1>', send_msg_btn_event_handler)
send_msg_btn.place (x = 15, y = 490)

if cli.ms_teams_webhook:
  send_msg_btn ['state'] = NORMAL
else:
  feedback_label.config (text = 'O envio de mensagens ao Teams está desabilitado.\nNão foi possível ler o arquivo de configuração.')


copy_btn = Button (
  root,
  text = 'Copiar',
  width = 30,
  height = 2,
  command = copy_btn_event_handler
)
copy_btn.place (x = 255, y = 490)


quit_btn = Button (
  root,
  text = 'Sair',
  width = 30,
  height = 2,
  command = quit_btn_event_handler
)
quit_btn.place (x = 15, y = 545)


root.mainloop ()
