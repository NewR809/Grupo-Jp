import csv
import os

def guardar_csv(archivo, datos):
    with open(archivo, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(datos)

def leer_csv(archivo):
    if not os.path.exists(archivo):
        return []
    with open(archivo, mode='r', encoding='utf-8') as f:
        return list(csv.reader(f))