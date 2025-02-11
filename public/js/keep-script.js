// بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ  ﷺ
// InshaAllah, By his marcy I will Gain Success

document.addEventListener('DOMContentLoaded', loadNotes);
let notes=[];
function addNote() {
    const title = document.getElementById('note-title').value.trim();
    const text = document.getElementById('note-text').value.trim();
    if (title.trim()  === '' && text.trim() === '') return;

    const note = {
        id: Date.now(),
        title,
        description:text
    };

    saveNoteToDB(note);
    renderNote(note);
    document.getElementById('note-title').value = '';
    document.getElementById('note-text').value = '';
}

function renderNote(note) {
    const notesGrid = document.getElementById('notes-grid');
    const noteCard = document.createElement('div');
    noteCard.classList.add('note-card');
    noteCard.setAttribute('data-id', note.id);
    noteCard.innerHTML = `
        <h3 class="note-title">${note.title}</h3>
        <p class="note-text">${note.text}</p>
        <button class="delete-btn" onclick="deleteNote(${note.id})">
            <i class="fas fa-trash"></i>
        </button>
    `;
    notesGrid.appendChild(noteCard);
}

async function saveNoteToDB(note) { 
    notes.push(note);
    let response= await fetch(window.location.origin +'/api/notes',{
        method :'post',
        body:JSON.stringify( { ...note }),
        headers :{'Content-Type':"application/json"}
    })
}

async function loadNotes() {
    notes =(await (await fetch(window.location.origin +'/api/notes')).json() )|| [];
    notes.forEach(renderNote);
}

function deleteNote(id) {
    let notes = JSON.parse(localStorage.getItem('notes')) || [];
    notes = notes.filter(note => note.id !== id);
    localStorage.setItem('notes', JSON.stringify(notes));
    
    document.querySelector(`[data-id='${id}']`).remove();
}
