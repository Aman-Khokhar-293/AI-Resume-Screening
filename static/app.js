function showJSON(el, data) {
  el.textContent = JSON.stringify(data, null, 2);
}
function showError(el, err) {
  el.textContent = `Error: ${err?.message || err}`;
}

async function postJSON(path, body) {
  const res = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const text = await res.text();
  try { return { ok: res.ok, status: res.status, data: JSON.parse(text) } } catch { return { ok: res.ok, status: res.status, data: text } }
}
async function getJSON(path) {
  const res = await fetch(path);
  const text = await res.text();
  try { return { ok: res.ok, status: res.status, data: JSON.parse(text) } } catch { return { ok: res.ok, status: res.status, data: text } }
}

function parseSkills(str) {
  if (!str) return [];
  return str.split(',').map(s => s.trim()).filter(Boolean);
}

window.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('recruiter-form');
  const btn = document.getElementById('btn-run');
  const resumePreview = document.getElementById('resume-preview');

  // Preview resume text (supports .txt, .pdf via backend extraction)
  form.resume_file.addEventListener('change', async (e) => {
    const file = e.target.files?.[0];
    if (!file) { resumePreview.textContent = ''; return; }
    if (!(file.type?.startsWith('text') || file.name.endsWith('.txt') || file.type === 'application/pdf' || file.name.endsWith('.pdf'))) {
      resumePreview.textContent = 'Please upload a .txt or .pdf file.';
      return;
    }
    try {
      const body = new FormData();
      body.append('file', file);
      const res = await fetch('/api/extract-resume', { method: 'POST', body });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error || 'Failed to extract');
      resumePreview.textContent = json.text?.slice(0, 5000) || '';
    } catch (err) {
      resumePreview.textContent = `Preview error: ${err?.message || err}`;
    }
  });

  const resultsDiv = document.getElementById('results');
  const btnText = document.getElementById('btn-text');

  function renderSkillTags(container, skills, colorClass = '') {
    if (!skills || skills.length === 0) {
      container.innerHTML = '<span class="empty-state">None</span>';
      return;
    }
    container.innerHTML = skills.map(s => `<span class="skill-tag ${colorClass}">${s}</span>`).join('');
  }

  function getRecommendation(score) {
    if (score >= 80) return { text: 'Excellent match! This candidate strongly aligns with the job requirements. Highly recommended for interview.', class: 'success' };
    if (score >= 60) return { text: 'Good match. The candidate meets most requirements with some gaps in specific skills. Consider for interview.', class: 'info' };
    if (score >= 40) return { text: 'Moderate match. The candidate has some relevant skills but is missing several key requirements. May need additional training.', class: 'warning' };
    return { text: 'Low match. Significant gaps between candidate skills and job requirements. Not recommended unless other factors compensate.', class: 'danger' };
  }

  function animateScore(value) {
    const circle = document.getElementById('score-progress');
    const radius = 52;
    const circumference = 2 * Math.PI * radius;
    circle.style.strokeDasharray = circumference;
    const offset = circumference - (value / 100) * circumference;
    setTimeout(() => { circle.style.strokeDashoffset = offset; }, 100);
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    resultsDiv.hidden = true;

    const fd = new FormData(form);
    const title = fd.get('title');
    const description = fd.get('description');
    const required_skills = (fd.get('required_skills') || '').toString();
    const name = fd.get('name') || undefined;
    const email = fd.get('email') || undefined;
    const file = form.resume_file.files?.[0];

    if (!title || !description) { outMatch.textContent = 'Error: title and description are required'; return; }
    if (!file) { outMatch.textContent = 'Error: resume file is required'; return; }
    const isTxt = file.type?.startsWith('text') || file.name.endsWith('.txt');
    const isPdf = file.type === 'application/pdf' || file.name.endsWith('.pdf');
    if (!isTxt && !isPdf) { outMatch.textContent = 'Please upload a .txt or .pdf file.'; return; }

    btn.disabled = true;
    btnText.textContent = '⏳ Processing...';

    try {
      // 1) Create candidate from resume text (extract if PDF)
      let resume_text = '';
      if (isPdf) {
        const body = new FormData();
        body.append('file', file);
        const x = await fetch('/api/extract-resume', { method: 'POST', body });
        const j = await x.json();
        if (!x.ok) throw new Error(j.error || 'Failed to extract resume');
        resume_text = j.text || '';
      } else {
        resume_text = await file.text();
      }
      const candRes = await postJSON('/api/resumes', { name, email, resume_text });
      if (!candRes.ok) throw new Error('Failed to create candidate');
      const candData = candRes.data;

      // 2) Create job
      const jobRes = await postJSON('/api/jobs', {
        title,
        description,
        required_skills: required_skills ? required_skills.split(',').map(s => s.trim()).filter(Boolean) : []
      });
      if (!jobRes.ok) throw new Error('Failed to create job');
      const jobData = jobRes.data;

      // 3) Match
      const matchRes = await getJSON(`/api/match?candidate_id=${encodeURIComponent(candData.candidate_id)}&job_id=${encodeURIComponent(jobData.job_id)}`);
      const matchData = matchRes?.data || {};

      // Calculate percentage score
      let scoreValue = matchData.score ?? matchData.match_score ?? matchData.match ?? 0;
      if (scoreValue <= 1) scoreValue *= 100;
      scoreValue = Math.round(scoreValue);

      // Populate results
      document.getElementById('score').textContent = scoreValue;
      animateScore(scoreValue);

      document.getElementById('candidate-name').textContent = name || candData.name || 'Anonymous';
      document.getElementById('candidate-email').textContent = email || candData.email || 'Not provided';
      document.getElementById('job-title').textContent = title;

      const overlapSkills = matchData.overlap_skills || [];
      const missingSkills = matchData.missing_skills || [];
      const candidateSkills = candData.skills || [];
      const extraSkills = candidateSkills.filter(s => !overlapSkills.includes(s) && !missingSkills.includes(s));

      document.getElementById('skills-match').textContent = `${overlapSkills.length} / ${overlapSkills.length + missingSkills.length}`;
      document.getElementById('candidate-skills-count').textContent = candidateSkills.length;

      document.getElementById('overlap-count').textContent = overlapSkills.length;
      document.getElementById('missing-count').textContent = missingSkills.length;
      document.getElementById('extra-count').textContent = extraSkills.length;

      renderSkillTags(document.getElementById('overlap-skills'), overlapSkills, 'success');
      renderSkillTags(document.getElementById('missing-skills'), missingSkills, 'warning');
      renderSkillTags(document.getElementById('extra-skills'), extraSkills, 'info');
      renderSkillTags(document.getElementById('all-candidate-skills'), candidateSkills);

      const recommendation = getRecommendation(scoreValue);
      const recBox = document.getElementById('recommendation');
      recBox.className = 'recommendation-box ' + recommendation.class;
      document.getElementById('recommendation-text').textContent = recommendation.text;

      // Show results section
      resultsDiv.hidden = false;
      setTimeout(() => { resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }, 200);
    } catch (err) {
      alert(`Error: ${err?.message || err}`);
    } finally {
      btn.disabled = false;
      btnText.textContent = '🚀 Analyze Match';
    }
  });
});
