#%% Librerías

import pandas as pd
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict


#%% Clases

@dataclass
class UP:
    id: str
    fazenda: str
    db: float
    volume: float
    rsp: float
    data_colheita: datetime
    idade_floresta: float
    reservado: str
    volume_restante: float = None
    transportes: List[Dict] = None
    
    def __post_init__(self):
        self.volume_restante = self.volume
        self.transportes = []

@dataclass
class Transportador:
    nome: str
    frota_min: int
    frota_max: int
    qtd_gruas: int
    porcentagem_veiculos_min: float
    fazenda_atual: str = None
    up_atual: str = None

@dataclass
class Rota:
    origem: str
    destino: str
    transportador: str
    caixa_carga: float
    tempo_ciclo: float
    ciclo_lento: bool
    fazenda: str

@dataclass
class DemandaFabrica:
    dia: int
    fabrica: str
    demanda_min: float
    demanda_max: float
    rsp_min: float
    rsp_max: float

@dataclass
class DiaHorizonte:
    dia: int
    mes: int
    ano: int
    ciclo_lento: bool


#%% Función carga de datos
def cargar_datos(archivo_excel: str):
    """Carga y estructura los datos del archivo Excel proporcionado"""
    
    # Cargar cada hoja del Excel
    horizonte_df = pd.read_excel(archivo_excel, sheet_name='HORIZONTE')
    bd_up_df = pd.read_excel(archivo_excel, sheet_name='BD_UP')
    frota_df = pd.read_excel(archivo_excel, sheet_name='FROTA')
    grua_df = pd.read_excel(archivo_excel, sheet_name='GRUA')
    fabrica_df = pd.read_excel(archivo_excel, sheet_name='FABRICA')
    rota_df = pd.read_excel(archivo_excel, sheet_name='ROTA')
    
    # Limpiar y preparar datos
    horizonte_df['CICLO_LENTO'] = horizonte_df['CICLO_LENTO'].fillna('').apply(lambda x: x == 'X')
    bd_up_df['DATA_COLHEITA'] = pd.to_datetime(bd_up_df['DATA_COLHEITA'])
    bd_up_df['PRECIPITACAO'] = pd.to_numeric(bd_up_df['PRECIPITACAO'], errors='coerce')
    
    # Crear estructuras de datos
    ups = {}
    for _, row in bd_up_df.iterrows():
        up = UP(
            id=row['UP'],
            fazenda=row['FAZENDA'],
            db=row['DB'],
            volume=row['VOLUME'],
            rsp=row['RSP'],
            data_colheita=row['DATA_COLHEITA'],
            idade_floresta=row['IDADE_FLORESTA'],
            reservado=row['RESERVADO']
        )
        ups[up.id] = up
    
    transportadores = {}
    for _, row in frota_df.iterrows():
        # Obtener datos de grúa para este transportador
        grua_info = grua_df[grua_df['TRANSPORTADOR'] == row['TRANSPORTADOR']].iloc[0]
        
        transportador = Transportador(
            nome=row['TRANSPORTADOR'],
            frota_min=row['FROTA_MIN'],
            frota_max=row['FROTA_MAX'],
            qtd_gruas=grua_info['QTD_GRUAS'],
            porcentagem_veiculos_min=grua_info['PORCENTAGEM_VEICULOS_MIN']
        )
        transportadores[transportador.nome] = transportador
    
    rotas = []
    for _, row in rota_df.iterrows():
        rota = Rota(
            origem=row['ORIGEM'],
            destino=row['DESTINO'],
            transportador=row['TRANSPORTADOR'],
            caixa_carga=row['CAIXA_CARGA'],
            tempo_ciclo=row['TEMPO_CICLO'],
            ciclo_lento=row['CICLO_LENTO'] == 1,
            fazenda=row['Fazenda']
        )
        rotas.append(rota)
    
    demandas = []
    for _, row in fabrica_df.iterrows():
        demanda = DemandaFabrica(
            dia=row['DIA'],
            fabrica=row['FABRICA'],
            demanda_min=row['DEMANDA_MIN'],
            demanda_max=row['DEMANDA_MAX'],
            rsp_min=row['RSP_MIN'],
            rsp_max=row['RSP_MAX']
        )
        demandas.append(demanda)
    
    dias_horizonte = []
    for _, row in horizonte_df.iterrows():
        dia = DiaHorizonte(
            dia=row['DIA'],
            mes=row['MES'],
            ano=row['ANO'],
            ciclo_lento=row['CICLO_LENTO']
        )
        dias_horizonte.append(dia)
    
    return {
        'ups': ups,
        'transportadores': transportadores,
        'rotas': rotas,
        'demandas': demandas,
        'dias_horizonte': dias_horizonte
    }



#%% Ejemplooooo

datos = cargar_datos('generic_input_case.xlsx')

# Info cargada
print(f"{len(datos['ups'])} UPs:")
for up in datos['ups']:
    print(f"  {datos['ups'][up]}")
print(f"{len(datos['transportadores'])} transportadores")
for transp in datos['transportadores']:
    print(f"  {datos['transportadores'][transp]}")
print(f"{len(datos['rotas'])} rutas")
for ruta in datos['rotas']:
    print(f"  {ruta}")
print(f"{len(datos['demandas'])} días de demanda de fábrica")
for dem in datos['demandas']:
    print(f"  {dem}")
print(f"{len(datos['dias_horizonte'])} días en el horizonte")
for dias in datos['dias_horizonte']:
    print(f"  {dias}")

# %%
print(datos['ups']['S6C421'].db)
# %%
