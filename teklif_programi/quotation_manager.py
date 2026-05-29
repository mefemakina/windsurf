import sqlite3
import json
import os
from datetime import datetime

class QuotationManager:
    def __init__(self, db_path):
        db_file = os.path.join(db_path, 'teklif.db')
        self.conn = sqlite3.connect(db_file)
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quotation_no TEXT UNIQUE NOT NULL,
                date TEXT NOT NULL,
                company_id INTEGER,
                delivery_type TEXT,
                currency TEXT,
                total_amount REAL,
                notes TEXT,
                items TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies(id)
            )
        ''')
        self.conn.commit()
        
    def generate_quotation_no(self):
        """Generate quotation number in format C01-YYMMDD"""
        today = datetime.now()
        date_str = today.strftime("%y%m%d")
        
        # Get the count of quotations for today
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM quotations 
            WHERE quotation_no LIKE ?
        ''', (f'C%-{date_str}',))
        count = cursor.fetchone()[0]
        
        # Generate sequential number (01, 02, etc.)
        seq = str(count + 1).zfill(2)
        return f"C{seq}-{date_str}"
        
    def add_quotation(self, quotation_no, date, company_id, delivery_type, 
                     currency, total_amount, notes, items):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO quotations (quotation_no, date, company_id, delivery_type, 
                                   currency, total_amount, notes, items)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (quotation_no, date, company_id, delivery_type, 
              currency, total_amount, notes, json.dumps(items)))
        self.conn.commit()
        return cursor.lastrowid
        
    def get_all_quotations(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT q.quotation_no, q.date, c.name, q.delivery_type, 
                   q.currency, q.total_amount
            FROM quotations q
            LEFT JOIN companies c ON q.company_id = c.id
            ORDER BY q.created_at DESC
        ''')
        return cursor.fetchall()
        
    def get_quotation_by_no(self, quotation_no):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM quotations WHERE quotation_no = ?
        ''', (quotation_no,))
        result = cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'quotation_no': result[1],
                'date': result[2],
                'company_id': result[3],
                'delivery_type': result[4],
                'currency': result[5],
                'total_amount': result[6],
                'notes': result[7],
                'items': json.loads(result[8]) if result[8] else []
            }
        return None
        
    def get_quotation_by_id(self, quotation_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM quotations WHERE id = ?', (quotation_id,))
        result = cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'quotation_no': result[1],
                'date': result[2],
                'company_id': result[3],
                'delivery_type': result[4],
                'currency': result[5],
                'total_amount': result[6],
                'notes': result[7],
                'items': json.loads(result[8]) if result[8] else []
            }
        return None
        
    def update_quotation(self, quotation_id, date, company_id, delivery_type,
                        currency, total_amount, notes, items):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE quotations 
            SET date=?, company_id=?, delivery_type=?, currency=?, 
                total_amount=?, notes=?, items=?
            WHERE id=?
        ''', (date, company_id, delivery_type, currency, 
              total_amount, notes, json.dumps(items), quotation_id))
        self.conn.commit()
        
    def delete_quotation(self, quotation_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM quotations WHERE id = ?', (quotation_id,))
        self.conn.commit()
        
    def close(self):
        self.conn.close()
