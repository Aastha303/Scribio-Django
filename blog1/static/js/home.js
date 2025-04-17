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

window.addEventListener("scroll", reveal);
reveal();