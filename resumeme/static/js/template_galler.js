// Template Gallery JavaScript
document.addEventListener("DOMContentLoaded", () => {
  // Template card hover effects
  const templateCards = document.querySelectorAll(".template-card")

  templateCards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.classList.add("shadow")
    })

    card.addEventListener("mouseleave", function () {
      this.classList.remove("shadow")
    })
  })

  // Filter functionality
  const filterButtons = document.querySelectorAll(".filter-btn")

  filterButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault()

      // Update active button
      filterButtons.forEach((btn) => btn.classList.remove("active"))
      this.classList.add("active")

      // Get filter value
      const filter = this.dataset.filter

      // Filter templates
      templateCards.forEach((card) => {
        if (filter === "all" || card.dataset.category === filter) {
          card.closest(".col-md-4").style.display = "block"
        } else {
          card.closest(".col-md-4").style.display = "none"
        }
      })
    })
  })
})

