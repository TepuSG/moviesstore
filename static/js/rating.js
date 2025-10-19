document.addEventListener('DOMContentLoaded', function() {
  // Initialize display stars based on data-rating attribute
  document.querySelectorAll('.stars-display').forEach(function(display){
    const rating = parseFloat(display.getAttribute('data-rating')) || 0;
    const stars = display.querySelectorAll('.star');
    stars.forEach(function(star){
      const value = parseInt(star.getAttribute('data-value'));
      if (value <= Math.round(rating)) {
        star.classList.add('filled');
      }
    });
  });

  // Rating widget interaction for logged-in users
  document.querySelectorAll('.rating-widget').forEach(function(widget){
    const movieId = widget.getAttribute('data-movie-id');
    const stars = widget.querySelectorAll('.star-input');
    const status = widget.querySelector('.rating-status');

    function clearHover() {
      stars.forEach(s => s.classList.remove('hover'));
    }

    stars.forEach(function(star){
      star.addEventListener('mouseover', function(){
        clearHover();
        const v = parseInt(star.getAttribute('data-value'));
        stars.forEach(function(s){
          if (parseInt(s.getAttribute('data-value')) <= v) s.classList.add('hover');
        });
      });
      star.addEventListener('mouseout', function(){
        clearHover();
      });
      star.addEventListener('click', function(){
        const value = star.getAttribute('data-value');
        // Send AJAX POST to submit rating
        fetch(`/${movieId}/rating/submit/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: `rating=${value}`
        }).then(res => res.json())
          .then(data => {
            if (data.success) {
              // update status text
              status.innerHTML = `<small class="text-success">You rated this movie ${data.user_rating}/5 stars</small>`;
              // update display stars
              document.querySelectorAll('.stars-display').forEach(function(display){
                const stars = display.querySelectorAll('.star');
                stars.forEach(function(s){
                  s.classList.toggle('filled', parseInt(s.getAttribute('data-value')) <= Math.round(data.average_rating));
                });
              });
              // update rating count and text if present
              const ratingText = document.querySelector('.rating-text');
              if (ratingText) {
                ratingText.innerText = `${data.average_rating}/5 (${data.rating_count} rating${data.rating_count == 1 ? '' : 's'})`;
              }
            } else if (data.error) {
              status.innerHTML = `<small class="text-danger">${data.error}</small>`;
            }
          }).catch(err => {
            status.innerHTML = `<small class="text-danger">Network error</small>`;
          });
      });
    });
  });

  // helper: getCookie (from Django docs)
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});