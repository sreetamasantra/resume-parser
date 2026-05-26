const fileInput = document.getElementById('fileInput');
const fileName  = document.getElementById('fileName');

fileInput.addEventListener('change', () => {
    fileName.textContent = fileInput.files[0]?.name || 'No file chosen';
});

async function uploadResume() {
    const file = fileInput.files[0];
    if (!file) { alert('Please choose a file first.'); return; }

    // Show loader, hide others
    show('loader'); hide('dashboard'); hide('errorBox');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res  = await fetch('/upload', { method: 'POST', body: formData });
        const json = await res.json();

        if (json.error) { showError(json.error); return; }

        renderDashboard(json.data);
    } catch (e) {
        showError('Something went wrong. Please try again.');
    } finally {
        hide('loader');
    }
}

function renderDashboard(data) {
    // Profile
    const initials = (data.name || '?').split(' ').map(w => w[0]).join('').slice(0,2);
    document.getElementById('avatarInitials').textContent = initials;
    document.getElementById('resName').textContent = data.name || 'Unknown';
    document.getElementById('resEmail').innerHTML  = `📧 ${data.email || 'N/A'}`;
    document.getElementById('resPhone').innerHTML  = `📞 ${data.phone || 'N/A'}`;

    // Links
    setLink('resLinkedin', data.linkedin);
    setLink('resGithub',   data.github);

    // Skills
    const skillsEl = document.getElementById('skillsList');
    skillsEl.innerHTML = data.skills.length
        ? data.skills.map(s => `<span class="skill-tag">${s}</span>`).join('')
        : '<p>No skills detected</p>';

    // Education
    fillList('educationList', data.education);

    // Experience
    fillList('experienceList', data.experience);

    show('dashboard');
}

function setLink(id, url) {
    const el = document.getElementById(id);
    if (url) { el.href = url; el.classList.remove('hidden'); }
    else { el.classList.add('hidden'); }
}

function fillList(id, items) {
    const el = document.getElementById(id);
    el.innerHTML = items.length
        ? items.map(i => `<li>${i}</li>`).join('')
        : '<li>Not detected</li>';
}

function showError(msg) {
    const el = document.getElementById('errorBox');
    el.textContent = msg;
    show('errorBox'); hide('loader');
}

function show(id) { document.getElementById(id).classList.remove('hidden'); }
function hide(id) { document.getElementById(id).classList.add('hidden'); } 