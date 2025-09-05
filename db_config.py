import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
import pymysql
from pymysql.err import OperationalError, InternalError
import pandas as pd
import ssl
from flask import Flask, jsonify, request, Response  # Import Flask, jsonify, request, and Response
import subprocess  # Import subprocess for firewall function
from functools import wraps
import requests

def definir_conexion():
    DB_CONFIG = {
        "host": "yamanote.proxy.rlwy.net",
        "port": 18234,
        "user": "root",
        "password": "UyuZkiAaxFytvlevPCSrGMNPKhOeYxXT",
        "database": "railway",
        "charset": "utf8mb4",
    "cursorclass": "DictCursor"
}

    return pymysql.connect(**DB_CONFIG)

USERNAME = "powerbi"
PASSWORD = "secure123"