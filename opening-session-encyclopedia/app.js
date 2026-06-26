const data = window.OPENING_ATLAS_DATA || { entries: [], stageOrder: [], timeline: [], courses: [], glossary: [] };

const state = {
  query: "",
  stage: "全部",
  activeId: data.entries[0]?.id || null
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

function searchBlob(value) {
  if (Array.isArray(value)) return value.map(searchBlob).join(" ");
  if (value && typeof value === "object") return Object.values(value).map(searchBlob).join(" ");
  return String(value || "");
}

function formatNumber(value) {
  return new Intl.NumberFormat("zh-CN").format(value || 0);
}

function init() {
  $("#entryCount").textContent = formatNumber(data.stats?.entries || data.entries.length);
  $("#chartCount").textContent = formatNumber(data.stats?.charts || 0);
  $("#courseCount").textContent = formatNumber(data.stats?.coreCourses || data.courses.length);
  $("#searchInput").addEventListener("input", (event) => {
    state.query = event.target.value.trim().toLowerCase();
    renderEntries();
  });
  $("#modalClose").addEventListener("click", closeModal);
  $("#imageModal").addEventListener("click", (event) => {
    if (event.target.id === "imageModal") closeModal();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeModal();
  });
  renderTimeline();
  renderStageFilters();
  renderEntries();
  renderCourses();
  renderGlossary();
}

function renderTimeline() {
  $("#timeline").innerHTML = data.timeline.map((item, index) => `
    <article class="timeline-item">
      <span>${String(index + 1).padStart(2, "0")}</span>
      <strong>${html(item.time)} · ${html(item.title)}</strong>
      <p>${html(item.body)}</p>
    </article>
  `).join("");
}

function renderStageFilters() {
  const stages = ["全部", ...(data.stageOrder || [])];
  $("#stageFilters").innerHTML = stages.map((stage) => `
    <button type="button" class="${stage === state.stage ? "active" : ""}" data-stage="${html(stage)}">
      ${html(stage)}
    </button>
  `).join("");
  $$("#stageFilters button").forEach((button) => {
    button.addEventListener("click", () => {
      state.stage = button.dataset.stage;
      renderStageFilters();
      renderEntries();
    });
  });
}

function filteredEntries() {
  const query = state.query;
  return data.entries.filter((entry) => {
    if (state.stage !== "全部" && entry.stage !== state.stage) return false;
    if (!query) return true;
    return searchBlob(entry).toLowerCase().includes(query);
  });
}

function renderEntries() {
  const rows = filteredEntries();
  if (!rows.some((entry) => entry.id === state.activeId)) {
    state.activeId = rows[0]?.id || data.entries[0]?.id || null;
  }
  $("#visibleCount").textContent = `${formatNumber(rows.length)} 个`;
  $("#entryList").innerHTML = rows.length ? rows.map(renderEntryButton).join("") : `
    <div class="empty-state">没有匹配结果，换一个关键词。</div>
  `;
  $$(".entry-button").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeId = button.dataset.id;
      renderDetail();
      $$(".entry-button").forEach((item) => item.classList.toggle("active", item.dataset.id === state.activeId));
    });
  });
  renderDetail();
}

function renderEntryButton(entry) {
  return `
    <button type="button" class="entry-button ${entry.id === state.activeId ? "active" : ""}" data-id="${html(entry.id)}">
      <span class="entry-rank">${String(entry.rank).padStart(2, "0")}</span>
      <span class="entry-title">
        <strong>${html(entry.title)}</strong>
        <em>${html(entry.stage)} · ${html(entry.winRate)}</em>
      </span>
      <span class="entry-score">${entry.importance}</span>
    </button>
  `;
}

function renderDetail() {
  const entry = data.entries.find((item) => item.id === state.activeId);
  if (!entry) {
    $("#detail").innerHTML = `<div class="empty-state">请选择一个早盘形态。</div>`;
    return;
  }
  $("#detail").innerHTML = `
    <article class="detail-hero">
      <div>
        <p class="eyebrow">${html(entry.stage)} · ${html(entry.lesson)}</p>
        <h2>${html(entry.title)}</h2>
        <p class="lead">${html(entry.thesis)}</p>
        <div class="chip-row">
          <span>胜率 ${html(entry.winRate)}</span>
          <span>重要性 ${entry.importance}</span>
          <span>难度 ${"●".repeat(entry.difficulty || 1)}</span>
          <span>${html(entry.source)}</span>
        </div>
      </div>
      <div class="decision-card">
        <span>Brooks 读法</span>
        <strong>位置 → 跟随 → 放弃条件</strong>
        <p>${html(entry.summary)}</p>
      </div>
    </article>

    <section class="study-grid">
      <article>
        <span>读图顺序</span>
        <ol>${entry.readOrder.map((item) => `<li>${html(item)}</li>`).join("")}</ol>
      </article>
      <article>
        <span>容易犯错</span>
        <ul>${entry.traps.map((item) => `<li>${html(item)}</li>`).join("")}</ul>
      </article>
      <article>
        <span>交易检查</span>
        <dl>${entry.checklist.map((item) => `<dt>${html(item.label)}</dt><dd>${html(item.value)}</dd>`).join("")}</dl>
      </article>
    </section>

    <section class="chart-section">
      <div class="subhead">
        <div>
          <p class="eyebrow">Chart Encyclopedia</p>
          <h3>中文课件图表</h3>
        </div>
        <p>${formatNumber(entry.charts.length)} 张样本</p>
      </div>
      <div class="chart-grid">
        ${entry.charts.map((chart, index) => renderChart(entry, chart, index)).join("")}
      </div>
    </section>

    <section class="lesson-section">
      <div class="subhead">
        <div>
          <p class="eyebrow">Related Lessons</p>
          <h3>相关 Brooks 课程</h3>
        </div>
      </div>
      <div class="lesson-list">
        ${entry.lessons.slice(0, 8).map((lesson) => `
          <article>
            <span>${html(lesson.module)} · ${html(lesson.language)} · ${formatNumber(lesson.cueCount)} 条字幕</span>
            <strong>${html(lesson.title)}</strong>
            <p>${html(lesson.brief)}</p>
          </article>
        `).join("")}
      </div>
    </section>
  `;
  bindChartButtons();
}

function renderChart(entry, chart, index) {
  const caption = `${entry.title} · ${chart.source} · p.${chart.page} · 样本 ${index + 1}`;
  return `
    <article class="chart-card">
      <button type="button" class="chart-open" data-src="${html(chart.src)}" data-caption="${html(caption)}">
        <img src="${html(chart.src)}" alt="${html(caption)}" loading="${index > 1 ? "lazy" : "eager"}" />
      </button>
      <div class="chart-body">
        <div class="chart-meta">
          <span>样本 ${index + 1}</span>
          <span>${html(chart.source)} · p.${chart.page}</span>
        </div>
        <p>${html(chart.note)}</p>
      </div>
    </article>
  `;
}

function renderCourses() {
  $("#courseGrid").innerHTML = data.courses.map((course) => `
    <article class="course-card">
      <span>${html(course.status)}</span>
      <strong>${html(course.id)} · ${html(course.title)}</strong>
      <p>${html(course.focus)}</p>
      <div class="bar" style="--value:${Math.max(10, Math.min(course.weight, 100))}%"></div>
    </article>
  `).join("");
}

function renderGlossary() {
  $("#glossary").innerHTML = data.glossary.map((item) => `
    <article>
      <span>${html(item.term)}</span>
      <strong>${html(item.cn)}</strong>
      <p>${html(item.body)}</p>
    </article>
  `).join("");
}

function bindChartButtons() {
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

init();
