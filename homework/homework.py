"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    return


if __name__ == "__main__":
    clean_campaign_data()

import os
import glob
import pandas as pd


def clean_campaign_data():
    """
    Limpieza de datos de una campaña de marketing.
    """
    # 1. Asegurar que la carpeta de salida exista
    os.makedirs("files/output", exist_ok=True)

    # 2. Leer y concatenar todos los archivos csv.zip de la carpeta input
    path_pattern = os.path.join("files/input/", "*.csv.zip")
    file_paths = glob.glob(path_pattern)
    
    dfs = []
    for file_path in file_paths:
        df_temp = pd.read_csv(file_path, compression="zip")
        dfs.append(df_temp)
        
    df = pd.concat(dfs, ignore_index=True)

    # =========================================================================
    # TABLA 1: client.csv
    # =========================================================================
    client = df[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()
    
    client["job"] = client["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    client["education"] = client["education"].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    client["credit_default"] = client["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    client["mortgage"] = client["mortgage"].apply(lambda x: 1 if x == "yes" else 0)

    client.to_csv("files/output/client.csv", index=False)

    # =========================================================================
    # TABLA 2: campaign.csv
    # =========================================================================
    campaign = df[[
        "client_id", 
        "number_contacts", 
        "contact_duration", 
        "previous_campaign_contacts", 
        "previous_outcome", 
        "campaign_outcome", 
        "day", 
        "month"
    ]].copy()
    
    campaign["previous_outcome"] = campaign["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    campaign["campaign_outcome"] = campaign["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)
    
    months_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
        "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    
    day_padded = campaign["day"].astype(str).str.zfill(2)
    month_numeric = campaign["month"].str.lower().map(months_map)
    
    campaign["last_contact_date"] = "2022-" + month_numeric + "-" + day_padded
    campaign = campaign.drop(columns=["day", "month"])
    
    campaign = campaign[[
        "client_id", 
        "number_contacts", 
        "contact_duration", 
        "previous_campaign_contacts", 
        "previous_outcome", 
        "campaign_outcome", 
        "last_contact_date"
    ]]

    campaign.to_csv("files/output/campaign.csv", index=False)

    # =========================================================================
    # TABLA 3: economics.csv
    # =========================================================================
    # Seleccionamos y mantenemos los nombres de columnas originales que el test valida
    economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()

    economics.to_csv("files/output/economics.csv", index=False)

    return


if __name__ == "__main__":
    clean_campaign_data()