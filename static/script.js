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

let currentFilename = null;

async function uploadResume() {
    const file = fileInput.files[0];
    if (!file) { alert('Please choose a file first.'); return; }

    show('loader'); hide('dashboard'); hide('errorBox'); hide('matchSection');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res  = await fetch('/upload', { method: 'POST', body: formData });
        const json = await res.json();
        if (json.error) { showError(json.error); return; }

        currentFilename = json.filename;  // Store for matching
        renderDashboard(json.data);
        show('matchSection');             // Show match section after parse
    } catch (e) {
        showError('Something went wrong. Please try again.');
    } finally {
        hide('loader');
    }
}

async function analyzeMatch() {
    const jd = document.getElementById('jobDesc').value.trim();
    if (!jd) { alert('Please paste a job description first.'); return; }
    if (!currentFilename) { alert('Please upload a resume first.'); return; }

    try {
        const res  = await fetch(`/match/${encodeURIComponent(currentFilename)}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ job_description: jd })
        });
        const json = await res.json();
        if (json.error) { alert(json.error); return; }

        renderMatchResult(json.match);
    } catch (e) {
        alert('Match analysis failed. Please try again.');
    }
}

function renderMatchResult(match) {
    document.getElementById('scoreValue').textContent  = match.score + '%';
    document.getElementById('scoreDetail').textContent =
        `${match.total_matched} of ${match.total_jd_skills} required skills found`;

    // Color code the score
    const circle = document.getElementById('scoreCircle');
    if (match.score >= 70)      circle.style.background = '#2d6a4f';
    else if (match.score >= 40) circle.style.background = '#e6a817';
    else                        circle.style.background = '#c0392b';

    // Matched skills
    const matchedEl = document.getElementById('matchedSkills');
    matchedEl.innerHTML = match.matched_skills.length
        ? match.matched_skills.map(s => `<span class="skill-tag">${s}</span>`).join('')
        : '<p style="color:#888">None matched</p>';

    // Missing skills
    const missingEl = document.getElementById('missingSkills');
    missingEl.innerHTML = match.missing_skills.length
        ? match.missing_skills.map(s => `<span class="missing-tag">${s}</span>`).join('')
        : '<p style="color:#2d6a4f">No critical gaps!</p>';

    show('matchResult');
}