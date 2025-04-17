$(document).ready(function() {
    // Follow button functionality
    $('.follow-button').click(function() {
        var username = $(this).data('username');
        var button = $(this);
        
        $.ajax({
            url: '/profile/' + username + '/follow/',
            type: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            },
            success: function(data) {
                if (data.success) {
                    if (data.is_following) {
                        button.removeClass('bg-white border border-primary text-primary').addClass('bg-primary text-white');
                        button.html('<i class="fas fa-check mr-2"></i>Following');
                    } else {
                        button.removeClass('bg-primary text-white').addClass('bg-white border border-primary text-primary');
                        button.html('<i class="fas fa-plus mr-2"></i>Follow');
                    }
                }
            }
        });
    });
    
    // Search functionality
    $("#followingSearch").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#followingList .following-item").filter(function() {
            $(this).toggle($(this).find(".following-name").text().toLowerCase().indexOf(value) > -1)
        });
    });
    
    // Animation for list items
    $(".following-item").each(function(index) {
        $(this).css('animation-delay', (index * 0.1) + 's');
        $(this).addClass('animate__animated animate__fadeIn');
    });
});