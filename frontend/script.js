const isLocalFrontend = ['localhost', '127.0.0.1'].includes(window.location.hostname)
  && window.location.port === '8001';
const API_BASE_URL = isLocalFrontend ? 'http://localhost:8000' : '';
const SESSION_KEY = 'skillmatch-demo-email';
const sessionEmail = sessionStorage.getItem(SESSION_KEY);
const form = document.getElementById('career-form');
const submitButton = document.getElementById('submit-btn');
const formMessage = document.getElementById('form-message');
const resultContent = document.getElementById('result-content');

document.getElementById('session-email').textContent = sessionEmail || '';
document.getElementById('logout-btn').addEventListener('click', () => {
  sessionStorage.removeItem(SESSION_KEY);
  window.location.assign('login.html');
});

const sliderFields = document.querySelectorAll('input[type="range"]');

sliderFields.forEach((slider) => {
  const valueNode = slider.parentElement.querySelector('.slider-value span');
  valueNode.textContent = slider.value;

  slider.addEventListener('input', () => {
    valueNode.textContent = slider.value;
  });
});

function setMessage(message, type = '') {
  formMessage.textContent = message;
  formMessage.className = 'form-message';
  if (type) {
    formMessage.classList.add(type);
  }
}

function getPayload() {
  return {
    interested_field: document.getElementById('interested_field').value,
    python_skill: Number(document.getElementById('python_skill').value),
    ml_skill: Number(document.getElementById('ml_skill').value),
    sql_skill: Number(document.getElementById('sql_skill').value),
    deep_learning_skill: Number(document.getElementById('deep_learning_skill').value),
    web_dev_skill: Number(document.getElementById('web_dev_skill').value),
    cybersecurity_skill: Number(document.getElementById('cybersecurity_skill').value),
    statistics_skill: Number(document.getElementById('statistics_skill').value),
    communication_skill: Number(document.getElementById('communication_skill').value),
    problem_solving_skill: Number(document.getElementById('problem_solving_skill').value),
    cgpa: Number(document.getElementById('cgpa').value),
    ai_interest: Number(document.getElementById('ai_interest').value),
    data_interest: Number(document.getElementById('data_interest').value),
  };
}

function renderSkillBadges(items, type) {
  if (!items || items.length === 0) {
    return '<span class="badge">None</span>';
  }

  return items
    .map((item) => `<span class="badge ${type}">${item}</span>`)
    .join('');
}

function renderResult(data) {
  const requiredSkills = data.required_skills || [];
  const strongSkills = data.strong_skills || [];
  const developingSkills = data.developing_skills || [];
  const missingSkills = data.missing_skills || [];
  const roadmap = data.roadmap || [];
  const certifications = data.certifications || [];
  const projects = data.projects || [];
  const companies = data.companies || [];
  const industries = data.industries || [];
  const nextSteps = data.next_steps || [];

  resultContent.className = 'result-content';
  resultContent.innerHTML = `
    <div class="result-card">
      <div class="career-header">
        <div>
          <span class="career-badge">Predicted role</span>
          <h3 class="career-name">${data.career}</h3>
        </div>
        <div class="match-pill">${data.match_score}% Match</div>
      </div>

      <div class="dashboard-grid">
        <div class="metric-card">
          <h4>Required skills</h4>
          <div class="skill-badges">
            ${renderSkillBadges(requiredSkills, 'developing')}
          </div>
        </div>

        <div class="metric-card">
          <h4>Model confidence</h4>
          <div class="skill-badges">
            <span class="badge strong">${data.model_confidence || data.match_score}% confidence</span>
          </div>
        </div>

        <div class="info-card">
          <h4>Strong Skills</h4>
          <div class="skill-badges">
            ${renderSkillBadges(strongSkills, 'strong')}
          </div>
        </div>

        <div class="info-card">
          <h4>Developing Skills</h4>
          <div class="skill-badges">
            ${renderSkillBadges(developingSkills, 'developing')}
          </div>
        </div>

        <div class="info-card" style="grid-column: 1 / -1;">
          <h4>Missing Skills</h4>
          <div class="skill-badges">
            ${renderSkillBadges(missingSkills, 'missing')}
          </div>
        </div>
      </div>

      <div class="roadmap-card">
        <h4>Personalized Roadmap</h4>
        <ol>
          ${roadmap.map((step, index) => `<li><strong>Step ${index + 1}:</strong> ${step}</li>`).join('')}
        </ol>
      </div>

      <div class="dashboard-grid">
        <div class="list-card">
          <h4>Certifications</h4>
          <ul>
            ${certifications.map((item) => `<li>${item}</li>`).join('')}
          </ul>
        </div>

        <div class="list-card">
          <h4>Projects</h4>
          <ul>
            ${projects.map((item) => `<li>${item}</li>`).join('')}
          </ul>
        </div>

        <div class="list-card">
          <h4>Companies</h4>
          <ul>
            ${companies.map((item) => `<li>${item}</li>`).join('')}
          </ul>
        </div>

        <div class="list-card">
          <h4>Industries</h4>
          <ul>
            ${industries.map((item) => `<li>${item}</li>`).join('')}
          </ul>
        </div>

        <div class="list-card" style="grid-column: 1 / -1;">
          <h4>Next Steps</h4>
          <ul>
            ${nextSteps.map((item) => `<li>${item}</li>`).join('')}
          </ul>
        </div>
      </div>
    </div>
  `;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = getPayload();
  submitButton.disabled = true;
  submitButton.textContent = 'Analyzing your profile...';
  setMessage('Analyzing your profile...', 'success');

  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Prediction failed. Please try again.');
    }

    renderResult(data);
    setMessage('Career profile analyzed successfully.', 'success');
  } catch (error) {
    setMessage(error.message || 'The API is currently unavailable. Please try again later.', 'error');
    resultContent.className = 'result-content';
    resultContent.innerHTML = `
      <div class="empty-card">
        <div class="empty-icon">!</div>
        <h3>Prediction unavailable</h3>
        <p>${error.message || 'An unexpected error occurred while connecting to the backend.'}</p>
      </div>
    `;
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = 'Analyze My Career';
  }
});
