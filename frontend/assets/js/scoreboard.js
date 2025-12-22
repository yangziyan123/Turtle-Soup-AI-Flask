async function loadScores() {
    const tbody = document.getElementById("score-body");
    const loadingText = (window.I18N && I18N.t("common.loading", "Loading...")) || "Loading...";
    tbody.innerHTML = `<tr><td colspan='3'>${loadingText}</td></tr>`;
    try {
        const lang = (window.I18N && I18N.getLang && I18N.getLang()) || "zh";
        const res = await fetch(`/api/scores?lang=${encodeURIComponent(lang)}`);
        const data = await res.json();
        if (!res.ok) {
            const failedText = (window.I18N && I18N.t("common.failedToLoad", "Failed to load")) || "Failed to load";
            tbody.innerHTML = `<tr><td colspan='3'>${failedText}: ${data.error || "error"}</td></tr>`;
            return;
        }
        const list = data.data || [];
        if (list.length === 0) {
            const emptyText = (window.I18N && I18N.t("scoreboard.noScores", "No scores yet.")) || "No scores yet.";
            tbody.innerHTML = `<tr><td colspan='3'>${emptyText}</td></tr>`;
            return;
        }
        tbody.innerHTML = "";
        list.forEach((item, idx) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${idx + 1}</td>
                <td>${item.username || "Unknown"}</td>
                <td class="score">${item.total_score ?? 0}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error(err);
        const errText = (window.I18N && I18N.t("common.networkError", "Network error")) || "Network error";
        tbody.innerHTML = `<tr><td colspan='3'>${errText}</td></tr>`;
    }
}

window.addEventListener("DOMContentLoaded", loadScores);
