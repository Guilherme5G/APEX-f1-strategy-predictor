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
    # remove explicitamente voltas de entrada/saida de pit
    voltas_piloto = voltas_piloto[voltas_piloto['PitInTime'].isna() & voltas_piloto['PitOutTime'].isna()]

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


def carregar_lote_treinamento(ano, lista_gps, lista_pilotos, retornar_grupos=False):
    todas_voltas = []

    for gp in lista_gps:
        try:
            session = fastf1.get_session(ano, gp, 'R')
            session.load(telemetry=False, weather=False)

            voltas = session.laps.pick_drivers(lista_pilotos).pick_accurate()
            # remove voltas com Safety Car / VSC / bandeira vermelha
            voltas = voltas[voltas['TrackStatus'] == '1']
            # remove explicitamente voltas de entrada/saida de pit (reforco de seguranca,
            # pick_accurate() costuma pegar a maioria mas nem sempre todas)
            voltas = voltas[voltas['PitInTime'].isna() & voltas['PitOutTime'].isna()]

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

    # --- Suavizacao ---
    # Antes de normalizar, aplica mediana movel (janela=3) por stint. Isso filtra
    # picos de UMA volta isolada (trafego, susto, lock-up pontual) sem apagar a
    # tendencia real e gradual de degradacao do pneu ao longo do stint.
    df_modeloML['LapTime_Suavizado'] = df_modeloML.groupby(
        ['EventName', 'Driver', 'Stint']
    )['LapTime'].transform(lambda x: x.rolling(window=3, center=True, min_periods=1).median())

    # --- Normalizacao do alvo ---
    # LapTime absoluto e dominado pelo baseline de cada pista (Monaco ~70s vs Spa ~104s),
    # o que faz o modelo aprender "qual pista e essa" em vez de "como o pneu degrada".
    # LapTime_Normalizado = quanto mais lento a volta (suavizada) e em relacao a
    # melhor volta daquele mesmo stint (mesmo piloto, mesma corrida, mesmo set de pneu).
    # Isso isola o efeito de degradacao e fica comparavel entre pistas diferentes.
    df_modeloML['LapTime_Normalizado'] = df_modeloML.groupby(
        ['EventName', 'Driver', 'Stint']
    )['LapTime_Suavizado'].transform(lambda x: x - x.min())

    # --- Diagnostico: mostra os maiores outliers ANTES de cortar qualquer coisa ---
    # Ajuda a identificar se sao voltas de gerenciamento de ritmo (piloto com gap
    # grande poupando pneu/motor), trafego nao sinalizado, ou algum problema de dado.
    piores = df_modeloML.sort_values('LapTime_Normalizado', ascending=False).head(10)
    print("\n[Diagnostico] Top 10 maiores 'deltas' de LapTime_Normalizado (candidatos a ruido nao-fisico):")
    print(piores[['EventName', 'Driver', 'LapNumber', 'Stint', 'TyreLife', 'LapTime_Normalizado']].to_string(index=False))

    # --- Corte de outliers nao-fisicos ---
    # Deltas acima desse limiar raramente sao degradacao real de pneu -- geralmente
    # sao gerenciamento de ritmo, trafego, ou volta atipica isolada. O valor e uma
    # heuristica; ajuste observando a tabela impressa acima.
    LIMITE_DEGRADACAO_MAX = 2.5  # segundos
    n_antes = len(df_modeloML)
    df_modeloML = df_modeloML[df_modeloML['LapTime_Normalizado'] <= LIMITE_DEGRADACAO_MAX]
    n_removidas = n_antes - len(df_modeloML)
    print(f"\n[Diagnostico] Removidas {n_removidas} voltas ({n_removidas/n_antes:.1%}) com delta > {LIMITE_DEGRADACAO_MAX}s\n")

    # remove a coluna intermediaria de suavizacao -- ela e quase uma copia do alvo
    # (LapTime_Normalizado = LapTime_Suavizado - min), entao deixa-la em X seria
    # vazamento de dados (data leakage) direto para o modelo
    df_modeloML = df_modeloML.drop(columns=['LapTime_Suavizado'])

    # reseta o indice ANTES de capturar os grupos, para garantir alinhamento perfeito
    # entre grupos, X_train e y_train no notebook (o filtro acima deixou "buracos" no indice)
    df_modeloML = df_modeloML.reset_index(drop=True)

    # guarda o nome da corrida (para uso em split/CV por grupo) SOMENTE APOS os filtros/cortes,
    # senao grupos fica com linhas a mais que o df_modeloML final e o mask de treino/teste
    # no notebook fica desalinhado (pandas "reindexed to match", corrompendo o split silenciosamente)
    grupos = df_modeloML['EventName'].copy()

    df_modeloML = pd.get_dummies(df_modeloML, columns=['Compound', 'EventName', 'Driver'], dtype=int)

    if retornar_grupos:
        return df_modeloML, grupos

    return df_modeloML