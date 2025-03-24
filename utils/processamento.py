import pandas as pd
import numpy as np

DATA_PATH = "data/N_seaice_extent_daily_v3.0.csv"


def carregar_dados(caminho=DATA_PATH):
    df = pd.read_csv(caminho)
    df = df[1:].copy()  # remove linha de cabeçalho extra
    df.columns = ["Year", "Month", "Day", "Extent", "Missing", "Source"]
    df["Year"] = df["Year"].astype(int)
    df["Month"] = df["Month"].astype(int)
    df["Day"] = df["Day"].astype(int)
    df["Extent"] = pd.to_numeric(df["Extent"], errors="coerce")
    df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
    df = df[df["Year"] <= 2024]  # filtra até 2024
    df.sort_values("Date", inplace=True)
    return df.reset_index(drop=True)


def media_anual(df):
    df["Year"] = df["Date"].dt.year
    return df.groupby("Year")["Extent"].mean().reset_index()


def media_mensal(df):
    df["Month"] = df["Date"].dt.month
    return df.groupby("Month")["Extent"].mean().reset_index()


def media_por_estacao(df):
    df["Month"] = df["Date"].dt.month
    df["Estacao"] = df["Month"].apply(classificar_estacao)
    return df.groupby("Estacao")["Extent"].mean().reindex(["Verão", "Outono", "Inverno", "Primavera"])


def tendencia_estacional(df):
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Estacao"] = df["Month"].apply(classificar_estacao)
    return df.groupby(["Year", "Estacao"])["Extent"].mean().reset_index()


def classificar_estacao(mes):
    if mes in [12, 1, 2]:
        return "Verão"
    elif mes in [3, 4, 5]:
        return "Outono"
    elif mes in [6, 7, 8]:
        return "Inverno"
    else:
        return "Primavera"
