/**
 * Frontend application logic for Banking Customer Churn Analytics Platform.
 */

let geoChart = null;
let ageChart = null;
let productChart = null;
let importanceChart = null;

// Tab Switching
function switchTab(tabId) {
  ['overview', 'predictor', 'sql', 'models'].forEach(id => {
    const el = document.getElementById(`tab-${id}`);
    const btn = document.getElementById(`tab-btn-${id}`);
    if (id === tabId) {
      el.classList.remove('hidden');
      btn.className = 'py-3 px-1 text-sm tab-active transition';
    } else {
      el.classList.add('hidden');
      btn.className = 'py-3 px-1 text-sm text-slate-500 hover:text-slate-700 transition';
    }
  });

  if (tabId === 'models' && !importanceChart) {
    loadModelMetrics();
  }
}

// Preset archetypes
function applyPreset(preset) {
  if (preset === 'german_high') {
    document.getElementById('inp-credit').value = 620;
    document.getElementById('inp-geo').value = 'Germany';
    document.getElementById('inp-gender').value = 'Female';
    document.getElementById('inp-age').value = 52;
    document.getElementById('inp-tenure').value = 3;
    document.getElementById('inp-balance').value = 125000;
    document.getElementById('inp-products').value = '1';
    document.getElementById('inp-card').value = '1';
    document.getElementById('inp-active').value = '0';
    document.getElementById('inp-salary').value = 95000;
  } else if (preset === 'french_loyal') {
    document.getElementById('inp-credit').value = 740;
    document.getElementById('inp-geo').value = 'France';
    document.getElementById('inp-gender').value = 'Male';
    document.getElementById('inp-age').value = 28;
    document.getElementById('inp-tenure').value = 6;
    document.getElementById('inp-balance').value = 45000;
    document.getElementById('inp-products').value = '2';
    document.getElementById('inp-card').value = '1';
    document.getElementById('inp-active').value = '1';
    document.getElementById('inp-salary').value = 65000;
  }
  submitPrediction();
}

// Load Executive Analytics & Charts
async function loadDashboardData() {
  try {
    // 1. KPIs
    const kpiRes = await fetch('/api/v1/analytics/kpis');
    const kpiData = await kpiRes.json();
    const kpis = kpiData.kpis;

    document.getElementById('kpi-total-cust').textContent = Number(kpis.total_customers).toLocaleString();
    document.getElementById('kpi-churn-rate').textContent = `${kpis.churn_rate_pct}%`;
    document.getElementById('kpi-churned-count').textContent = Number(kpis.churned_customers).toLocaleString();
    document.getElementById('kpi-retained-rate').textContent = `${kpis.retention_rate_pct}%`;
    document.getElementById('kpi-retained-count').textContent = Number(kpis.retained_customers).toLocaleString();
    document.getElementById('kpi-active-rate').textContent = `${kpis.active_member_pct}%`;
    document.getElementById('kpi-active-count').textContent = Number(kpis.active_members).toLocaleString();

    // 2. Geography Chart
    const geoRes = await fetch('/api/v1/analytics/geography');
    const geoJson = await geoRes.json();
    const geoLabels = geoJson.data.map(d => d.Geography);
    const geoChurns = geoJson.data.map(d => d.churn_rate_pct);

    const ctxGeo = document.getElementById('geoChart').getContext('2d');
    if (geoChart) geoChart.destroy();
    geoChart = new Chart(ctxGeo, {
      type: 'bar',
      data: {
        labels: geoLabels,
        datasets: [{
          label: 'Churn Rate (%)',
          data: geoChurns,
          backgroundColor: ['#ef4444', '#3b82f6', '#10b981'],
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, max: 40, ticks: { callback: v => `${v}%` } } }
      }
    });

    // 3. Age Group Chart
    const demoRes = await fetch('/api/v1/analytics/demographics');
    const demoJson = await demoRes.json();
    const ageLabels = demoJson.by_age_group.map(d => d.AgeGroup);
    const ageChurns = demoJson.by_age_group.map(d => d.churn_rate_pct);

    const ctxAge = document.getElementById('ageChart').getContext('2d');
    if (ageChart) ageChart.destroy();
    ageChart = new Chart(ctxAge, {
      type: 'line',
      data: {
        labels: ageLabels,
        datasets: [{
          label: 'Churn Rate (%)',
          data: ageChurns,
          borderColor: '#f97316',
          backgroundColor: 'rgba(249, 115, 22, 0.1)',
          fill: true,
          tension: 0.3,
          pointRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, max: 65, ticks: { callback: v => `${v}%` } } }
      }
    });

    // 4. Products Chart
    const prodRes = await fetch('/api/v1/analytics/products');
    const prodJson = await prodRes.json();
    const prodLabels = prodJson.data.map(d => `${d.NumOfProducts} Product${d.NumOfProducts > 1 ? 's' : ''}`);
    const prodChurns = prodJson.data.map(d => d.churn_rate_pct);

    const ctxProd = document.getElementById('productChart').getContext('2d');
    if (productChart) productChart.destroy();
    productChart = new Chart(ctxProd, {
      type: 'bar',
      data: {
        labels: prodLabels,
        datasets: [{
          label: 'Churn Rate (%)',
          data: prodChurns,
          backgroundColor: ['#3b82f6', '#10b981', '#ef4444', '#b91c1c'],
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, max: 100, ticks: { callback: v => `${v}%` } } }
      }
    });
  } catch (err) {
    console.error('Failed loading analytics data:', err);
  }
}

// Real-time Prediction
async function submitPrediction() {
  const payload = {
    CreditScore: parseInt(document.getElementById('inp-credit').value),
    Geography: document.getElementById('inp-geo').value,
    Gender: document.getElementById('inp-gender').value,
    Age: parseInt(document.getElementById('inp-age').value),
    Tenure: parseInt(document.getElementById('inp-tenure').value),
    Balance: parseFloat(document.getElementById('inp-balance').value),
    NumOfProducts: parseInt(document.getElementById('inp-products').value),
    HasCrCard: parseInt(document.getElementById('inp-card').value),
    IsActiveMember: parseInt(document.getElementById('inp-active').value),
    EstimatedSalary: parseFloat(document.getElementById('inp-salary').value)
  };

  const btnText = document.getElementById('pred-btn-text');
  btnText.textContent = 'Computing Risk Score...';

  try {
    const res = await fetch('/api/v1/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      alert(`Validation error: ${JSON.stringify(err.detail)}`);
      return;
    }

    const data = await res.json();

    // Display probability
    const probPctEl = document.getElementById('res-prob-pct');
    probPctEl.textContent = `${data.churn_probability_pct}%`;

    // Display tier badge
    const tierEl = document.getElementById('res-risk-tier');
    tierEl.textContent = `${data.risk_tier.toUpperCase()} RISK`;
    if (data.risk_tier === 'High') {
      tierEl.className = 'px-3 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-200';
      probPctEl.className = 'text-4xl font-extrabold text-rose-600 mt-1';
    } else if (data.risk_tier === 'Medium') {
      tierEl.className = 'px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800 border border-amber-200';
      probPctEl.className = 'text-4xl font-extrabold text-amber-600 mt-1';
    } else {
      tierEl.className = 'px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200';
      probPctEl.className = 'text-4xl font-extrabold text-emerald-600 mt-1';
    }

    // Display risk factors
    const factorsList = document.getElementById('res-risk-factors');
    factorsList.innerHTML = '';
    if (data.primary_risk_factors.length === 0) {
      factorsList.innerHTML = '<li class="text-slate-400 list-none">No critical high-risk indicators detected.</li>';
    } else {
      data.primary_risk_factors.forEach(f => {
        const li = document.createElement('li');
        li.textContent = f;
        factorsList.appendChild(li);
      });
    }

    // Display retention strategy
    document.getElementById('res-strategy-title').textContent = data.retention_strategy.intervention_type;
    const stepsList = document.getElementById('res-strategy-steps');
    stepsList.innerHTML = '';
    data.retention_strategy.actionable_steps.forEach(step => {
      const li = document.createElement('li');
      li.textContent = step;
      stepsList.appendChild(li);
    });

    document.getElementById('res-threshold').textContent = data.decision_threshold;
  } catch (err) {
    console.error('Prediction failed:', err);
  } finally {
    btnText.textContent = 'Score Customer Churn Risk';
  }
}

// SQL Query Runner
async function runSelectedSql() {
  const queryKey = document.getElementById('sql-query-select').value;
  try {
    const res = await fetch('/api/v1/analytics/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ named_query: queryKey })
    });
    const data = await res.json();

    document.getElementById('sql-row-count').textContent = data.row_count;
    document.getElementById('sql-bench').textContent = `Latency: ${data.execution_time_ms} ms`;

    // Render columns
    const thead = document.getElementById('sql-thead');
    thead.innerHTML = `<tr>${data.columns.map(c => `<th class="px-4 py-2.5 font-semibold">${c}</th>`).join('')}</tr>`;

    // Render rows
    const tbody = document.getElementById('sql-tbody');
    tbody.innerHTML = data.rows.map(row => {
      return `<tr>${data.columns.map(c => `<td class="px-4 py-2 text-slate-700">${row[c] !== null ? row[c] : ''}</td>`).join('')}</tr>`;
    }).join('');
  } catch (err) {
    console.error('SQL execution failed:', err);
  }
}

// Load Model Benchmarks & Metrics
async function loadModelMetrics() {
  try {
    const res = await fetch('/api/v1/predict/metrics');
    const data = await res.json();

    const tbody = document.getElementById('benchmarks-tbody');
    tbody.innerHTML = '';

    const models = data.benchmark_comparison;
    for (const [name, metrics] of Object.entries(models)) {
      const opt = metrics.test_optimal_threshold;
      const isChamp = (name === data.champion_model);
      const row = `
        <tr class="${isChamp ? 'bg-blue-50/50 font-medium' : ''}">
          <td class="px-4 py-3 text-slate-900">${name.replace('_', ' ')}</td>
          <td class="px-4 py-3">${metrics.cv_roc_auc_mean}</td>
          <td class="px-4 py-3">${opt.roc_auc}</td>
          <td class="px-4 py-3">${opt.pr_auc}</td>
          <td class="px-4 py-3">${opt.precision}</td>
          <td class="px-4 py-3">${opt.recall}</td>
          <td class="px-4 py-3 font-semibold text-blue-700">${opt.f1}</td>
          <td class="px-4 py-3">${opt.brier_score}</td>
          <td class="px-4 py-3">
            ${isChamp ? '<span class="bg-blue-100 text-blue-800 text-[10px] px-2 py-0.5 rounded font-bold">CHAMPION</span>' : '<span class="text-slate-400 text-[10px]">Candidate</span>'}
          </td>
        </tr>
      `;
      tbody.innerHTML += row;
    }

    // Feature Importances Chart
    const importances = data.feature_importances;
    const labels = Object.keys(importances).slice(0, 10);
    const values = Object.values(importances).slice(0, 10).map(v => (v * 100).toFixed(1));

    const ctxImp = document.getElementById('importanceChart').getContext('2d');
    if (importanceChart) importanceChart.destroy();
    importanceChart = new Chart(ctxImp, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Relative Importance (%)',
          data: values,
          backgroundColor: '#3b82f6',
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { x: { beginAtZero: true, ticks: { callback: v => `${v}%` } } }
      }
    });
  } catch (err) {
    console.error('Failed loading metrics:', err);
  }
}

// Initial page load
window.addEventListener('DOMContentLoaded', () => {
  loadDashboardData();
  runSelectedSql();
});
