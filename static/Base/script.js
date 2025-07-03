 // Mobile menu functionality
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');
        const mobileMenuClose = document.getElementById('mobile-menu-close');

        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        mobileMenuClose.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
            document.body.style.overflow = 'auto';
        });

        // Close mobile menu when clicking on a link
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('active');
                document.body.style.overflow = 'auto';
            });
        });

        // Add smooth scrolling behavior
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            });
        });

        // Add scroll effect to navigation dots
        const dots = document.querySelectorAll('.absolute.bottom-8 .w-3');
        let currentDot = 0;
        
        setInterval(() => {
            if (dots.length > 0) {
                dots[currentDot].classList.remove('bg-white');
                dots[currentDot].classList.add('bg-white/50');
                currentDot = (currentDot + 1) % dots.length;
                dots[currentDot].classList.remove('bg-white/50');
                dots[currentDot].classList.add('bg-white');
            }
        }, 3000);

        // News section scrolling functionality
        document.addEventListener('DOMContentLoaded', function() {
            const scrollContainer = document.querySelector('.news-scroll-container');
            const newsTrack = document.querySelector('.news-track');
            const leftArrow = document.getElementById('scroll-left');
            const rightArrow = document.getElementById('scroll-right');
            
            if (leftArrow && rightArrow && scrollContainer) {
                leftArrow.addEventListener('click', function() {
                    // Pause animation temporarily
                    newsTrack.style.animationPlayState = 'paused';
                    scrollContainer.scrollBy({
                        left: -320,
                        behavior: 'smooth'
                    });
                    // Resume animation after scroll
                    setTimeout(() => {
                        newsTrack.style.animationPlayState = 'running';
                    }, 500);
                });
                
                rightArrow.addEventListener('click', function() {
                    // Pause animation temporarily
                    newsTrack.style.animationPlayState = 'paused';
                    scrollContainer.scrollBy({
                        left: 320,
                        behavior: 'smooth'
                    });
                    // Resume animation after scroll
                    setTimeout(() => {
                        newsTrack.style.animationPlayState = 'running';
                    }, 500);
                });
            }
        });

        // Handle window resize for mobile menu
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 768) {
                mobileMenu.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });