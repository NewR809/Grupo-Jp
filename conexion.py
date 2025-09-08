from config import DB_CONFIG
import mysql.connector

def crear_conexion():
    return mysql.connector.connect(**DB_CONFIG)