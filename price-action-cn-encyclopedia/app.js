const data = window.CN_PATTERN_DATA || { patterns: [] };

const state = {
  query: "",
  family: "all",
  sort: "score",
  activeId: data.patterns[0]?.id || null
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

function html(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;"
  })[char]);
}

function searchText(value) {
  if (Array.isArray(value)) return value.map(searchText).join(" ");
  if (value && typeof value === "object") return Object.values(value).map(searchText).join(" ");
  return String(value || "");
}

function formatNumber(value) {
  return new Intl.NumberFormat("zh-CN").format(value || 0);
}

function init() {
  $("#patternCount").textContent = `${formatNumber(data.patternCount || data.patterns.length)} 形态`;
  $("#searchInput").addEventListener("input", (event) => {
    state.query = event.target.value.trim().toLowerCase();
    render();
  });
  $("#sortSelect").addEventListener("change", (event) => {
    state.sort = event.target.value;
    render();
  });
  $("#resetBtn").addEventListener("click", () => {
    state.query = "";
    state.family = "all";
    state.sort = "score";
    $("#searchInput").value = "";
    $("#sortSelect").value = "score";
    render();
  });
  $("#modalClose").addEventListener("click", closeModal);
  $("#imageModal").addEventListener("click", (event) => {
    if (event.target.id === "imageModal") closeModal();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeModal();
  });
  renderFamilyFilters();
  render();
}

function renderFamilyFilters() {
  const families = ["all", ...unique(data.patterns.map((pattern) => pattern.family))];
  $("#familyFilters").innerHTML = families.map((family) => `
    <button type="button" class="${family === state.family ? "active" : ""}" data-family="${html(family)}">
      ${family === "all" ? "全部" : html(family)}
    </button>
  `).join("");
  $$("#familyFilters button").forEach((button) => {
    button.addEventListener("click", () => {
      state.family = button.dataset.family;
      render();
    });
  });
}

function filteredPatterns() {
  const query = state.query;
  const rows = data.patterns.filter((pattern) => {
    if (state.family !== "all" && pattern.family !== state.family) return false;
    if (!query) return true;
    return searchText(pattern).toLowerCase().includes(query);
  });
  rows.sort((a, b) => {
    if (state.sort === "probability") return b.probScore - a.probScore || b.importance - a.importance;
    if (state.sort === "importance") return b.importance - a.importance || b.probScore - a.probScore;
    if (state.sort === "family") return a.family.localeCompare(b.family, "zh-CN") || b.importance - a.importance;
    return (b.probScore + b.importance) - (a.probScore + a.importance);
  });
  return rows;
}

function render() {
  renderFamilyFilters();
  const rows = filteredPatterns();
  if (!rows.some((pattern) => pattern.id === state.activeId)) {
    state.activeId = rows[0]?.id || data.patterns[0]?.id || null;
  }
  $("#visibleCount").textContent = `${formatNumber(rows.length)} 个`;
  $("#patternList").innerHTML = rows.length ? rows.map((pattern, index) => renderPatternRow(pattern, index)).join("") : `
    <div class="empty-state">没有匹配结果，换一个关键词。</div>
  `;
  $$(".pattern-row").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeId = button.dataset.id;
      renderDetail();
      $$(".pattern-row").forEach((row) => row.classList.toggle("active", row.dataset.id === state.activeId));
    });
  });
  renderDetail();
}

function renderPatternRow(pattern, index) {
  return `
    <button class="pattern-row ${pattern.id === state.activeId ? "active" : ""}" type="button" data-id="${html(pattern.id)}">
      <span class="rank">${String(index + 1).padStart(2, "0")}</span>
      <span class="row-title">
        <strong>${html(pattern.title)}</strong>
        <em>${html(pattern.family)} · ${html(pattern.winRate)}</em>
      </span>
      <span class="row-score">
        ${pattern.probScore}
        <small>${pattern.importance}</small>
      </span>
    </button>
  `;
}

function renderDetail() {
  const pattern = data.patterns.find((item) => item.id === state.activeId);
  if (!pattern) {
    $("#detail").innerHTML = `<div class="empty-state">请选择一个形态。</div>`;
    return;
  }
  $("#detail").innerHTML = `
    <article class="detail-card">
      <section class="detail-hero">
        <div>
          <p class="eyebrow">Pattern Terminal</p>
          <h1>${html(pattern.title)}</h1>
          <p class="hero-summary">${html(pattern.summary)}</p>
          <p class="source-line">${html(pattern.source)}</p>
          <div class="chip-row">
            <span>${html(pattern.family)}</span>
            <span>胜率 ${html(pattern.winRate)}</span>
            <span>胜率分 ${pattern.probScore}</span>
            <span>重要性 ${pattern.importance}</span>
            <span>难度 ${"●".repeat(pattern.difficulty)}</span>
            ${(pattern.aliases || []).map((alias) => `<span>${html(alias)}</span>`).join("")}
          </div>
        </div>
        <div class="stat-grid">
          <div><span>中文图源</span><strong>${formatNumber(pattern.charts?.length || 0)}</strong></div>
          <div><span>字幕课</span><strong>${formatNumber(pattern.video?.relatedCount || 0)}</strong></div>
          <div><span>家族</span><strong>${html(pattern.family)}</strong></div>
          <div><span>目标</span><strong>${html(first(pattern.target))}</strong></div>
        </div>
      </section>
    </article>

    ${renderVideo(pattern)}
    ${renderCharts(pattern)}
    ${renderCourses(pattern)}
  `;
  bindChartModals();
}

function renderVideo(pattern) {
  const video = pattern.video || {};
  const checklist = video.checklist || [];
  return `
    <section class="video-card">
      <div>
        <p class="eyebrow">Brooks Signal Notes</p>
        <h2>字幕课综合讲解</h2>
        <p>${html(video.synthesis || video.thesis || "暂无字幕总结。")}</p>
      </div>
      <div class="learning-grid">
        ${checklist.map((item) => `
          <section>
            <span>${html(item.label)}</span>
            <p>${html(item.value)}</p>
          </section>
        `).join("")}
      </div>
    </section>
  `;
}

function renderCharts(pattern) {
  const charts = pattern.charts || [];
  return `
    <section class="chart-section">
      <div class="section-head">
        <div>
          <p class="eyebrow">Chart Evidence</p>
          <h2>中文课件图解</h2>
        </div>
        <p>${formatNumber(charts.length)} 张，来自本地中文 PDF</p>
      </div>
      <div class="chart-grid">
        ${charts.length ? charts.map((chart, index) => renderChart(pattern, chart, index)).join("") : `
          <div class="empty-state">没有匹配到中文课件图。</div>
        `}
      </div>
    </section>
  `;
}

function renderChart(pattern, chart, index) {
  const caption = `${chart.source} · p.${chart.page} · ${pattern.title}`;
  return `
    <article class="chart-card">
      <button type="button" class="chart-open" data-src="${html(chart.src)}" data-caption="${html(caption)}">
        <img src="${html(chart.src)}" alt="${html(caption)}" loading="${index > 1 ? "lazy" : "eager"}" />
      </button>
      <div class="chart-body">
        <div class="chart-meta">
          <span>样本 ${index + 1} · 匹配分 ${chart.score}</span>
          <span>${html(chart.source)} · p.${chart.page}</span>
        </div>
        <p class="chart-note">${html(chart.note)}</p>
      </div>
    </article>
  `;
}

function renderCourses(pattern) {
  const lessons = pattern.video?.lessons || [];
  return `
    <section class="video-card">
      <div>
        <p class="eyebrow">Course Trace</p>
        <h2>相关字幕课</h2>
      </div>
      <div class="course-list">
        ${lessons.slice(0, 6).map((lesson) => `
          <article>
            <span>${html(lesson.module)} · ${html(lesson.language)} · ${formatNumber(lesson.cueCount)} 条字幕</span>
            <strong>${html(lesson.title)}</strong>
            <p>${html(lesson.brief || lesson.summary)}</p>
          </article>
        `).join("")}
      </div>
    </section>
  `;
}

function bindChartModals() {
  $$(".chart-open").forEach((button) => {
    button.addEventListener("click", () => {
      $("#modalImage").src = button.dataset.src;
      $("#modalImage").alt = button.dataset.caption;
      $("#modalCaption").textContent = button.dataset.caption;
      $("#imageModal").classList.add("open");
      $("#imageModal").setAttribute("aria-hidden", "false");
    });
  });
}

function closeModal() {
  $("#imageModal").classList.remove("open");
  $("#imageModal").setAttribute("aria-hidden", "true");
  $("#modalImage").src = "";
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function first(value) {
  return Array.isArray(value) ? value[0] : value || "";
}

init();
