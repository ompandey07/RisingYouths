  // Mobile Menu Toggle
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');
        const mobileMenuClose = document.getElementById('mobile-menu-close');

        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.add('active');
        });

        mobileMenuClose.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
        });

        // Hero Carousel
        const slides = document.querySelectorAll('.hero-slide');
        const dots = document.querySelectorAll('.nav-dot');
        let currentSlide = 0;

        function showSlide(index) {
            // Remove active class from all slides and dots
            slides.forEach(slide => slide.classList.remove('active'));
            dots.forEach(dot => {
                dot.classList.remove('active');
                dot.style.backgroundColor = 'rgba(255, 255, 255, 0.5)';
            });

            // Add active class to current slide and dot
            slides[index].classList.add('active');
            dots[index].classList.add('active');
            dots[index].style.backgroundColor = '#10b981';
        }

        function nextSlide() {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        }

        // Auto-advance slides every 4 seconds
        setInterval(nextSlide, 4000);

        // Dot click handlers
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                currentSlide = index;
                showSlide(currentSlide);
            });
        });

        // Scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    if (entry.target.classList.contains('fade-in-up')) {
                        entry.target.classList.add('animate');
                    }
                    if (entry.target.classList.contains('fade-in-left')) {
                        entry.target.classList.add('animate');
                    }
                    if (entry.target.classList.contains('fade-in-right')) {
                        entry.target.classList.add('animate');
                    }
                    if (entry.target.classList.contains('scale-in')) {
                        entry.target.classList.add('animate');
                    }
                    if (entry.target.classList.contains('slide-in-bottom')) {
                        entry.target.classList.add('animate');
                    }
                }
            });
        }, observerOptions);

        // Observe all animated elements
        document.querySelectorAll('.fade-in-up, .fade-in-left, .fade-in-right, .scale-in, .slide-in-bottom').forEach(el => {
            observer.observe(el);
        });

        // Initial animation for hero content when page loads
        window.addEventListener('load', () => {
            setTimeout(() => {
                const heroTitle = document.querySelector('.hero-title-animate');
                const heroDescription = document.querySelector('.hero-description-animate');
                const heroButtons = document.querySelector('.hero-buttons-animate');
                
                if (heroTitle) {
                    heroTitle.classList.add('animate');
                    // Add floating animation after entrance animation completes
                    setTimeout(() => {
                        heroTitle.classList.add('hero-text-animate');
                    }, 1500);
                }
                if (heroDescription) heroDescription.classList.add('animate');
                if (heroButtons) heroButtons.classList.add('animate');
                
                // Add dramatic entrance sound effect (visual feedback)
                document.body.style.animation = 'none';
                
            }, 500); // Increased delay for more dramatic entrance
        });

        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Add parallax effect to hero section
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            const heroSlides = document.querySelectorAll('.hero-slide');
            
            heroSlides.forEach(slide => {
                slide.style.transform = `translateY(${rate}px)`;
            });
        });

        // Add bounce effect to buttons
        document.querySelectorAll('button, .hero-button-glow').forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.05)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
        });

        // Add shake effect on certain interactions
        function addShakeEffect(element) {
            element.classList.add('shake');
            setTimeout(() => {
                element.classList.remove('shake');
            }, 500);
        }

        // Easter egg: Add shake effect when clicking logo multiple times
        const logo = document.querySelector('.pulse-icon');
        let clickCount = 0;
        logo.addEventListener('click', () => {
            clickCount++;
            if (clickCount >= 5) {
                addShakeEffect(logo);
                clickCount = 0;
            }
        });

        // Add loading animation for empty blog state
        const emptyBlogSection = document.querySelector('.loading-dots');
        if (emptyBlogSection) {
            // Add some interactive behavior for the loading dots
            emptyBlogSection.addEventListener('click', () => {
                emptyBlogSection.style.animation = 'none';
                setTimeout(() => {
                    emptyBlogSection.style.animation = '';
                }, 10);
            });
        }

        // Enhanced scroll effects for service cards
        const serviceCards = document.querySelectorAll('.service-card');
        serviceCards.forEach((card, index) => {
            card.addEventListener('mouseenter', () => {
                card.style.zIndex = '10';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.zIndex = '1';
            });
        });

        // Add dynamic background to navigation on scroll
        window.addEventListener('scroll', () => {
            const nav = document.querySelector('nav');
            if (window.scrollY > 100) {
                nav.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
            } else {
                nav.style.boxShadow = 'none';
            }
        });

        // Performance optimization: Throttle scroll events
        function throttle(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }

        // Apply throttling to scroll-heavy functions
        window.addEventListener('scroll', throttle(() => {
            // Your scroll-heavy code here
        }, 16)); // ~60fps