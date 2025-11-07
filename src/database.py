import sqlite3
import json
from datetime import datetime
import os

class HistoryDatabase:
    def __init__(self, db_name="faktorial_history.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Inisialisasi database dan tabel"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_number INTEGER NOT NULL,
                result TEXT NOT NULL,
                calculation TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_calculation(self, input_number, result, calculation):
        """Menyimpan perhitungan ke database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO history (input_number, result, calculation)
            VALUES (?, ?, ?)
        ''', (input_number, str(result), calculation))
        
        conn.commit()
        conn.close()
    
    def get_all_history(self):
        """Mengambil semua history"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM history 
            ORDER BY timestamp DESC
        ''')
        
        history = cursor.fetchall()
        conn.close()
        return history
    
    def clear_history(self):
        """Menghapus semua history"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM history')
        
        conn.commit()
        conn.close()
    
    def get_statistics(self):
        """Mendapatkan statistik penggunaan"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM history')
        total_calculations = cursor.fetchone()[0]
        
        cursor.execute('SELECT MAX(input_number) FROM history')
        max_number = cursor.fetchone()[0]
        
        cursor.execute('SELECT timestamp FROM history ORDER BY timestamp DESC LIMIT 1')
        last_calculation = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_perhitungan': total_calculations,
            'angka_tertinggi': max_number if max_number else 0,
            'terakhir_dihitung': last_calculation[0] if last_calculation else 'Belum ada'
        }