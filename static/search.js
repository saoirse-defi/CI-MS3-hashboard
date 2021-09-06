document.addEventListener('DOMContentLoaded', function() {
    const search_button = document.getElementById('search-submit');
    const loading = document.getElementById('loading');

    search_button.addEventListener('click', () => {
      loading.style.display = 'flex';
    });
    
  });

  