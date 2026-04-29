from __future__ import annotations


CHARTJS_CDN: str = (
    '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js">'
    "</script>"
)


APP_JS: str = """
<script>
let currentMode    = 'original';
let currentFeature = 'MedInc';
let charts         = {};


document.addEventListener('DOMContentLoaded', () => {
  initCharts();
  loadChartData();
  loadUserTable();
});


const TICK_STYLE = { color:'#4a6080', font:{ family:'DM Mono', size:10 } };
const GRID_STYLE = { color:'rgba(42,58,88,0.5)' };
const TOOLTIP_STYLE = {
  backgroundColor:'#141b2d', borderColor:'#2a3a58', borderWidth:1,
  titleColor:'#b8cce0', bodyColor:'#7a90b0', padding:10, cornerRadius:8,
};
const BASE_OPTS = {
  responsive:true, maintainAspectRatio:false,
  plugins:{ legend:{ display:false }, tooltip:TOOLTIP_STYLE },
  scales:{
    x:{ ticks:TICK_STYLE, grid:GRID_STYLE },
    y:{ ticks:TICK_STYLE, grid:GRID_STYLE },
  }
};


function initCharts() {
  charts.scatter = new Chart(document.getElementById('scatterChart'), {
    type: 'scatter',
    data: { datasets: [] },
    options: {
      ...BASE_OPTS,
      plugins: {
        ...BASE_OPTS.plugins,
        tooltip:{
          ...TOOLTIP_STYLE,
          callbacks:{ label: ctx => `(${ctx.parsed.x.toFixed(3)}, ${ctx.parsed.y.toFixed(3)})` }
        }
      },
    }
  });

  charts.bar = new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: { labels:[], datasets:[] },
    options: {
      ...BASE_OPTS,
      scales:{
        x:{ ticks:{ ...TICK_STYLE, maxRotation:45, font:{size:9} }, grid:GRID_STYLE },
        y:{ ticks:TICK_STYLE, grid:GRID_STYLE },
      }
    }
  });

  charts.pie = new Chart(document.getElementById('pieChart'), {
    type: 'doughnut',
    data: { labels:[], datasets:[] },
    options: {
      responsive:true, maintainAspectRatio:false, cutout:'60%',
      plugins:{
        legend:{
          display:true, position:'bottom',
          labels:{ color:'#7a90b0', font:{ family:'DM Mono', size:10 }, padding:12, boxWidth:10 }
        },
        tooltip:TOOLTIP_STYLE,
      }
    }
  });
}

async function loadChartData() {
  try {
    const res  = await fetch(`/api/chart-data?mode=${currentMode}&feature=${currentFeature}`);
    if (!res.ok) {
      const err = await res.json();
      return showToast(err.detail || 'Failed to load data', 'error');
    }
    const data = await res.json();
    renderScatter(data.scatter);
    renderBar(data.bar, data.feature_label);
    renderPie(data.pie);
    renderMetrics(data);
    renderStats(data.stats, data.feature_label);
  } catch (e) {
    showToast('Network error — is the server running?', 'error');
    console.error(e);
  }
}

function renderScatter(s) {
  const userSet = new Set(s.user_indices);
  const orig = [], user = [];
  s.x_values.forEach((x, i) => {
    const pt = { x: +x.toFixed(4), y: +s.y_values[i].toFixed(4) };
    (userSet.has(i) ? user : orig).push(pt);
  });

  const linePts = (s.x_line && s.x_line.length === 2)
    ? [{ x:s.x_line[0], y:s.y_line[0] }, { x:s.x_line[1], y:s.y_line[1] }]
    : [];

  charts.scatter.data.datasets = [
    { label:'Original',  data:orig, backgroundColor:'rgba(0,212,255,0.45)',
      pointRadius:3, pointHoverRadius:5 },
    { label:'User Added', data:user, backgroundColor:'#7fff6e',
      pointRadius:7, pointHoverRadius:9, pointStyle:'rectRot' },
    { label:'Regression', type:'line', data:linePts,
      borderColor:'#ffc947', borderWidth:2.5, pointRadius:0, tension:0, fill:false },
  ];

  const xLabel = document.getElementById('feature-select')?.selectedOptions[0]?.text || '';
  charts.scatter.options.scales.x.title = { display:true, text:xLabel,         color:'#4a6080', font:{ family:'DM Mono', size:10 } };
  charts.scatter.options.scales.y.title = { display:true, text:'Med. House Val ($100k)', color:'#4a6080', font:{ family:'DM Mono', size:10 } };
  charts.scatter.update('active');

  el('reg-coef').textContent = s.coefficient.toFixed(5);
  el('reg-int' ).textContent = s.intercept.toFixed(5);
  el('reg-r2'  ).textContent = s.r2_score.toFixed(5);
  el('reg-mse' ).textContent = s.mse.toFixed(5);
}

function renderBar(bar, featureLabel) {
  charts.bar.data.labels   = bar.labels;
  charts.bar.data.datasets = [{
    data: bar.counts,
    backgroundColor: bar.counts.map((_,i) =>
      `rgba(0,212,255,${(0.18 + i / bar.counts.length * 0.55).toFixed(2)})`),
    borderColor:'rgba(0,212,255,0.55)', borderWidth:1, borderRadius:4,
  }];
  const t = document.getElementById('bar-title');
  if (t) t.textContent = featureLabel + ' Distribution';
  charts.bar.update('active');
}

function renderPie(pie) {
  charts.pie.data.labels   = pie.labels;
  charts.pie.data.datasets = [{
    data: pie.values,
    backgroundColor:['rgba(0,212,255,0.70)','rgba(255,201,71,0.70)','rgba(255,85,114,0.70)'],
    borderColor:    ['#00d4ff','#ffc947','#ff5572'],
    borderWidth:1.5, hoverOffset:8,
  }];
  charts.pie.update('active');
}

function renderMetrics(data) {
  animCount('m-total',  data.n_total_points);
  animCount('m-user',   data.n_user_points);
  el('m-r2' ).textContent = data.scatter.r2_score.toFixed(4);
  el('m-mse').textContent = data.scatter.mse.toFixed(4);
}

function animCount(id, target) {
  const node  = el(id);
  if (!node) return;
  const start = parseInt(node.textContent.replace(/,/g,'')) || 0;
  const dur   = 500;
  const t0    = performance.now();
  const step  = ts => {
    const p = Math.min((ts - t0) / dur, 1);
    node.textContent = Math.round(start + (target - start) * p).toLocaleString();
    if (p < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

function renderStats(stats, featureLabel) {
  const panel = el('stats-panel');
  if (!panel || !stats) return;

  panel.innerHTML = Object.entries(stats).map(([key, s]) => `
    <div class="stat-mini">
      <p class="label" style="margin-bottom:6px;">${key}</p>
      <div class="stat-grid">
        ${[['μ',s.mean],['σ',s.std],['↓',s.min],['↑',s.max]].map(([l,v]) => `
          <div><div class="stat-lbl">${l}</div><div class="stat-val">${v}</div></div>
        `).join('')}
      </div>
    </div>
  `).join('');
}

async function loadUserTable() {
  try {
    const rows   = await (await fetch('/api/user-data')).json();
    const tbody  = el('user-tbody');
    if (!tbody) return;

    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:#4a6080;padding:16px;">No submissions yet</td></tr>';
      return;
    }

    tbody.innerHTML = rows.map((r, i) => {
      const d = new Date(r.created_at).toLocaleDateString('en-US',{month:'short',day:'numeric'});
      return `<tr class="fade-up">
        <td style="color:#00d4ff">${rows.length - i}</td>
        <td>${r.med_inc.toFixed(2)}</td>
        <td>${r.house_age.toFixed(0)}</td>
        <td style="color:#7fff6e">${r.med_house_val.toFixed(3)}</td>
        <td style="color:#4a6080">${d}</td>
      </tr>`;
    }).join('');
  } catch(e) { console.error('User table error', e); }
}

async function submitData(event) {
  event.preventDefault();
  const form = event.target;
  const btn  = el('submit-btn');

  btn.disabled     = true;
  btn.innerHTML    = '<span class="spinner"></span> Adding…';

  const payload = {};
  new FormData(form).forEach((v, k) => { payload[k] = parseFloat(v); });
  const STRING_FIELDS = new Set(['city', 'neighbourhood']);
  new FormData(form).forEach((v, k) => {
    payload[k] = STRING_FIELDS.has(k) ? v : parseFloat(v);
  });

  try {
    const res = await fetch('/api/submit', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json();
      const msg = Array.isArray(err.detail)
        ? err.detail.map(e => e.msg).join(', ')
        : (err.detail || 'Validation error');
      showToast(msg, 'error');
    } else {
      showToast('Point added — charts refreshed!', 'success');
      form.reset();
      await Promise.all([loadChartData(), loadUserTable()]);
    }
  } catch(e) {
    showToast('Network error during submission', 'error');
  } finally {
    btn.disabled  = false;
    btn.innerHTML = 'Add Data Point';
  }
}

async function resetData() {
  if (!confirm('Delete ALL your submitted data points?')) return;
  try {
    const body = await (await fetch('/api/user-data/reset',{method:'DELETE'})).json();
    showToast(`Reset complete — ${body.deleted} record(s) removed.`, 'info');
    await Promise.all([loadChartData(), loadUserTable()]);
  } catch(e) { showToast('Reset failed', 'error'); }
}

function setMode(mode) {
  currentMode = mode;
  document.querySelectorAll('.tab').forEach(b => {
    b.classList.toggle('active', b.dataset.mode === mode);
  });
  loadChartData();
}

function onFeatureChange() {
  currentFeature = el('feature-select').value;
  loadChartData();
}

function exportCSV() {
  window.location.href = `/api/export?mode=${currentMode}`;
}

function fillSample() {
  const SAMPLES = [
    {med_inc:3.87,house_age:41,ave_rooms:6.98,ave_bedrms:1.02,population:322, ave_occup:2.56,latitude:37.88,longitude:-122.23,med_house_val:4.526},
    {med_inc:2.10,house_age:21,ave_rooms:4.20,ave_bedrms:1.02,population:1851,ave_occup:2.81,latitude:34.26,longitude:-118.46,med_house_val:1.679},
    {med_inc:5.64,house_age:15,ave_rooms:7.01,ave_bedrms:0.98,population:980, ave_occup:2.95,latitude:37.45,longitude:-122.10,med_house_val:3.250},
    {med_inc:1.50,house_age:30,ave_rooms:3.80,ave_bedrms:1.05,population:600, ave_occup:3.10,latitude:33.80,longitude:-117.90,med_house_val:1.200},
    {med_inc:6.90,house_age:8, ave_rooms:8.20,ave_bedrms:1.00,population:420, ave_occup:2.40,latitude:38.10,longitude:-122.50,med_house_val:4.800},
  ];
  const s    = SAMPLES[Math.floor(Math.random() * SAMPLES.length)];
  const form = document.getElementById('data-form');
  Object.entries(s).forEach(([k,v]) => {
    const inp = form.querySelector(`[name="${k}"]`);
    if (inp) inp.value = v;
  });
}

let _toastTimer;
function showToast(msg, type='info') {
  const node = el('toast');
  node.textContent = msg;
  node.className   = `show t-${type}`;
  clearTimeout(_toastTimer);
  _toastTimer = setTimeout(() => { node.className = `t-${type}`; }, 3400);
}

const el = id => document.getElementById(id);
</script>
"""


def body_scripts() -> str:
    return CHARTJS_CDN + "\n" + APP_JS