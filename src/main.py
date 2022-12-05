import openpyxl, sys, emoji, requests, json
from datetime import datetime

try:
  file_name = sys.argv [1]
  wb = openpyxl.load_workbook (filename = file_name, data_only = True)
except FileNotFoundError:
  print (f'Não foi possível abrir o arquivo {file_name}. Verifique se o caminho do arquivo está correto.')
  exit (1)
except IndexError:
  # To Do: Implement usage function.
  print (f'Nome do arquivo de entrada não foi informado.')
  exit (1)




msg_template = '''
{em01} Health-Check Backup

{em02} {data_hora}

{em03} Infraestrutura

(AVAMAR E VEEAM)

RJ1

{em04} Área Ocupada: {area_ocupada_rj1}%

{em05} Área Livre: {area_livre_rj1} TB

{em06} {cres_dec_str_rj1}: {cres_dec_value_rj1} TB

RJ2

{em07} Área Ocupada: {area_ocupada_rj2}%

{em08} Área Livre: {area_livre_rj2} TB

{em09} {cres_dec_str_rj2}: {cres_dec_value_rj2} TB

{em10} Replicação AWS

{em11} RJ1 Executado: {rep_aws_executado_rj1}%

{em12} Dt última: {rep_aws_ultima_rj1}

{em13} Área Livre: {rep_aws_livre_rj1}%

{em14} RJ2 executado: {rep_aws_executado_rj2}%

{em15} Dt última: {rep_aws_ultima_rj2}

{em16} Área Livre: {rep_aws_livre_rj2}%


{em17} Execuções Data Center

{em18} JOBS RJ1: {jobs_rj1}

{em19} Executado: {jobs_executado_rj1}%

{em20} JOBS RJ2: {jobs_rj2}

{em21} Executado: {jobs_executado_rj2}%


{em22} Execuções Unidades

{em23} Escopo: {qtd_locais} Locais

{em24} Sucesso: {pct_sucesso_total}%
'''
ws = wb.active
status_column = tuple (ws.iter_cols (min_col = 4, max_col = 4, min_row = 8, values_only = True)) [0]
qtd_locais = len (status_column)
ms_webhook_endpoint = 'https://vtalcorp.webhook.office.com/webhookb2/d86744c3-007e-4d32-806e-ee45d82a4a30@85b28421-d45a-4b07-889d-24b528c7f250/IncomingWebhook/8fd9febc864942a685a335aaa45cbb33/05e806a2-a31b-43a7-ab4f-2a5a8374585c'

def conditional_emoji (rule, value = 0):
  match rule:
    case 1:
      return ':check_mark_button:' if value <= 79 else ':warning:' if value > 79 and value <= 90 else ':hollow_red_circle:'

    case 2:
      return ':hollow_red_circle:' if 'Falha' in status_column else ':warning:' if 'Parcial' in status_column else ':check_mark_button:'

def conditional_string (rule, value = 0):
  match rule:
    case 1:
      return 'Crescimento/dia' if value >= 0 else 'Redução nas últimas 24h'

emoji.EMOJI_DATA

output_text = msg_template.format (
  em01 = ':stethoscope:',
  em02 = ':spiral_calendar:', data_hora = datetime.now ().strftime ('%d/%m/%Y'),
  em03 = ':large_blue_diamond:',
  em04 = conditional_emoji (1, ws ['O3'].value * 100), area_ocupada_rj1 = int (ws ['O3'].value * 100),
  em05 = ':information:', area_livre_rj1 = ws ['I3'].value,
  em06 = ':information:', cres_dec_str_rj1 = conditional_string (1, ws ['J3'].value), cres_dec_value_rj1 = ws ['J3'].value,
  em07 = ':check_mark_button:', area_ocupada_rj2 = int (ws ['O4'].value * 100),
  em08 = ':information:', area_livre_rj2 = ws ['I4'].value,
  em09 = ':information:', cres_dec_str_rj2 = conditional_string (1, ws ['J4'].value), cres_dec_value_rj2 = ws ['J4'].value,
  em10 = ':large_blue_diamond:',
  em11 = ':check_mark_button:', rep_aws_executado_rj1 = ws ['G3'].value * 100,
  em12 = ':information:', rep_aws_ultima_rj1 = 'dd/mm/yyyy veriricar qual data considerar',
  em13 = ':check_mark_button:', rep_aws_livre_rj1 = ws ['K3'].value,
  em14 = ':check_mark_button:', rep_aws_executado_rj2 = ws ['G4'].value * 100,
  em15 = ':information:', rep_aws_ultima_rj2 = 'dd/mm/yyyy veriricar qual data considerar',
  em16 = ':check_mark_button:', rep_aws_livre_rj2 = ws ['K4'].value,
  em17 = ':large_blue_diamond:',
  em18 = ':information:', jobs_rj1 = ws ['N3'].value,
  em19 = ':information:', jobs_executado_rj1 = 'verificar como considerar o campo',
  em20 = ':information:', jobs_rj2 = ws ['N4'].value,
  em21 = ':information:', jobs_executado_rj2 = 'verificar como considerar o campo',
  em22 = ':large_blue_diamond:',
  em23 = conditional_emoji (2), qtd_locais = qtd_locais,
  em24 = ':information:', pct_sucesso_total = 'verificar como é considerado os status'
  
)


emojized_output = emoji.emojize (output_text)

print (emojized_output)

payload = {
  'text': emojized_output
}

requests.post (ms_webhook_endpoint, data = json.dumps (payload))


# range_d = ws.iter_cols (min_col = 4, max_col = 4, min_row = 8, values_only = True)

# for r in range_d:
#   print (r)


# 🩺 Health-Check Backup 
# 🗓 01-12-22

# 🔹 Infraestrutura
# (AVAMAR E VEEAM)

# RJ1
# ✅ Area Ocupada: 71%                 ['o3']
# ℹ️ Área Livre: 49,3 TB                 ['i3']
# ℹ️ Crescimento/dia: 0,6 TB             []

# RJ2
# ⚠️ Área Ocupada: 87%                  []
# ℹ️ Área Livre: 22,5 TB
# ℹ️ Redução nas últimas 24h: -2,5 TB

# 🔹 Replicação AWS
# ✅ RJ1 Executado: 100%
# ℹ️ Dt ultima: 30/11/2022
# ✅ Área Livre: 19%

# ✅ RJ2 executado: 100%
# ℹ️ Dt ultima: 30/11/2022
# ❌ Área Livre: 0%, processo de Cleaning em execução.

# 🔹 Execuções Data Center
# ℹ️ JOBS RJ1: 4161 
# ✅ Executado: 99,98%

# ℹ️ JOBS RJ2: 3049
# ✅ Executado: 100%


# 🔹 Execuções Unidades

# ℹ️ Escopo: 77 Locais

# ℹ️ Sucesso: 100%