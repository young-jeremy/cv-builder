document.addEventListener("DOMContentLoaded", () => {
  // Mobile menu toggle
  const mobileMenuToggle = document.querySelector(".mobile-menu-toggle")
  const mobileNav = document.querySelector(".mobile-nav")

  if (mobileMenuToggle && mobileNav) {
    mobileMenuToggle.addEventListener("click", () => {
      mobileNav.classList.toggle("active")
      document.body.classList.toggle("menu-open")
    })
  }

  // Mobile submenu toggles
  const mobileNavToggles = document.querySelectorAll(".mobile-nav-toggle")

  if (mobileNavToggles.length > 0) {
    mobileNavToggles.forEach((toggle) => {
      toggle.addEventListener("click", function () {
        const subnav = this.nextElementSibling
        if (subnav) {
          subnav.classList.toggle("active")

          // Toggle icon
          const icon = this.querySelector("i")
          if (icon) {
            if (subnav.classList.contains("active")) {
              icon.classList.remove("bi-chevron-down")
              icon.classList.add("bi-chevron-up")
            } else {
              icon.classList.remove("bi-chevron-up")
              icon.classList.add("bi-chevron-down")
            }
          }
        }
      })
    })
  }

  // Close messages
  const messageCloseButtons = document.querySelectorAll(".message-close")

  if (messageCloseButtons.length > 0) {
    messageCloseButtons.forEach((button) => {
      button.addEventListener("click", function () {
        const message = this.closest(".message")
        if (message) {
          message.style.height = message.offsetHeight + "px"
          message.offsetHeight // Force reflow
          message.style.height = "0"
          message.style.opacity = "0"
          message.style.padding = "0"
          message.style.margin = "0"
          message.style.overflow = "hidden"
          message.style.transition = "all 0.3s ease"

          setTimeout(() => {
            message.remove()
          }, 300)
        }
      })
    })
  }

  // Auto-hide messages after 5 seconds
  const messages = document.querySelectorAll(".message")

  if (messages.length > 0) {
    setTimeout(() => {
      messages.forEach((message) => {
        const closeButton = message.querySelector(".message-close")
        if (closeButton) {
          closeButton.click()
        }
      })
    }, 5000)
  }

  // Dropdown positioning
  const dropdowns = document.querySelectorAll(".dropdown")

  if (dropdowns.length > 0) {
    dropdowns.forEach((dropdown) => {
      const dropdownMenu = dropdown.querySelector(".dropdown-menu")

      if (dropdownMenu) {
        // Check if dropdown would go off-screen to the right
        dropdown.addEventListener("mouseenter", () => {
          const rect = dropdownMenu.getBoundingClientRect()
          const viewportWidth = window.innerWidth || document.documentElement.clientWidth

          if (rect.right > viewportWidth) {
            dropdownMenu.style.left = "auto"
            dropdownMenu.style.right = "0"
          }
        })
      }
    })
  }

  // Sticky header shadow
  const header = document.querySelector(".site-header")

  if (header) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 10) {
        header.classList.add("scrolled")
        header.style.boxShadow = "var(--shadow-md)"
      } else {
        header.classList.remove("scrolled")
        header.style.boxShadow = "var(--shadow-sm)"
      }
    })
  }

  // Smooth scrolling for anchor links
  const anchorLinks = document.querySelectorAll('a[href^="#"]:not([href="#"])')

  if (anchorLinks.length > 0) {
    anchorLinks.forEach((link) => {
      link.addEventListener("click", function (e) {
        e.preventDefault()

        const targetId = this.getAttribute("href")
        const targetElement = document.querySelector(targetId)

        if (targetElement) {
          const headerHeight = document.querySelector(".site-header").offsetHeight
          const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight

          window.scrollTo({
            top: targetPosition,
            behavior: "smooth",
          })

          // Update URL without page reload
          history.pushState(null, null, targetId)
        }
      })
    })
  }
})

// Resume counter animation and update
document.addEventListener("DOMContentLoaded", () => {
  // Resume counter animation
  const resumeCounter = document.getElementById("resumeCounterValue")
  if (resumeCounter) {
    const finalCount = Number.parseInt(resumeCounter.textContent.replace(/,/g, ""))
    const startCount = Math.max(finalCount - 1000, 0)
    const duration = 2000 // 2 seconds
    const frameDuration = 1000 / 60 // 60fps
    const totalFrames = Math.round(duration / frameDuration)
    const countIncrement = (finalCount - startCount) / totalFrames

    let currentCount = startCount
    let frame = 0

    const animateCount = () => {
      currentCount += countIncrement
      resumeCounter.textContent = Math.floor(currentCount).toLocaleString()

      if (frame < totalFrames) {
        frame++
        requestAnimationFrame(animateCount)
      } else {
        resumeCounter.textContent = finalCount.toLocaleString()

        // Start the periodic update after initial animation
        setInterval(updateResumeCounter, 30000) // Update every 30 seconds
      }
    }

    animateCount()
  }

  // Periodic counter update
  function updateResumeCounter() {
    const resumeCounter = document.getElementById("resumeCounterValue")
    if (resumeCounter) {
      const currentCount = Number.parseInt(resumeCounter.textContent.replace(/,/g, ""))
      // Add a random number between 1 and 5
      const newCount = currentCount + Math.floor(Math.random() * 5) + 1
      resumeCounter.textContent = newCount.toLocaleString()
    }
  }

  // AI Assistant functionality
  const aiButton = document.getElementById("aiAssistantButton")
  const aiModal = document.getElementById("aiAssistantModal")
  const aiModalClose = document.getElementById("aiModalClose")
  const aiChatInput = document.getElementById("aiChatInput")
  const aiChatSend = document.getElementById("aiChatSend")
  const aiChatMessages = document.getElementById("aiChatMessages")

  if (aiButton && aiModal) {
    aiButton.addEventListener("click", () => {
      aiModal.style.display = "flex"
    })

    aiModalClose.addEventListener("click", () => {
      aiModal.style.display = "none"
    })

    // Simple chat functionality
    if (aiChatSend && aiChatInput) {
      aiChatSend.addEventListener("click", sendAiMessage)
      aiChatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault()
          sendAiMessage()
        }
      })
    }

    function sendAiMessage() {
      const message = aiChatInput.value.trim()
      if (message) {
        // Add user message
        const userMessageHtml = `
          <div class="ai-message user-message" style="justify-content: flex-end;">
            <div class="ai-message-content" style="background-color: var(--primary-light); color: var(--primary-dark);">
              <p>${message}</p>
            </div>
          </div>
        `
        aiChatMessages.insertAdjacentHTML("beforeend", userMessageHtml)

        // Clear input
        aiChatInput.value = ""

        // Scroll to bottom
        aiChatMessages.scrollTop = aiChatMessages.scrollHeight

        // Simulate AI response (in a real app, this would call your backend)
        setTimeout(() => {
          const aiResponses = [
            "I can help you improve that section of your resume. Try being more specific about your achievements.",
            "Great question! For your industry, I recommend highlighting your technical skills and quantifiable results.",
            "Consider using action verbs at the beginning of each bullet point to make your experience more impactful.",
            "Your resume looks good! To make it even better, try to customize it for each job application.",
          ]

          const randomResponse = aiResponses[Math.floor(Math.random() * aiResponses.length)]

          const aiMessageHtml = `
            <div class="ai-message">
              <div class="ai-avatar">
                <i class="bi bi-robot"></i>
              </div>
              <div class="ai-message-content">
                <p>${randomResponse}</p>
              </div>
            </div>
          `

          aiChatMessages.insertAdjacentHTML("beforeend", aiMessageHtml)

          // Scroll to bottom
          aiChatMessages.scrollTop = aiChatMessages.scrollHeight
        }, 1000)
      }
    }
  }

  // Cookie consent banner
  const cookieConsent = document.getElementById("cookieConsent")
  const cookieAccept = document.getElementById("cookieAccept")
  const cookieSettings = document.getElementById("cookieSettings")

  if (cookieConsent) {
    // Check if user has already accepted cookies
    const cookiesAccepted = localStorage.getItem("cookiesAccepted")

    if (!cookiesAccepted) {
      // Show the cookie banner after a short delay
      setTimeout(() => {
        cookieConsent.style.display = "block"
      }, 2000)
    }

    if (cookieAccept) {
      cookieAccept.addEventListener("click", () => {
        localStorage.setItem("cookiesAccepted", "true")
        cookieConsent.style.display = "none"
      })
    }

    if (cookieSettings) {
      cookieSettings.addEventListener("click", () => {
        // In a real app, this would open cookie settings
        alert("Cookie settings would open here")
      })
    }
  }

  // Feedback button
  const feedbackButton = document.getElementById("feedbackButton")

  if (feedbackButton) {
    feedbackButton.addEventListener("click", () => {
      // In a real app, this would open a feedback form
      alert("Feedback form would open here")
    })
  }
})

