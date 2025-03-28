.mobile-menu {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--bg-primary);
    z-index: 2000;
    transform: translateX(-100%);
    transition: transform 0.3s ease-in-out;
}

.mobile-menu.active {
    transform: translateX(0);
}

.mobile-menu-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid var(--border-color);
}

.mobile-menu-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    color: var(--text-secondary);
    cursor: pointer;
}

.mobile-menu-content {
    padding: 1rem;
}

.mobile-nav-link {
    display: block;
    padding: 1rem;
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    border-bottom: 1px solid var(--border-color);
}

.mobile-nav-link:last-child {
    border-bottom: none;
}

// Main JavaScript for the site

document.addEventListener("DOMContentLoaded", () => {
  // Initialize dropdowns
  const dropdowns = document.querySelectorAll(".dropdown-toggle")
  dropdowns.forEach((dropdown) => {
    dropdown.addEventListener("click", function (e) {
      e.preventDefault()
      const dropdownMenu = this.nextElementSibling
      if (dropdownMenu.classList.contains("show")) {
        dropdownMenu.classList.remove("show")
      } else {
        // Close all other dropdowns
        document.querySelectorAll(".dropdown-menu.show").forEach((menu) => {
          menu.classList.remove("show")
        })
        dropdownMenu.classList.add("show")
      }
    })
  })

  // Close dropdowns when clicking outside
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".dropdown")) {
      document.querySelectorAll(".dropdown-menu.show").forEach((menu) => {
        menu.classList.remove("show")
      })
    }
  })

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href")
      if (targetId !== "#") {
        e.preventDefault()
        const target = document.querySelector(targetId)
        if (target) {
          window.scrollTo({
            top: target.offsetTop - 100,
            behavior: "smooth",
          })
        }
      }
    })
  })

  // Counter animation for statistics
  const animateCounter = (element, start, end, duration) => {
    let startTimestamp = null
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp
      const progress = Math.min((timestamp - startTimestamp) / duration, 1)
      const value = Math.floor(progress * (end - start) + start)
      element.textContent = value.toLocaleString()
      if (progress < 1) {
        window.requestAnimationFrame(step)
      }
    }
    window.requestAnimationFrame(step)
  }

  // Animate counters when they come into view
  const counters = document.querySelectorAll(".counter-number, .stat-percentage")
  if (counters.length > 0) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const target = entry.target
            const end = Number.parseInt(target.textContent.replace(/,/g, ""))
            animateCounter(target, 0, end, 2000)
            observer.unobserve(target)
          }
        })
      },
      { threshold: 0.5 },
    )

    counters.forEach((counter) => {
      observer.observe(counter)
    })
  }
})

