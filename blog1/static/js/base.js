// Scroll reveal animation
function reveal() {
    var reveals = document.querySelectorAll(".reveal");
    
    reveals.forEach(element => {
        var windowHeight = window.innerHeight;
        var elementTop = element.getBoundingClientRect().top;
        var elementVisible = 150;
        
        if (elementTop < windowHeight - elementVisible) {
            element.classList.add("active");
        }
    });
}

// Animate elements on page load
document.addEventListener("DOMContentLoaded", function() {
    // Add animation classes to elements
    document.querySelectorAll('.blog-card').forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate-slide-up');
    });

    document.querySelectorAll('.topic-tag').forEach((tag, index) => {
        tag.style.animationDelay = `${index * 0.05}s`;
        tag.classList.add('animate-fade-in');
    });
});

// Handle scroll animations
window.addEventListener("scroll", reveal);
reveal();