// 点击模式卡片 -> 选中样式切换
document.querySelectorAll(".mode-option").forEach(opt => {
    opt.addEventListener("click", () => {
        document.querySelectorAll(".mode-option").forEach(o => o.classList.remove("selected"));
        opt.classList.add("selected");
    });
});

// 点击 "Start Game"
function startGame() {
    const selected = document.querySelector(".mode-option.selected");
    const mode = selected.dataset.mode;

    const riddleId = window.location.pathname.split("/")[2];

    window.location.href = `/game/${riddleId}/${mode}`;
}
