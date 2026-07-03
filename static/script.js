document.addEventListener("DOMContentLoaded", () => {
    const input = document.querySelector(".movie-search");

    input.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            this.form.submit();
        }
    });
});