import pandas as pd
import fastf1

# Nossa função refatorada e blindada
def extrair_telemetria_piloto(ano, gp, piloto):
    session = fastf1.get_session(ano, gp, 'R')
    session.load(telemetry=False, weather=False) 
    
    voltas_piloto = session.laps.pick_drivers(piloto).pick_accurate() 
    
    dados_modeloML = voltas_piloto[['LapNumber', 'Stint', 'Compound', 'TyreLife', 'LapTime']].copy()
    dados_modeloML['LapTime'] = dados_modeloML['LapTime'].dt.total_seconds()
    
    # Filtro dinâmico
    tempo_minimo = dados_modeloML['LapTime'].min()
    limite_tempo = tempo_minimo * 1.10
    dados_modeloML = dados_modeloML[dados_modeloML['LapTime'] <= limite_tempo] 
    
    # Colunas de pneus
    dados_modeloML = pd.get_dummies(dados_modeloML, columns=['Compound'], dtype=int) 
    
    compostos_esperados = ['Compound_SOFT', 'Compound_MEDIUM', 'Compound_HARD', 'Compound_INTERMEDIATE', 'Compound_WET']
    for composto in compostos_esperados:
        if composto not in dados_modeloML.columns:
            dados_modeloML[composto] = 0
            
    return dados_modeloML

# --- BLOCO DE TESTE ---
if __name__ == "__main__":
    print("Iniciando extração: Verstappen - GP do Brasil 2024...")
    
    # Chamando a função para um circuito longo
    df_teste = extrair_telemetria_piloto(2024, 'Brazil Grand Prix', 'VER')
    
    print("\n✅ Extração Concluída!")
    print("\n--- Primeiras 5 linhas extraídas ---")
    print(df_teste.head())
    
    print("\n--- Verificação das Colunas de Pneus (Devem aparecer todas) ---")
    print(df_teste.columns.tolist())
    
    print(f"\nTotal de voltas prontas para o ML: {len(df_teste)}")