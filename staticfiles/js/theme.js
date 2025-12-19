
const root = document.documentElement;

document.getElementById("theme-toggle").addEventListener("click", () => {
const current = root.getAttribute("data-theme");

    // Toggle between light and dark
    const newTheme = current === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", newTheme);

    // Optionally save user preference
    localStorage.setItem("theme", newTheme);
});

// Load saved preference on page load
const saved = localStorage.getItem("theme");
if (saved) root.setAttribute("data-theme", saved);