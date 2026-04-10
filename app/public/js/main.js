// Small page-load effect so cards fade in with a subtle stagger.
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".card");
  cards.forEach((card, index) => {
    card.animate(
      [
        { opacity: 0, transform: "translateY(12px)" },
        { opacity: 1, transform: "translateY(0)" }
      ],
      {
        duration: 420,
        delay: index * 60,
        easing: "ease-out",
        fill: "forwards"
      }
    );
  });

  const mainProductImage = document.querySelector("#mainProductImage");
  const thumbs = document.querySelectorAll("[data-gallery-thumb]");

  thumbs.forEach((thumb) => {
    thumb.addEventListener("click", () => {
      if (!mainProductImage) {
        return;
      }

      thumbs.forEach((item) => item.classList.remove("is-active"));
      thumb.classList.add("is-active");
      mainProductImage.src = thumb.dataset.image || mainProductImage.src;
      mainProductImage.alt = thumb.dataset.alt || mainProductImage.alt;
    });
  });
});
