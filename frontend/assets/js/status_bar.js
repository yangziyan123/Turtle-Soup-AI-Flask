(function () {
    // 1. Initial Styles and Elements
    // Add a style to support hiding elements by default (prevent flash)
    const style = document.createElement('style');
    style.innerHTML = `
        .auth-hidden { display: none !important; }
        .status-bar-global {
            background-color: #333;
            color: #fff;
            width: 100%;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding: 0 20px;
            font-size: 13px;
            font-family: 'Quicksand', sans-serif;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 10000;
            box-sizing: border-box;
        }
        body.has-status-bar {
            margin-top: 30px;
        }
        body.has-status-bar header.top-section {
            top: 30px;
        }
        body.has-status-bar .topbar {
            top: 30px;
        }
    `;
    document.head.appendChild(style);

    // 2. Logic to run on clear
    async function checkAuthAndRender() {
        const token = localStorage.getItem("token");
        const path = window.location.pathname;

        // AUTH CHECK FOR ADMIN PAGE
        if (path.includes("admin.html")) {
            if (!token) {
                window.location.protocol + "//" + window.location.host + "/login.html"
                window.location.href = "/login.html";
                return;
            }
        }

        if (!token) {
            // If on admin page and no token (and script above failed?), force redirect
            if (path.includes("admin.html")) {
                window.location.href = "/login.html";
            }
            return;
        }

        try {
            const headers = { "Authorization": `Bearer ${token}` };
            const res = await fetch("/api/auth/me", { headers });

            if (res.status === 401) {
                if (path.includes("admin.html")) {
                    window.location.href = "/login.html";
                }
                localStorage.removeItem("token");
                return;
            }

            const data = await res.json();
            if (res.ok && data.user) {
                const user = data.user;

                // --- RENDER STATUS BAR ---
                const bar = document.createElement("div");
                bar.className = "status-bar-global";
                bar.innerHTML = `
                    <span style="margin-right: 15px;">Logged in as: <b>${user.username}</b></span>
                `;
                document.body.classList.add("has-status-bar");
                document.body.insertBefore(bar, document.body.firstChild);

                // --- PAGE SPECIFIC LOGIC ---

                // Admin Page Logic
                if (path.includes("admin.html")) {
                    if (!user.is_admin) {
                        window.location.href = "/login.html";
                        return;
                    }
                    document.body.classList.remove("auth-hidden");
                }

                // Index Page Logic
                if (path.endsWith("index.html") || path === "/") {
                    const adminBtn = document.querySelector('a[href="/admin.html"]');
                    if (adminBtn) {
                        if (user.is_admin) {
                            adminBtn.style.display = "inline-flex";
                        } else {
                            adminBtn.style.display = "none";
                        }
                    }
                }
            }
        } catch (err) {
            console.error("Status bar auth check failed", err);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", checkAuthAndRender);
    } else {
        checkAuthAndRender();
    }
})();
