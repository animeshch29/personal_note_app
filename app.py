from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Step 3: Database initialization function
def init_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 title TEXT, 
                 content TEXT)''')
    conn.commit()
    conn.close()

# Call the database initialization function when the app starts
init_db()

# Step 4: Routes for CRUD Operations

# Home Route (List Notes)
@app.route('/')
def index():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

# Add Note Route
@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_note.html')

# Edit Note Route
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        c.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    c.execute("SELECT * FROM notes WHERE id = ?", (id,))
    note = c.fetchone()
    conn.close()
    return render_template('edit_note.html', note=note)

# Delete Note Route
@app.route('/delete/<int:id>')
def delete_note(id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
