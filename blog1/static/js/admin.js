    // Sample data for charts
        const activityData = {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'User Activity',
                backgroundColor: 'rgba(20, 184, 166, 0.2)',
                borderColor: '#0D9488',
                borderWidth: 2,
                data: [65, 59, 80, 81, 56, 55, 72],
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#0D9488'
            }]
        };
        
        // Initialize charts when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            // Activity chart
            const activityCtx = document.getElementById('activityChart').getContext('2d');
            const activityChart = new Chart(activityCtx, {
                type: 'line',
                data: activityData,
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                drawBorder: false
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
            
            // Tab navigation
            const navItems = document.querySelectorAll('.nav-item');
            const contentTabs = document.querySelectorAll('.content-tabs');
            
            navItems.forEach(item => {
                item.addEventListener('click', function() {
                    const tabId = this.getAttribute('data-tab');
                    
                    // Remove active class from all nav items
                    navItems.forEach(navItem => {
                        navItem.classList.remove('active');
                    });
                    
                    // Add active class to clicked nav item
                    this.classList.add('active');
                    
                    // Hide all content tabs
                    contentTabs.forEach(tab => {
                        tab.classList.remove('active');
                    });
                    
                    // Show the selected content tab
                    document.getElementById(tabId).classList.add('active');
                });
            });
            
            // View report modal
            const reportButtons = document.querySelectorAll('.view-report');
            const reportModal = document.getElementById('reportModal');
            const closeButtons = document.querySelectorAll('.modal-close');
            
            reportButtons.forEach(button => {
                button.addEventListener('click', function() {
                    reportModal.style.display = 'flex';
                });
            });
            
            closeButtons.forEach(button => {
                button.addEventListener('click', function() {
                    reportModal.style.display = 'none';
                    addUserModal.style.display = 'none';
                });
            });
            
            // Add User modal
            const addUserBtn = document.getElementById('addUserBtn');
            const addUserModal = document.getElementById('addUserModal');
            
            addUserBtn.addEventListener('click', function() {
                addUserModal.style.display = 'flex';
            });
            
            // Close modals when clicking outside
            window.addEventListener('click', function(event) {
                if (event.target === reportModal) {
                    reportModal.style.display = 'none';
                }
                if (event.target === addUserModal) {
                    addUserModal.style.display = 'none';
                }
            });
            
            // View all reported content button
            const viewAllReported = document.getElementById('viewAllReported');
            viewAllReported.addEventListener('click', function() {
                // Navigate to reported tab
                navItems.forEach(navItem => {
                    navItem.classList.remove('active');
                    if (navItem.getAttribute('data-tab') === 'reported') {
                        navItem.classList.add('active');
                    }
                });
                
                contentTabs.forEach(tab => {
                    tab.classList.remove('active');
                });
                document.getElementById('reported').classList.add('active');
            });
        });
        // Reported content functionality
document.addEventListener('DOMContentLoaded', function() {
    // Store reported content data
    const reportedItems = [
        {
            id: 1,
            title: "Inappropriate language in post",
            author: "Ryan Adams",
            reporter: "Multiple Users",
            reason: "This post contains offensive language that violates community guidelines",
            content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse potenti. Mauris [offensive content] nec magna. Suspendisse potenti. Duis aute irure dolor in reprehenderit.",
            date: "Apr 9, 2025",
            status: "Pending"
        },
        {
            id: 2,
            title: "Spam content detected",
            author: "Marketing123",
            reporter: "Jane Doe",
            reason: "Multiple users reported this post as spam content with promotional links",
            content: "Check out our amazing products at [suspicious link removed]. Best deals guaranteed! Buy now with 80% discount! Limited offer! [Multiple spam links]",
            date: "Apr 9, 2025",
            status: "Pending"
        },
        {
            id: 3,
            title: "Copyright infringement claim",
            author: "Photo_Expert",
            reporter: "Original Creator",
            reason: "User claimed this content was copied from their original work without permission",
            content: "This tutorial on photography techniques appears to be copied from a professional publication without attribution. The images and text are identical to the original source.",
            date: "Apr 8, 2025",
            status: "Pending"
        },
        {
            id: 4,
            title: "Political misinformation",
            author: "NewsObserver",
            reporter: "FactChecker",
            reason: "Contains factually incorrect statements about recent political events",
            content: "The article makes claims about election results and government policies that have been verified as false by multiple fact-checking organizations.",
            date: "Apr 7, 2025",
            status: "Pending"
        },
        {
            id: 5,
            title: "Harassment in comment section",
            author: "Anonymous User",
            reporter: "Multiple Users",
            reason: "Targeting specific community members with hostile language",
            content: "The comment thread contains personal attacks against another user including derogatory language and threats.",
            date: "Apr 7, 2025",
            status: "Pending"
        }
    ];

    // Dashboard reported posts functionality
    const dashboardReportedSection = document.querySelector('.reported-posts');
    if (dashboardReportedSection) {
        const reportedPosts = dashboardReportedSection.querySelectorAll('.reported-post');
        
        // Add event listeners to review buttons on dashboard
        reportedPosts.forEach((post, index) => {
            const reviewBtn = post.querySelector('.btn-primary');
            if (reviewBtn) {
                reviewBtn.addEventListener('click', function() {
                    openReportModal(reportedItems[index]);
                });
            }
            
            const deleteBtn = post.querySelector('.btn-danger');
            if (deleteBtn) {
                deleteBtn.addEventListener('click', function() {
                    if (confirm('Are you sure you want to delete this post?')) {
                        post.style.opacity = '0.5';
                        setTimeout(() => {
                            post.remove();
                            updateReportCounter(-1);
                        }, 500);
                    }
                });
            }
            
            const warnBtn = post.querySelector('.btn-warning');
            if (warnBtn) {
                warnBtn.addEventListener('click', function() {
                    alert(`Warning sent to ${reportedItems[index].author}`);
                    post.style.opacity = '0.5';
                    setTimeout(() => {
                        post.remove();
                        updateReportCounter(-1);
                    }, 500);
                });
            }
        });
    }

    // Reported content tab functionality
    const reportedTab = document.getElementById('reported');
    if (reportedTab) {
        const viewReportButtons = reportedTab.querySelectorAll('.view-report');
        const approveButtons = reportedTab.querySelectorAll('.approve-content');
        const deleteButtons = reportedTab.querySelectorAll('.delete-content');
        
        viewReportButtons.forEach((button, index) => {
            button.addEventListener('click', function() {
                const tableRow = this.closest('tr');
                const title = tableRow.querySelector('td:nth-child(2)').textContent;
                const author = tableRow.querySelector('td:nth-child(3)').textContent;
                const reporter = tableRow.querySelector('td:nth-child(4)').textContent;
                const reason = tableRow.querySelector('td:nth-child(5)').textContent;
                
                // Find the matching report data
                const reportData = reportedItems.find(item => item.title === title) || reportedItems[index];
                openReportModal(reportData);
            });
        });
        
        approveButtons.forEach((button) => {
            button.addEventListener('click', function() {
                const tableRow = this.closest('tr');
                if (confirm('Are you sure you want to approve this content?')) {
                    const statusBadge = tableRow.querySelector('.status-badge');
                    statusBadge.textContent = 'Approved';
                    statusBadge.classList.remove('status-flagged');
                    statusBadge.classList.add('status-published');
                    updateReportCounter(-1);
                }
            });
        });
        
        deleteButtons.forEach((button) => {
            button.addEventListener('click', function() {
                const tableRow = this.closest('tr');
                if (confirm('Are you sure you want to delete this content?')) {
                    tableRow.style.opacity = '0.5';
                    setTimeout(() => {
                        tableRow.remove();
                        updateReportCounter(-1);
                    }, 500);
                }
            });
        });
    }

    // Function to open report modal with dynamic content
    function openReportModal(reportData) {
        const reportModal = document.getElementById('reportModal');
        
        // Set modal content
        reportModal.querySelector('.modal-title').textContent = 'Review Reported Content';
        
        const modalBody = reportModal.querySelector('.modal-body');
        modalBody.innerHTML = `
            <div class="form-group">
                <div class="form-label">Content Title</div>
                <div>${reportData.title}</div>
            </div>
            <div class="form-group">
                <div class="form-label">Author</div>
                <div>${reportData.author}</div>
            </div>
            <div class="form-group">
                <div class="form-label">Content Preview</div>
                <div style="padding: 10px; background-color: #f9fafb; border-radius: 5px;">
                    ${reportData.content}
                </div>
            </div>
            <div class="form-group">
                <div class="form-label">Reported by</div>
                <div>${reportData.reporter}</div>
            </div>
            <div class="form-group">
                <div class="form-label">Reason for Report</div>
                <div>${reportData.reason}</div>
            </div>
            <div class="form-group">
                <div class="form-label">Moderation Decision</div>
                <div class="form-check">
                    <input type="radio" name="decision" id="approve" class="form-check-input">
                    <label for="approve">Approve Content (No violation found)</label>
                </div>
                <div class="form-check">
                    <input type="radio" name="decision" id="edit" class="form-check-input">
                    <label for="edit">Edit Content (Remove violations)</label>
                </div>
                <div class="form-check">
                    <input type="radio" name="decision" id="delete" class="form-check-input">
                    <label for="delete">Delete Content (Violates guidelines)</label>
                </div>
                <div class="form-check">
                    <input type="radio" name="decision" id="warn" class="form-check-input">
                    <label for="warn">Warn User (Issue warning only)</label>
                </div>
            </div>
            <div class="form-group">
                <div class="form-label">Moderator Notes</div>
                <textarea class="form-control" placeholder="Add notes about this moderation decision..."></textarea>
            </div>
            <div class="form-actions">
                <button class="btn btn-outline modal-close">Cancel</button>
                <button class="btn btn-primary" id="submitDecision">Submit Decision</button>
            </div>
        `;
        
        // Show modal
        reportModal.style.display = 'flex';
        
        // Add submit button functionality
        const submitBtn = modalBody.querySelector('#submitDecision');
        submitBtn.addEventListener('click', function() {
            const selectedDecision = modalBody.querySelector('input[name="decision"]:checked');
            if (!selectedDecision) {
                alert('Please select a moderation decision.');
                return;
            }
            
            alert(`Decision ${selectedDecision.id} submitted for "${reportData.title}"`);
            reportModal.style.display = 'none';
            updateReportCounter(-1);
        });
    }
    
    // Function to update report counter
    function updateReportCounter(change) {
        const reportCountElement = document.querySelector('.stat-card:nth-child(4) .stat-card-value');
        if (reportCountElement) {
            const currentCount = parseInt(reportCountElement.textContent);
            reportCountElement.textContent = currentCount + change;
        }
    }
    
    // Bulk action functionality in reported tab
    const bulkActionButton = document.querySelector('#reported .btn-primary');
    if (bulkActionButton) {
        bulkActionButton.addEventListener('click', function() {
            const checkedItems = document.querySelectorAll('#reported input[type="checkbox"]:checked');
            if (checkedItems.length === 0) {
                alert('Please select at least one item.');
                return;
            }
            
            const action = prompt('Select action (approve, delete, warn):');
            if (!action) return;
            
            const validActions = ['approve', 'delete', 'warn'];
            if (!validActions.includes(action.toLowerCase())) {
                alert('Invalid action. Please choose approve, delete, or warn.');
                return;
            }
            
            const confirmAction = confirm(`Are you sure you want to ${action} ${checkedItems.length} selected items?`);
            if (confirmAction) {
                checkedItems.forEach(item => {
                    if (item.closest('tr')) {
                        if (action.toLowerCase() === 'delete') {
                            item.closest('tr').style.opacity = '0.5';
                            setTimeout(() => {
                                item.closest('tr').remove();
                            }, 500);
                        } else {
                            const statusBadge = item.closest('tr').querySelector('.status-badge');
                            if (statusBadge) {
                                statusBadge.textContent = action === 'approve' ? 'Approved' : 'Warned';
                                statusBadge.classList.remove('status-flagged');
                                statusBadge.classList.add(action === 'approve' ? 'status-published' : 'status-draft');
                            }
                        }
                    }
                });
                
                updateReportCounter(-checkedItems.length);
                alert(`Successfully processed ${checkedItems.length} items.`);
            }
        });
    }
    
    // Add functionality for main table header checkbox to select all rows
    const headerCheckboxes = document.querySelectorAll('table thead input[type="checkbox"]');
    headerCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const tableBody = this.closest('table').querySelector('tbody');
            const rowCheckboxes = tableBody.querySelectorAll('input[type="checkbox"]');
            
            rowCheckboxes.forEach(rowCheckbox => {
                rowCheckbox.checked = this.checked;
            });
        });
    });
    
    // Search functionality for reported items
    const reportedSearchInput = document.querySelector('#reported .search-bar input');
    if (reportedSearchInput) {
        reportedSearchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const reportedTable = document.querySelector('#reported table tbody');
            const rows = reportedTable.querySelectorAll('tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
});