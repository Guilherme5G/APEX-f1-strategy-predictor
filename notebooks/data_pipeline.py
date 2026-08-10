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
    # remove voltas com Safety Car / VSC / bandeira vermelha (so mantem pista 100% verde)
    voltas_piloto = voltas_piloto[voltas_piloto['TrackStatus'] == '1']

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


def carregar_lote_treinamento(ano, lista_gps, lista_pilotos):
    todas_voltas = []

    for gp in lista_gps:
        try:
            session = fastf1.get_session(ano, gp, 'R')
            session.load(telemetry=False, weather=False)

            voltas = session.laps.pick_drivers(lista_pilotos).pick_accurate()
            # remove voltas com Safety Car / VSC / bandeira vermelha
            voltas = voltas[voltas['TrackStatus'] == '1']

            df_gp = voltas[['LapNumber', 'Stint', 'Compound', 'TyreLife', 'LapTime']].copy()
            df_gp['LapTime'] = df_gp['LapTime'].dt.total_seconds()

            df_gp['EventName'] = session.event['EventName']
            df_gp['Driver'] = voltas['Driver']

            tempo_minimo = df_gp['LapTime'].min()
            df_gp = df_gp[df_gp['LapTime'] <= tempo_minimo * 1.10]

            df_gp = df_gp[df_gp['LapNumber'] > 1]

            todas_voltas.append(df_gp)
            print(f"Extracao OK: {gp}")

        except Exception as e:
            print(f"Erro ao extrair dados do GP {gp}: {e}")
            continue

    df_modeloML = pd.concat(todas_voltas, ignore_index=True)
    df_modeloML = pd.get_dummies(df_modeloML, columns=['Compound', 'EventName', 'Driver'], dtype=int)

    return df_modeloML