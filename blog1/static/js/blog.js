// Sample article data (in practice, this would come from your backend)
const articleData = [
    {
        author: 'Emily Green',
        authorImage: '../static/images/download11.jpeg',
        publication: 'Sustainable Living',
        title: 'Urban Gardening: Transform Your Balcony Into a Green Paradise',
        content: 'Discover how to create a thriving garden in limited space. From choosing the right plants to setting up efficient irrigation systems, this guide will help you build your own urban oasis...',
        readTime: '8 min read',
        date: 'Feb 12',
        image: '../static/images/download12.jpeg'
    },
    {
        author: 'Michael Woods',
        authorImage: '../static/images/download13.jpeg',
        publication: 'Eco-Technology',
        title: 'Solar Power Revolution: The Future of Home Energy',
        content: 'With recent advancements in solar technology, powering your home with renewable energy has never been more accessible. Learn about the latest innovations and how to make the switch...',
        readTime: '10 min read',
        date: 'Feb 11',
        image: '../static/images/download14.jpeg'
    },
    {
        author: 'Sarah Forest',
        authorImage: '../static/images/download15.jpeg',
        publication: 'Mindful Living',
        title: 'The Art of Forest Bathing: Connecting with Nature',
        content: 'Explore the Japanese practice of shinrin-yoku (forest bathing) and its scientifically proven benefits for mental health, stress reduction, and overall well-being...',
        readTime: '6 min read',
        date: 'Feb 10',
        image: '../static/images/download16.jpeg'
    }
];

let page = 0;
let loading = false;
const articlesPerPage = 3;

function createArticleElement(article) {
    return `
        <article class="mb-12 fade-in">
            <div class="flex items-start mb-4">
               <div class="w-10 h-10 rounded-full bg-green-100 mr-3">
                    <img src="${article.authorImage}" alt="${article.author}" class="w-full h-full rounded-full">
                </div>
                <div>
                    <p class="font-medium">${article.author}</p>
                    <p class="text-gray-500 text-sm">in ${article.publication}</p>
                </div>
            </div>
            
            <div class="flex justify-between">
                <div class="flex-1 pr-8">
                    <h2 class="text-xl font-bold mb-2 hover:text-green-600">
                       <a href="${damonUrl}?article_id=${article.id}">${ article.title }</a>
                    </h2>
                    <p class="text-gray-600 mb-4">${article.content}</p>
                    <div class="flex items-center text-gray-500 text-sm">
                        <span>${article.readTime}</span>
                        <span class="mx-2">·</span>
                        <span>${article.date}</span>
                        <button class="ml-4 hover:text-green-600">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z" />
                            </svg>
                        </button>
                    </div>
                </div>
                <div class="w-32 h-32">
                    <img src="${article.image}" alt="${article.title}" class="w-full h-full object-cover rounded-lg">
                </div>
            </div>
        </article>
    `;
}

function loadMoreArticles() {
    if (loading) return;
    
    loading = true;
    const spinner = document.getElementById('loading-spinner');
    spinner.classList.remove('hidden');

    // Simulate API call delay
    setTimeout(() => {
        const container = document.getElementById('articles-container');
        const startIndex = page * articlesPerPage;
        const newArticles = articleData.map(createArticleElement).join('');
        
        if (page === 0) {
            container.innerHTML = newArticles;
        } else {
            container.insertAdjacentHTML('beforeend', newArticles);
        }

        page++;
        loading = false;
        spinner.classList.add('hidden');
    }, 1000);
}

// Initial load
loadMoreArticles();

// Infinite scroll handler
window.addEventListener('scroll', () => {
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 500) {
        loadMoreArticles();
    }
});