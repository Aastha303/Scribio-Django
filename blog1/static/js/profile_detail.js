    document.addEventListener('DOMContentLoaded', function() {
        // Follow button functionality
        const followButton = document.getElementById('follow-button');
        if (followButton) {
            followButton.addEventListener('click', function() {
                const username = this.getAttribute('data-username');
                const isFollowing = this.innerHTML.includes('Following');
                
                // Send AJAX request to follow/unfollow
                fetch(`/api/follow/${username}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update button text and icon
                        if (isFollowing) {
                            this.innerHTML = '<i class="fas fa-user-plus me-2"></i>Follow';
                            document.getElementById('followers-count').textContent = 
                                parseInt(document.getElementById('followers-count').textContent) - 1;
                        } else {
                            this.innerHTML = '<i class="fas fa-user-check me-2"></i>Following';
                            document.getElementById('followers-count').textContent = 
                                parseInt(document.getElementById('followers-count').textContent) + 1;
                        }
                    }
                });
            });
        }
        
        // Function to get CSRF cookie
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        
        // Animate elements on scroll
        const animateElements = document.querySelectorAll('.slide-up, .fade-in');
        
        function checkIfInView() {
            animateElements.forEach(element => {
                const elementTop = element.getBoundingClientRect().top;
                const windowHeight = window.innerHeight;
                
                if (elementTop < windowHeight - 100) {
                    element.classList.add('animate__animated');
                    
                    if (element.classList.contains('slide-up')) {
                        element.classList.add('animate__fadeInUp');
                    } else if (element.classList.contains('fade-in')) {
                        element.classList.add('animate__fadeIn');
                    }
                }
            });
        }
        
        // Check elements on load
        checkIfInView();
        
        // Check elements on scroll
        window.addEventListener('scroll', checkIfInView);
    });

    