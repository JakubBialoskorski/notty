import os
import hashlib
from sqlalchemy import create_engine

def get_database_connection():
    engine = create_engine((os.environ['SQLALCHEMY_CONFIG']+'?charset=utf8mb4'), pool_size=25, max_overflow=5, pool_recycle=300, connect_args={'connect_timeout': 10})
    conn = engine.raw_connection()
    return conn

def check_user_exists(username, password):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        result = cursor.fetchone()
        if result:
            return result[0]
            cursor.close()
    except:
        return False
        cursor.close()

def check_username(username):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=%s', (username, ))
        if cursor.fetchone():
            return True
            cursor.close()
    except:
        return False
        cursor.close()

def signup_user(username, password, email):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(username, password, email) VALUES (%s, %s, %s)", (username, password, email))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()

def get_user_data(user_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id=%s', (str(user_id), ))
        results = cursor.fetchall()
        cursor.close()
        if len(results) == 0:
            return None
        return results
    except:
        cursor.close()

def get_data_using_user_id(id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE user_id=' + str(id))
        results = cursor.fetchall()
        cursor.close()
        if len(results) == 0:
            return None
        return results
    except:
        cursor.close()

def get_data_using_id(id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE id=' + str(id))
        results = cursor.fetchall()
        cursor.close()
        return results
    except:
        cursor.close()

def get_number_of_notes(id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(note) FROM notes WHERE user_id=' + str(id))
        results = cursor.fetchone()[0]
        cursor.close()
        return results
    except:
        cursor.close()

def get_data():
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes')
        results = cursor.fetchall()
        cursor.close()
        return results
    except:
        cursor.close()

def add_note(note_title, note, note_markdown, tags, user_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes(note_title, note, note_markdown, tags, user_id) VALUES (%s, %s, %s, %s, %s)", (note_title, note, note_markdown, tags, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()

def edit_note(note_title, note, note_markdown, tags, note_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE notes SET note_title=%s, note=%s, note_markdown=%s, tags=%s WHERE id=%s", (note_title, note, note_markdown, tags, note_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()

def delete_note_using_id(id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id=" + str(id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()

def generate_password_hash(password):
    hashed_value = hashlib.md5(password.encode())
    return hashed_value.hexdigest()

def add_tag(tag, user_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tags(tag, user_id) VALUES (%s, %s)", (tag, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()

def get_all_tags(user_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, tag FROM tags WHERE user_id=%s', (str(user_id), ))
        results = cursor.fetchall()
        if len(results) > 0:
            results = [(str(results[i][0]), results[i][1]) for i in range(len(results))]
        else:
            results = None
        cursor.close()
        return results
    except:
        cursor.close()

def get_data_using_tag_id(tag_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT tag FROM tags WHERE id=%s', (str(tag_id), ))
        results = cursor.fetchone()
        cursor.close()
        return results
    except:
        cursor.close()

def get_tag_using_note_id(id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT tags FROM notes WHERE id=%s', (str(id), ))
        results = cursor.fetchall()
        results = results[0][0].split(',')
        cursor.close()
        return results
    except:
        cursor.close()

def get_tagname_using_tag_id(tag_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT tag FROM tags WHERE id=%s', (str(tag_id), ))
        results = cursor.fetchone()
        cursor.close()
        return ''.join(results)
    except:
        cursor.close()

def delete_tag_using_id(tag_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tags WHERE id=" + str(tag_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()

def get_number_of_tags(id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(tag) FROM tags WHERE user_id=' + str(id))
        results = cursor.fetchone()[0]
        cursor.close()
        return results
    except:
        cursor.close()

def get_notes_using_tag_id(tag_id, username):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, note_title FROM notes WHERE user_id=%s AND tags like %s', (username, '%' + tag_id + '%'))
        results = cursor.fetchall()
        cursor.close()
        return results
    except:
        cursor.close()

def edit_email(email, user_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email=%s WHERE id=%s", (email, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()

def edit_password(password, user_id):
    conn = get_database_connection()
    password = generate_password_hash(password)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password=%s WHERE id=%s", (password, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()

def get_search_data(pattern, user_id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE user_id=%s AND note_title LIKE %s LIMIT 5", (user_id, '%' + pattern + '%'))
        results = cursor.fetchall()
        results = [(results[i][0], results[i][1]) for i in range(len(results))]
        cursor.close()
        return results
    except:
        cursor.close()

def get_rest_data_using_user_id(id):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE user_id=' + str(id))
        results = cursor.fetchall()
        fieldnames = [f[0] for f in cursor.description]
        cursor.close()
        if len(results) == 0:
            return None
        else:
            outer = {}
            for i in range(len(results)):
                data = {}
                for j in range(len(results[0])):
                    data[fieldnames[j]] = results[i][j]
                outer[int(i)] = data

            return outer
    except:
        cursor.close()