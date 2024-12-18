from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

notes = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notlar', methods=['GET', 'POST'])
def notlar():
    if request.method == 'POST':
        new_note = request.form['note']
        notes.append(new_note)
        return redirect(url_for('notlar'))
    
    return render_template('notlar.html', notes=notes)

@app.route('/sil_not/<int:index>')
def sil_not(index):
    
    if 0 <= index < len(notes):
        notes.pop(index)
    return redirect(url_for('notlar'))

@app.route('/cikis')
def cikis():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
    
    



