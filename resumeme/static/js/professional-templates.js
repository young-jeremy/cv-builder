document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const filterOptions = document.querySelectorAll(".filter-option")
  const sortSelect = document.getElementById("sort-select")
  const clearFiltersBtn = document.getElementById("clear-filters")
  const resetFiltersBtn = document.getElementById("reset-filters")
  const templateCards = document.querySelectorAll(".template-card")
  const templatesCountEl = document.getElementById("templates-count")
  const noTemplatesEl = document.querySelector(".no-templates")

  // Current filter state
  let currentFilters = {
    style: "",
    color: "",
    difficulty: "",
  }

  let currentSort = "popular"

  // Initialize
  updateTemplatesCount()

  // Event listeners
  filterOptions.forEach((option) => {
    option.addEventListener("click", function () {
      const filterType = this.getAttribute("data-filter")
      const filterValue = this.getAttribute("data-value")

      // Update active state in UI
      document.querySelectorAll(`.filter-option[data-filter="${filterType}"]`).forEach((opt) => {
        opt.classList.remove("active")
      })
      this.classList.add("active")

      // Update filter state
      currentFilters[filterType] = filterValue

      // Apply filters
      applyFilters()
    })
  })

  sortSelect.addEventListener("change", function () {
    currentSort = this.value
    sortTemplates()
  })

  clearFiltersBtn.addEventListener("click", clearAllFilters)

  if (resetFiltersBtn) {
    resetFiltersBtn.addEventListener("click", clearAllFilters)
  }

  // Filter functions
  function applyFilters() {
    let visibleCount = 0

    templateCards.forEach((card) => {
      const style = card.getAttribute("data-style")
      const color = card.getAttribute("data-color")
      const difficulty = card.getAttribute("data-difficulty")

      // Check if card matches all active filters
      const styleMatch = !currentFilters.style || currentFilters.style === style
      const colorMatch = !currentFilters.color || currentFilters.color === color
      const difficultyMatch = !currentFilters.difficulty || currentFilters.difficulty === difficulty

      const isVisible = styleMatch && colorMatch && difficultyMatch

      // Show/hide card
      if (isVisible) {
        card.style.display = ""
        visibleCount++
      } else {
        card.style.display = "none"
      }
    })

    // Update count and show/hide empty state
    updateTemplatesCount(visibleCount)

    // Update URL with filter parameters
    updateURL()
  }

  function sortTemplates() {
    const templatesGrid = document.querySelector(".templates-grid")
    const cards = Array.from(templateCards)

    // Sort cards based on current sort option
    cards.sort((a, b) => {
      if (currentSort === "popular") {
        // Sort by popularity (data attribute or class)
        const aPopular = a.querySelector(".template-badge.popular") !== null
        const bPopular = b.querySelector(".template-badge.popular") !== null
        return bPopular - aPopular
      } else if (currentSort === "newest") {
        // This would ideally use a data attribute with creation date
        // For demo purposes, we'll use a random sort
        return Math.random() - 0.5
      } else if (currentSort === "name") {
        // Sort alphabetically by name
        const aName = a.querySelector(".template-name").textContent
        const bName = b.querySelector(".template-name").textContent
        return aName.localeCompare(bName)
      }
      return 0
    })

    // Reorder cards in the DOM
    cards.forEach((card) => {
      templatesGrid.appendChild(card)
    })

    // Update URL with sort parameter
    updateURL()
  }

  function clearAllFilters() {
    // Reset filter state
    currentFilters = {
      style: "",
      color: "",
      difficulty: "",
    }

    // Reset UI
    filterOptions.forEach((option) => {
      if (option.getAttribute("data-value") === "") {
        option.classList.add("active")
      } else {
        option.classList.remove("active")
      }
    })

    // Reset sort
    sortSelect.value = "popular"
    currentSort = "popular"

    // Apply filters
    applyFilters()
    sortTemplates()
  }

  function updateTemplatesCount(count) {
    const visibleCount =
      count !== undefined ? count : Array.from(templateCards).filter((card) => card.style.display !== "none").length

    if (templatesCountEl) {
      templatesCountEl.textContent = visibleCount
    }

    // Show/hide empty state
    if (noTemplatesEl) {
      if (visibleCount === 0) {
        noTemplatesEl.style.display = "block"
      } else {
        noTemplatesEl.style.display = "none"
      }
    }
  }

  function updateURL() {
    // Create URL with current filters and sort
    const params = new URLSearchParams()

    if (currentFilters.style) {
      params.set("style", currentFilters.style)
    }

    if (currentFilters.color) {
      params.set("color", currentFilters.color)
    }

    if (currentFilters.difficulty) {
      params.set("difficulty", currentFilters.difficulty)
    }

    if (currentSort !== "popular") {
      params.set("sort", currentSort)
    }

    // Update URL without reloading the page
    const newURL = window.location.pathname + (params.toString() ? "?" + params.toString() : "")
    window.history.replaceState({}, "", newURL)
  }

  // Initialize from URL parameters
  function initFromURL() {
    const params = new URLSearchParams(window.location.search)

    // Set filters from URL
    if (params.has("style")) {
      const style = params.get("style")
      currentFilters.style = style
      document.querySelector(`.filter-option[data-filter="style"][data-value="${style}"]`)?.classList.add("active")
      document.querySelector(`.filter-option[data-filter="style"][data-value=""]`)?.classList.remove("active")
    }

    if (params.has("color")) {
      const color = params.get("color")
      currentFilters.color = color
      document.querySelector(`.filter-option[data-filter="color"][data-value="${color}"]`)?.classList.add("active")
      document.querySelector(`.filter-option[data-filter="color"][data-value=""]`)?.classList.remove("active")
    }

    if (params.has("difficulty")) {
      const difficulty = params.get("difficulty")
      currentFilters.difficulty = difficulty
      document
        .querySelector(`.filter-option[data-filter="difficulty"][data-value="${difficulty}"]`)
        ?.classList.add("active")
      document.querySelector(`.filter-option[data-filter="difficulty"][data-value=""]`)?.classList.remove("active")
    }

    // Set sort from URL
    if (params.has("sort")) {
      const sort = params.get("sort")
      currentSort = sort
      if (sortSelect) {
        sortSelect.value = sort
      }
    }

    // Apply filters and sort
    applyFilters()
    sortTemplates()
  }

  // Initialize from URL
  initFromURL()

  // Template preview hover effects
  templateCards.forEach((card) => {
    const previewImg = card.querySelector(".template-preview img")

    card.addEventListener("mouseenter", () => {
      if (previewImg) {
        previewImg.style.transform = "translateY(-10%)"
      }
    })

    card.addEventListener("mouseleave", () => {
      if (previewImg) {
        previewImg.style.transform = "translateY(0)"
      }
    })
  })

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const targetId = this.getAttribute("href")
      if (targetId === "#") return

      const targetElement = document.querySelector(targetId)
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 100,
          behavior: "smooth",
        })
      }
    })
  })

  // Sticky filters on scroll
  const filtersSection = document.querySelector(".filters-section")
  const filtersSectionTop = filtersSection ? filtersSection.offsetTop : 0

  window.addEventListener("scroll", () => {
    if (filtersSection) {
      if (window.pageYOffset > filtersSectionTop) {
        filtersSection.classList.add("sticky")
      } else {
        filtersSection.classList.remove("sticky")
      }
    }
  })
})

