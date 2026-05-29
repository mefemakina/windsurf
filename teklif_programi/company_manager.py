import sqlite3
import json
import os
from datetime import datetime

class CompanyManager:
    def __init__(self, db_path):
        db_file = os.path.join(db_path, 'teklif.db')
        self.conn = sqlite3.connect(db_file)
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                tax_no TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        
    def add_company(self, name, tax_no=None, phone=None, email=None, address=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO companies (name, tax_no, phone, email, address)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, tax_no, phone, email, address))
        self.conn.commit()
        return cursor.lastrowid
        
    def get_all_companies(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, tax_no, phone, email, address FROM companies ORDER BY name')
        return cursor.fetchall()
        
    def get_company(self, company_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM companies WHERE id = ?', (company_id,))
        return cursor.fetchone()
        
    def get_company_id_by_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM companies WHERE name = ?', (name,))
        result = cursor.fetchone()
        return result[0] if result else None
        
    def update_company(self, company_id, name, tax_no=None, phone=None, email=None, address=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE companies 
            SET name=?, tax_no=?, phone=?, email=?, address=?
            WHERE id=?
        ''', (name, tax_no, phone, email, address, company_id))
        self.conn.commit()
        
    def delete_company(self, company_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM companies WHERE id = ?', (company_id,))
        self.conn.commit()
        
    def close(self):
        self.conn.close()
