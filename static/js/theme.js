const root = document.documentElement;

const theme = localStorage.getItem("theme");

if (theme) {
    root.setAttribute("data-theme", theme);
} else {
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const systemtheme = prefersDark ? "dark" : "light";

    // apply
    root.setAttribute("data-theme", systemtheme);
    // save
    localStorage.setItem("theme", systemtheme);
}

document.getElementById("theme-toggle").addEventListener("click", () => {
    const current = root.getAttribute("data-theme");
    const newtheme = current === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", newtheme);
    localStorage.setItem("theme", newtheme);
});
