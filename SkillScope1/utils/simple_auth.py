import streamlit as st
import sqlite3
import bcrypt
import datetime
from typing import Optional, Dict, Any
import os

class SimpleAuthManager:
    """Simple SQLite-based authentication manager for development"""
    
    def __init__(self):
        self.db_path = "skillscope.db"
        self.init_database()
    
    def get_connection(self):
        """Get SQLite database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize the SQLite database tables"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        profile_data TEXT DEFAULT '{}',
                        preferences TEXT DEFAULT '{}'
                    )
                """)
                
                # Create user_skills table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_skills (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        skill_name TEXT NOT NULL,
                        proficiency_level INTEGER DEFAULT 1,
                        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, skill_name),
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                # Create job_searches table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS job_searches (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        search_query TEXT NOT NULL,
                        filters TEXT DEFAULT '{}',
                        results_count INTEGER DEFAULT 0,
                        search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                # Create saved_jobs table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS saved_jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        job_id TEXT NOT NULL,
                        job_title TEXT,
                        company TEXT,
                        salary_min INTEGER,
                        salary_max INTEGER,
                        location TEXT,
                        saved_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, job_id),
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                conn.commit()
        except Exception as e:
            st.error(f"Database initialization error: {e}")
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_user(self, email: str, name: str, password: str) -> bool:
        """Create a new user account"""
        try:
            password_hash = self.hash_password(password)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (email, name, password_hash)
                    VALUES (?, ?, ?)
                """, (email, name, password_hash))
                
                conn.commit()
                return True
                
        except sqlite3.IntegrityError:
            return False  # User already exists
        except Exception as e:
            st.error(f"Error creating user: {e}")
            return False
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, email, name, password_hash, profile_data
                    FROM users WHERE email = ?
                """, (email,))
                
                user_data = cursor.fetchone()
                
                if user_data and self.verify_password(password, user_data[3]):
                    # Update last login
                    cursor.execute("""
                        UPDATE users SET last_login = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (user_data[0],))
                    conn.commit()
                    
                    return {
                        'id': user_data[0],
                        'email': user_data[1],
                        'name': user_data[2],
                        'profile_data': user_data[4] if user_data[4] else {}
                    }
                return None
                
        except Exception as e:
            st.error(f"Authentication error: {e}")
            return None
    
    def update_user_profile(self, user_id: int, profile_data: Dict[str, Any]) -> bool:
        """Update user profile information"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET profile_data = ? WHERE id = ?
                """, (str(profile_data), user_id))
                
                conn.commit()
                return True
                
        except Exception as e:
            st.error(f"Profile update error: {e}")
            return False
