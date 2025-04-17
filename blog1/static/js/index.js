document.addEventListener("DOMContentLoaded", function () {
    let page = 1;
    let loading = false;
    let blogsPerPage = 10;

    document.getElementById("load-more-btn").addEventListener("click", function () {
        if (loading) return;
        loading = true;

        fetch(`/load_trending_blogs?page=${page}&limit=${blogsPerPage}`)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    document.getElementById("load-more-btn").style.display = "none";
                    return;
                }

                const container = document.getElementById("trending-blogs-container");
                data.forEach(post => {
                    let article = document.createElement("article");
                    article.classList.add("bg-white", "p-6", "rounded-lg", "shadow-md", "hover:shadow-xl", "transition", "blog-card", "hover-scale");
                    article.innerHTML = `
                        <span class="text-4xl font-bold text-gray-200 mb-4 block">${page * blogsPerPage - blogsPerPage + (container.children.length + 1)}</span>
                        <div>
                            <div class="flex items-center mb-3">
                                <img src="${post.author_image}" alt="Author Image" class="w-8 h-8 rounded-full mr-2">
                                <div>
                                    <span class="font-medium block">${post.author}</span>
                                    <span class="text-gray-500 text-sm">${post.date}</span>
                                </div>
                            </div>
                            <h3 class="font-bold text-xl mb-3 hover:text-primary transition">${post.title}</h3>
                            <p class="text-gray-600 mb-4 line-clamp-2">${post.excerpt}</p>
                            <div class="flex items-center justify-between text-sm">
                                <span class="text-gray-500">${post.read_time} min read</span>
                                <div class="flex items-center space-x-2">
                                    <span class="text-gray-500">${post.likes} likes</span>
                                    <span>•</span>
                                    <span class="text-gray-500">${post.comments} comments</span>
                                </div>
                            </div>
                        </div>
                    `;
                    container.appendChild(article);
                });

                page++;
                loading = false;
            })
            .catch(error => {
                console.error("Error loading blogs:", error);
                loading = false;
            });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
      const alerts = document.querySelectorAll('.alert');
      alerts.forEach(function (alert) {
        if (bootstrap && bootstrap.Alert) {
          const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
          bsAlert.close();
        }
      });
    }, 4000); 
  });

