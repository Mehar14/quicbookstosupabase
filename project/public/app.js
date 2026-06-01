const state = {
  entities: [],
  selectedEntity: null,
  rows: [],
  columns: [],
  filteredRows: [],
};

const sidebar = document.getElementById("sidebar");
const sidebarOverlay = document.getElementById("sidebar-overlay");
const menuBtn = document.getElementById("menu-btn");
const entityNav = document.getElementById("entity-nav");
const pageTitle = document.getElementById("page-title");
const pageSubtitle = document.getElementById("page-subtitle");
const statRecords = document.getElementById("stat-records");
const statTable = document.getElementById("stat-table");
const statStatus = document.getElementById("stat-status");
const loadingEl = document.getElementById("loading");
const emptyState = document.getElementById("empty-state");
const tableWrap = document.getElementById("table-wrap");
const tableHead = document.getElementById("table-head");
const tableBody = document.getElementById("table-body");
const refreshBtn = document.getElementById("refresh-btn");
const searchInput = document.getElementById("search-input");
const themeToggle = document.getElementById("theme-toggle");
const themeIconLight = document.getElementById("theme-icon-light");
const themeIconDark = document.getElementById("theme-icon-dark");
const toast = document.getElementById("toast");
const detailDialog = document.getElementById("detail-dialog");
const detailContent = document.getElementById("detail-content");
const closeDialogBtn = document.getElementById("close-dialog");

const THEME_KEY = "qbo-viewer-theme";
const MOBILE_BREAKPOINT = 960;

function isMobileView() {
  return window.innerWidth <= MOBILE_BREAKPOINT;
}

function openSidebar() {
  sidebar.classList.add("open");
  sidebarOverlay.classList.remove("hidden");
  sidebarOverlay.setAttribute("aria-hidden", "false");
}

function closeSidebar() {
  sidebar.classList.remove("open");
  sidebarOverlay.classList.add("hidden");
  sidebarOverlay.setAttribute("aria-hidden", "true");
}

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem(THEME_KEY, theme);

  const isDark = theme === "dark";
  themeIconLight.classList.toggle("hidden", isDark);
  themeIconDark.classList.toggle("hidden", !isDark);
  themeToggle.setAttribute(
    "aria-label",
    isDark ? "Switch to light mode" : "Switch to dark mode"
  );
}

function initTheme() {
  const savedTheme = localStorage.getItem(THEME_KEY);
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(savedTheme || (prefersDark ? "dark" : "light"));
}

function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute("data-theme");
  applyTheme(currentTheme === "dark" ? "light" : "dark");
}

function showToast(message, type = "default") {
  toast.textContent = message;
  toast.className = `toast ${type}`;
  toast.classList.remove("hidden");

  window.clearTimeout(showToast.timeoutId);
  showToast.timeoutId = window.setTimeout(() => {
    toast.classList.add("hidden");
  }, 4000);
}

async function parseJsonResponse(response) {
  const text = await response.text();

  try {
    return JSON.parse(text);
  } catch {
    const preview = text.replace(/\s+/g, " ").trim().slice(0, 120);
    throw new Error(
      `Server returned invalid JSON (${response.status}). ${preview || "Empty response."}`
    );
  }
}

function setLoading(isLoading) {
  loadingEl.classList.toggle("hidden", !isLoading);
}

function formatColumnLabel(column) {
  return column
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatCellValue(value) {
  if (value === null || value === undefined || value === "") {
    return "—";
  }
  if (typeof value === "boolean") {
    return value ? "Yes" : "No";
  }
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  return String(value);
}

function renderEntityNav() {
  entityNav.innerHTML = "";

  state.entities.forEach((entity) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `entity-link${state.selectedEntity === entity.name ? " active" : ""}`;
    button.innerHTML = `
      <span>${entity.label}</span>
      <span class="entity-count">${entity.count ?? 0}</span>
    `;
    button.addEventListener("click", () => selectEntity(entity.name));
    entityNav.appendChild(button);
  });
}

function renderTable() {
  tableHead.innerHTML = "";
  tableBody.innerHTML = "";

  const headerRow = document.createElement("tr");
  state.columns.forEach((column) => {
    const th = document.createElement("th");
    th.textContent = formatColumnLabel(column);
    headerRow.appendChild(th);
  });

  const detailsHeader = document.createElement("th");
  detailsHeader.textContent = "Details";
  headerRow.appendChild(detailsHeader);
  tableHead.appendChild(headerRow);

  state.filteredRows.forEach((row) => {
    const tr = document.createElement("tr");

    state.columns.forEach((column) => {
      const td = document.createElement("td");
      const span = document.createElement("span");
      span.className = "cell-value";
      span.textContent = formatCellValue(row[column]);
      span.title = formatCellValue(row[column]);
      td.appendChild(span);
      tr.appendChild(td);
    });

    const detailsCell = document.createElement("td");
    const viewBtn = document.createElement("button");
    viewBtn.type = "button";
    viewBtn.className = "view-btn";
    viewBtn.textContent = "View JSON";
    viewBtn.addEventListener("click", () => openDetails(row));
    detailsCell.appendChild(viewBtn);
    tr.appendChild(detailsCell);

    tableBody.appendChild(tr);
  });
}

function openDetails(row) {
  detailContent.textContent = JSON.stringify(row, null, 2);
  detailDialog.showModal();
}

function applySearchFilter() {
  const query = searchInput.value.trim().toLowerCase();

  if (!query) {
    state.filteredRows = [...state.rows];
  } else {
    state.filteredRows = state.rows.filter((row) =>
      Object.values(row).some((value) =>
        formatCellValue(value).toLowerCase().includes(query)
      )
    );
  }

  statRecords.textContent = String(state.filteredRows.length);
  renderTable();
}

async function loadEntities() {
  const response = await fetch("/api/entities");
  const payload = await parseJsonResponse(response);
  if (!response.ok) {
    throw new Error(payload.message || payload.error || "Failed to load entities");
  }
  state.entities = payload.entities || [];
  renderEntityNav();
}

async function loadEntityData(entityName) {
  setLoading(true);
  emptyState.classList.add("hidden");

  try {
    const response = await fetch(`/api/data/${entityName}`);
    const payload = await parseJsonResponse(response);
    if (!response.ok) {
      throw new Error(payload.message || payload.error || "Failed to load entity data");
    }
    state.rows = payload.rows || [];
    state.columns = payload.columns || [];
    state.filteredRows = [...state.rows];

    pageTitle.textContent = payload.label;
    pageSubtitle.textContent = `Showing synced ${payload.label} records from Supabase.`;
    statRecords.textContent = String(state.filteredRows.length);
    statTable.textContent = payload.table;
    statStatus.textContent = "Loaded";

    searchInput.disabled = false;
    emptyState.classList.add("hidden");
    tableWrap.classList.remove("hidden");
    renderTable();
  } catch (error) {
    statStatus.textContent = "Error";
    showToast(error.message, "error");
    tableWrap.classList.add("hidden");
    emptyState.classList.remove("hidden");
  } finally {
    setLoading(false);
  }
}

async function selectEntity(entityName) {
  state.selectedEntity = entityName;
  renderEntityNav();

  if (isMobileView()) {
    closeSidebar();
  }

  await loadEntityData(entityName);
}

async function refreshFromQuickBooks() {
  refreshBtn.disabled = true;
  statStatus.textContent = "Refreshing...";

  try {
    const response = await fetch("/api/refresh", { method: "POST" });
    const payload = await parseJsonResponse(response);

    if (!response.ok) {
      throw new Error(payload.message || "Refresh failed");
    }

    await loadEntities();

    if (state.selectedEntity) {
      await loadEntityData(state.selectedEntity);
    }

    statStatus.textContent = "Refreshed";
    showToast(
      payload.message || "Refresh complete.",
      payload.status === "error" ? "error" : "success"
    );
  } catch (error) {
    statStatus.textContent = "Refresh failed";
    showToast(error.message, "error");
  } finally {
    refreshBtn.disabled = false;
  }
}

menuBtn.addEventListener("click", () => {
  if (sidebar.classList.contains("open")) {
    closeSidebar();
  } else {
    openSidebar();
  }
});

sidebarOverlay.addEventListener("click", closeSidebar);
themeToggle.addEventListener("click", toggleTheme);
refreshBtn.addEventListener("click", refreshFromQuickBooks);
searchInput.addEventListener("input", applySearchFilter);
closeDialogBtn.addEventListener("click", () => detailDialog.close());

window.addEventListener("resize", () => {
  if (!isMobileView()) {
    closeSidebar();
  }
});

initTheme();
loadEntities().catch((error) => {
  showToast(error.message, "error");
});
