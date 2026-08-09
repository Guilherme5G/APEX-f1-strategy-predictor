import pandas as pd
import fastf1
import os

# Configura o cache dinamicamente ao importar o módulo
if not os.path.exists('../cache'):
    os.makedirs('../cache')
fastf1.Cache.enable_cache('../cache')

def extrair_telemetria_piloto(ano, gp, piloto):
    session = fastf1.get_session(ano, gp, 'R')
    session.load(telemetry=False, weather=False) 
    
    voltas_piloto = session.laps.pick_drivers(piloto).pick_accurate() 
    
    dados_modeloML = voltas_piloto[['LapNumber', 'Stint', 'Compound', 'TyreLife', 'LapTime']].copy()
    dados_modeloML['LapTime'] = dados_modeloML['LapTime'].dt.total_seconds()
    
    tempo_minimo = dados_modeloML['LapTime'].min()
    limite_tempo = tempo_minimo * 1.10
    dados_modeloML = dados_modeloML[dados_modeloML['LapTime'] <= limite_tempo] 
    
    dados_modeloML = pd.get_dummies(dados_modeloML, columns=['Compound'], dtype=int) 
    
    compostos_esperados = ['Compound_SOFT', 'Compound_MEDIUM', 'Compound_HARD', 'Compound_INTERMEDIATE', 'Compound_WET']
    for composto in compostos_esperados:
        if composto not in dados_modeloML.columns:
            dados_modeloML[composto] = 0
            
    return dados_modeloML