document.addEventListener('DOMContentLoaded', function() {
    // Character counter for bio
    const bioTextarea = document.getElementById('{{ form.bio.id_for_label }}');
    const bioCounter = document.getElementById('bio-counter');
    
    if (bioTextarea && bioCounter) {
        // Initialize counter with current text length
        bioCounter.textContent = bioTextarea.value.length;
        
        // Update counter as user types
        bioTextarea.addEventListener('input', function() {
            bioCounter.textContent = this.value.length;
            
            // Add visual feedback when approaching limit
            if (this.value.length > 220) {
                bioCounter.classList.add('text-warning');
            } else if (this.value.length > 240) {
                bioCounter.classList.remove('text-warning');
                bioCounter.classList.add('text-danger');
            } else {
                bioCounter.classList.remove('text-warning', 'text-danger');
            }
        });
    }
    
    // Smooth scroll for sidebar navigation
    const sidebarLinks = document.querySelectorAll('.list-group-item-action');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerOffset = 100;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
});

$(document).ready(function() {
    // Character counter for bio
    $('#{{ form.bio.id_for_label }}').on('input', function() {
        var characterCount = $(this).val().length;
        $('#bio-counter').text(characterCount);
        
        // Optional: Add warning when approaching limit
        if (characterCount > 230) {
            $('#bio-counter').addClass('text-danger');
        } else {
            $('#bio-counter').removeClass('text-danger');
        }
    });
    
    // Trigger the input event to update counter on page load
    $('#{{ form.bio.id_for_label }}').trigger('input');
    
    // Smooth scroll to sections
    $('.list-group-item').click(function(e) {
        e.preventDefault();
        var target = $(this).attr('href');
        $('html, body').animate({
            scrollTop: $(target).offset().top - 100
        }, 500);
    });
    
    // Preview image before upload
    $('#{{ form.profile_image.id_for_label }}').change(function() {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('img.rounded-circle').attr('src', e.target.result);
            }
            reader.readAsDataURL(this.files[0]);
        }
    });
    
    // Form validation
    $('#profile-form').submit(function(e) {
        var bioLength = $('#{{ form.bio.id_for_label }}').val().length;
        if (bioLength > 250) {
            e.preventDefault();
            alert('Bio is too long! Please keep it under 250 characters.');
            return false;
        }
        return true;
    });
});