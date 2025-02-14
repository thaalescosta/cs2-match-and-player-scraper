from _functions.get_urls import get_urls
from _functions.get_match_id import get_match_ids
from _functions.api_request import api_request
from _functions.download_files import download_files
from _functions.unrar import unrar
from _functions.extrair_dados import run_csda_on_demos
from _ETL.merge_files import merge_csv_files
import os

'''
CT SIDE = 2
T SIDE = 3
'''

root = os.getcwd()

# id_event = ["7909", "7903", "7524", "7557"]
id_event = ["7909", "7903"]

match_urls, camp, camp_var = get_urls(7909)

print(f"{match_urls}\n{camp}\n{camp_var}")

for id in id_event:
    # OBTER URL DE TODOS OS JOGOS DO CAMPEONATO
    match_urls, camp, camp_var = get_urls(id)

    # OBTER A ID CORRESPONDENTE A CADA CONFRONTO
    match_ids = get_match_ids(*match_urls) 

    # OBTER O LINK DE DOWNLOAD DAS DEMOS CADA CONFRONTO
    download_links = api_request(*match_ids)

    # BAIXAR OS ARQUIVOS .RAR DAS DEMOS
    download_files(*download_links, camp=camp, root=root)

    # EXTRAIR OS ARQUIVOS .RAR
    unrar(camp=camp)

    demos_path = os.path.join(root,"Demos")
    demos_path = os.path.join(demos_path,camp)
    output_path = os.path.join(root,"Dados")
    csda_path = os.path.join(root, "csda.exe")
    tabelas_finais = os.path.join(root, "Tabelas Finais")

    # EXTRAIR DADOS DAS DEMOS
    run_csda_on_demos(csda_path, demos_path, output_path, camp)

    merge_csv_files(camp, camp_var, output_path, tabelas_finais)