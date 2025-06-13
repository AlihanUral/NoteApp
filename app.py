from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# File to store notes
NOTES_FILE = 'notes.json'

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notlar', methods=['GET', 'POST'])
def notlar():
    notes = load_notes()
    
    if request.method == 'POST':
        new_note = request.form['note']
        title = request.form.get('title', '').strip()
        tags_input = request.form.get('tags', '')
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        
        notes.append({
            'content': new_note,
            'title': title,
            'tags': tags
        })
        save_notes(notes)
        return redirect(url_for('notlar'))
    
    # Get search query and tag filter
    search_query = request.args.get('search', '').lower()
    tag_filter = request.args.get('tag', '')
    
    # Filter notes based on search and tag
    filtered_notes = notes
    if search_query:
        filtered_notes = [note for note in filtered_notes 
                         if search_query in note['content'].lower() or 
                            search_query in note.get('title', '').lower()]
    if tag_filter:
        filtered_notes = [note for note in filtered_notes 
                         if tag_filter in note.get('tags', [])]
    
    # Get all unique tags for the filter dropdown
    all_tags = sorted(set(tag for note in notes for tag in note.get('tags', [])))
    
    return render_template('notlar.html', 
                         notes=filtered_notes, 
                         all_tags=all_tags,
                         current_tag=tag_filter)

@app.route('/sil_not/<int:index>')
def sil_not(index):
    notes = load_notes()
    if 0 <= index < len(notes):
        notes.pop(index)
        save_notes(notes)
    return redirect(url_for('notlar'))

@app.route('/cikis')
def cikis():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
    
    



