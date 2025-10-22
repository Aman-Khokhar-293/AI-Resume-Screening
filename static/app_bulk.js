window.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('recruiter-form');
  const btn = document.getElementById('btn-run');
  const btnText = document.getElementById('btn-text');
  const filesInput = document.getElementById('resume-files');
  const fileCount = document.getElementById('file-count');
  const fileList = document.getElementById('file-list');
  const progressBar = document.getElementById('progress-bar');
  const progressFill = document.getElementById('progress-fill');
  const progressText = document.getElementById('progress-text');
  const resultsDiv = document.getElementById('results');
  
  // Store candidates data globally within this closure
  let currentCandidates = [];

  // File selection handler
  filesInput.addEventListener('change', (e) => {
    const files = e.target.files;
    const count = files.length;
    
    if (count > 100) {
      alert('Maximum 100 files allowed');
      filesInput.value = '';
      fileCount.textContent = '0 files';
      fileList.innerHTML = '';
      return;
    }
    
    fileCount.textContent = `${count} file${count !== 1 ? 's' : ''}`;
    
    // Display file list
    if (count > 0 && count <= 10) {
      fileList.innerHTML = '<div class="file-list-items">' +
        Array.from(files).map((f, i) => 
          `<div class="file-item">📄 ${f.name}</div>`
        ).join('') +
        '</div>';
    } else if (count > 10) {
      fileList.innerHTML = `<div class="file-list-summary">${count} files selected (too many to list)</div>`;
    } else {
      fileList.innerHTML = '';
    }
  });

  // Form submission
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const files = filesInput.files;
    if (!files || files.length === 0) {
      alert('Please select at least one resume file');
      return;
    }

    if (files.length > 100) {
      alert('Maximum 100 files allowed');
      return;
    }

    const formData = new FormData(form);
    
    // Show progress bar
    btn.disabled = true;
    btnText.textContent = '⏳ Processing...';
    progressBar.style.display = 'block';
    resultsDiv.style.display = 'none';
    
    try {
      const response = await fetch('/api/bulk-match', {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();
      
      console.log('Received data from backend:', data);
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to process resumes');
      }
      
      if (!data.candidates || data.candidates.length === 0) {
        alert('No candidates were successfully processed. Please check the resume files.');
        progressBar.style.display = 'none';
        return;
      }
      
      // Hide progress, show results
      progressBar.style.display = 'none';
      renderRankingBoard(data);
      resultsDiv.style.display = 'block';
      
      // Scroll to results
      setTimeout(() => {
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
      
    } catch (error) {
      alert(`Error: ${error.message}`);
      progressBar.style.display = 'none';
    } finally {
      btn.disabled = false;
      btnText.textContent = '🚀 Rank All Candidates';
    }
  });

  function renderRankingBoard(data) {
    const candidates = data.candidates || [];
    const jobTitle = data.job_title || '--';
    
    // Store candidates for modal access
    currentCandidates = candidates;
    
    // Update header
    document.getElementById('job-title-ranking').textContent = jobTitle;
    document.getElementById('total-candidates').textContent = candidates.length;
    
    if (candidates.length > 0) {
      const scores = candidates.map(c => c.score * 100);
      const avgScore = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
      const topScore = Math.round(Math.max(...scores));
      
      document.getElementById('avg-score').textContent = `${avgScore}%`;
      document.getElementById('top-score').textContent = `${topScore}%`;
    } else {
      document.getElementById('avg-score').textContent = '0%';
      document.getElementById('top-score').textContent = '0%';
    }
    
    // Render table
    const tbody = document.getElementById('ranking-tbody');
    tbody.innerHTML = '';
    
    candidates.forEach((candidate, index) => {
      const row = document.createElement('tr');
      const score = Math.round(candidate.score * 100);
      const rank = index + 1;
      
      // Medal for top 3
      let rankDisplay = `#${rank}`;
      if (rank === 1) rankDisplay = '🥇';
      else if (rank === 2) rankDisplay = '🥈';
      else if (rank === 3) rankDisplay = '🥉';
      
      // Score color
      let scoreClass = 'score-low';
      if (score >= 80) scoreClass = 'score-excellent';
      else if (score >= 60) scoreClass = 'score-good';
      else if (score >= 40) scoreClass = 'score-moderate';
      
      row.innerHTML = `
        <td class="rank-cell">${rankDisplay}</td>
        <td class="name-cell">
          <div class="candidate-name">${candidate.name}</div>
          <div class="candidate-filename">${candidate.filename}</div>
        </td>
        <td class="contact-cell">${candidate.contact}</td>
        <td class="score-cell">
          <div class="score-badge ${scoreClass}">${score}%</div>
        </td>
        <td class="skills-cell">
          ${candidate.overlap_skills.length}/${candidate.overlap_skills.length + candidate.missing_skills.length}
        </td>
        <td class="action-cell">
          <button class="btn-details" data-index="${index}">View</button>
        </td>
      `;
      
      tbody.appendChild(row);
    });
    
    // Add click handlers for details buttons
    document.querySelectorAll('.btn-details').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const index = parseInt(e.target.dataset.index);
        showCandidateDetails(currentCandidates[index]);
      });
    });
  }

  function showCandidateDetails(candidate) {
    if (!candidate) {
      console.error('No candidate data provided');
      return;
    }
    
    console.log('Showing candidate details:', candidate);
    
    const modal = document.getElementById('candidate-modal');
    const score = Math.round((candidate.score || 0) * 100);
    
    // Safely set values with fallbacks
    document.getElementById('modal-candidate-name').textContent = candidate.name || 'Unknown';
    document.getElementById('modal-score').textContent = `${score}%`;
    document.getElementById('modal-contact').textContent = candidate.contact || 'Not provided';
    
    // Matching skills
    const overlapSkills = candidate.overlap_skills || [];
    document.getElementById('modal-match-count').textContent = overlapSkills.length;
    renderSkills('modal-match-skills', overlapSkills, 'success');
    
    // Missing skills
    const missingSkills = candidate.missing_skills || [];
    document.getElementById('modal-missing-count').textContent = missingSkills.length;
    renderSkills('modal-missing-skills', missingSkills, 'warning');
    
    // All skills
    const allSkills = candidate.all_skills || [];
    document.getElementById('modal-all-count').textContent = allSkills.length;
    renderSkills('modal-all-skills', allSkills);
    
    modal.style.display = 'flex';
  }

  function renderSkills(containerId, skills, colorClass = '') {
    const container = document.getElementById(containerId);
    if (!skills || skills.length === 0) {
      container.innerHTML = '<span class="empty-state">None</span>';
      return;
    }
    container.innerHTML = skills.map(s => 
      `<span class="skill-tag ${colorClass}">${s}</span>`
    ).join('');
  }

  // Modal close
  document.getElementById('modal-close').addEventListener('click', () => {
    document.getElementById('candidate-modal').style.display = 'none';
  });
  
  // Close modal on background click
  document.getElementById('candidate-modal').addEventListener('click', (e) => {
    if (e.target.id === 'candidate-modal') {
      document.getElementById('candidate-modal').style.display = 'none';
    }
  });
});
