import streamlit as st
import bcrypt
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import datetime
from typing import Optional, Dict, Any

class AuthManager:
    """Handle user authentication and database operations"""
    
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL')
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)
    
    def init_database(self):
        """Initialize the user database tables"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    # Create users table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            email VARCHAR(255) UNIQUE NOT NULL,
                            name VARCHAR(255) NOT NULL,
                            password_hash TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            last_login TIMESTAMP,
                            profile_data JSONB DEFAULT '{}',
                            preferences JSONB DEFAULT '{}'
                        )
                    """)
                    
                    # Create user_skills table for skill tracking
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS user_skills (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                            skill_name VARCHAR(255) NOT NULL,
                            proficiency_level INTEGER DEFAULT 1,
                            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            UNIQUE(user_id, skill_name)
                        )
                    """)
                    
                    # Create job_searches table for tracking user searches
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS job_searches (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                            search_query TEXT NOT NULL,
                            filters JSONB DEFAULT '{}',
                            results_count INTEGER DEFAULT 0,
                            search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    
                    # Create saved_jobs table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS saved_jobs (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                            job_id VARCHAR(255) NOT NULL,
                            job_title VARCHAR(255),
                            company VARCHAR(255),
                            salary_min INTEGER,
                            salary_max INTEGER,
                            location VARCHAR(255),
                            saved_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            UNIQUE(user_id, job_id)
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
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO users (email, name, password_hash)
                        VALUES (%s, %s, %s)
                        RETURNING id
                    """, (email, name, password_hash))
                    
                    user_id = cur.fetchone()['id']
                    conn.commit()
                    return True
                    
        except psycopg2.IntegrityError:
            return False  # User already exists
        except Exception as e:
            st.error(f"Error creating user: {e}")
            return False
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user login"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, email, name, password_hash, profile_data, preferences
                        FROM users 
                        WHERE email = %s
                    """, (email,))
                    
                    user = cur.fetchone()
                    
                    if user and self.verify_password(password, user['password_hash']):
                        # Update last login
                        cur.execute("""
                            UPDATE users 
                            SET last_login = CURRENT_TIMESTAMP 
                            WHERE id = %s
                        """, (user['id'],))
                        conn.commit()
                        
                        return {
                            'id': user['id'],
                            'email': user['email'],
                            'name': user['name'],
                            'profile_data': user['profile_data'] or {},
                            'preferences': user['preferences'] or {}
                        }
                    
                    return None
                    
        except Exception as e:
            st.error(f"Authentication error: {e}")
            return None
    
    def update_user_profile(self, user_id: int, profile_data: Dict[str, Any]) -> bool:
        """Update user profile data"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE users 
                        SET profile_data = %s 
                        WHERE id = %s
                    """, (psycopg2.extras.Json(profile_data), user_id))
                    conn.commit()
                    return True
                    
        except Exception as e:
            st.error(f"Error updating profile: {e}")
            return False
    
    def add_user_skill(self, user_id: int, skill_name: str, proficiency_level: int = 1) -> bool:
        """Add or update user skill"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO user_skills (user_id, skill_name, proficiency_level)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (user_id, skill_name) 
                        DO UPDATE SET proficiency_level = %s, added_date = CURRENT_TIMESTAMP
                    """, (user_id, skill_name, proficiency_level, proficiency_level))
                    conn.commit()
                    return True
                    
        except Exception as e:
            st.error(f"Error adding skill: {e}")
            return False
    
    def get_user_skills(self, user_id: int) -> list:
        """Get user skills"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT skill_name, proficiency_level, added_date
                        FROM user_skills 
                        WHERE user_id = %s
                        ORDER BY added_date DESC
                    """, (user_id,))
                    
                    return cur.fetchall()
                    
        except Exception as e:
            st.error(f"Error fetching skills: {e}")
            return []
    
    def save_job_search(self, user_id: int, search_query: str, filters: Dict[str, Any], results_count: int) -> bool:
        """Save user job search"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO job_searches (user_id, search_query, filters, results_count)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, search_query, psycopg2.extras.Json(filters), results_count))
                    conn.commit()
                    return True
                    
        except Exception as e:
            st.error(f"Error saving search: {e}")
            return False
    
    def save_job(self, user_id: int, job_data: Dict[str, Any]) -> bool:
        """Save a job for user"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO saved_jobs (user_id, job_id, job_title, company, salary_min, salary_max, location)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (user_id, job_id) DO NOTHING
                    """, (
                        user_id, 
                        job_data.get('job_id'),
                        job_data.get('title'),
                        job_data.get('company'),
                        job_data.get('salary_min'),
                        job_data.get('salary_max'),
                        job_data.get('location')
                    ))
                    conn.commit()
                    return True
                    
        except Exception as e:
            st.error(f"Error saving job: {e}")
            return False
    
    def get_saved_jobs(self, user_id: int) -> list:
        """Get user's saved jobs"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT job_id, job_title, company, salary_min, salary_max, location, saved_date
                        FROM saved_jobs 
                        WHERE user_id = %s
                        ORDER BY saved_date DESC
                    """, (user_id,))
                    
                    return cur.fetchall()
                    
        except Exception as e:
            st.error(f"Error fetching saved jobs: {e}")
            return []