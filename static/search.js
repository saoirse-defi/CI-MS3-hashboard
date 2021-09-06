document.addEventListener('DOMContentLoaded', function() {
    var search_button = document.getElementById('search-submit');
    var loading = document.getElementsByClassName('loading');

    loading.style.display = 'none';

  });

search_button.addEventListener('click', () => {
    loading.style.display = 'block';
  });