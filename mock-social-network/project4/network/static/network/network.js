document.addEventListener('DOMContentLoaded', function() {
  
  document.querySelectorAll('.follow-button').forEach(follow_user => {
    
    follow_user.addEventListener('click', function() {
      const user_to_follow = follow_user.dataset.usertofollow; // username
      const num_followers = document.querySelector(`.num-followers[data-puser="${user_to_follow}"]`);
      const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
      if(follow_user.innerHTML === "Follow User") {
        fetch(`/follow/${user_to_follow}`, {
          method: 'POST',
          headers: {
            "X-CSRFToken": token
          }
        })
        .then(response => {
          follow_user.innerHTML = "Unfollow User"; // change button's text 
          let my_num = parseInt(num_followers.innerHTML);
          my_num += 1;
          num_followers.innerHTML = my_num;
        });
      }
      else { // follow_user.innerHTML === "Unfollow User"
        //fetch request
        fetch(`/unfollow/${user_to_follow}`, {
          method: 'POST',
          headers: {
            "X-CSRFToken": token
          }
        })
        .then(response => {
          follow_user.innerHTML = "Follow User"; // change button's text
          let my_num = parseInt(num_followers.innerHTML);
          my_num -= 1;
          num_followers.innerHTML = my_num;
        });
      }
    })
  });

  document.querySelectorAll('.edit-button').forEach(edit => {
    edit.addEventListener('click', function() {
      const postId = edit.dataset.post;
      const area = document.querySelector(`.edit-area[data-post="${postId}"]`);
      const button = document.querySelector(`.edit-button[data-post="${postId}"]`);
      const content = document.querySelector(`.post-content[data-post="${postId}"]`);
 
      if (button.innerHTML === 'Edit') {
        area.value = content.innerHTML;
        area.style.display = 'block';
        content.style.display = 'none';
        button.innerHTML = 'Save';
      } else {
        const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        fetch(`/posts/${postId}/edit`, {
          method: 'PUT',
          body: JSON.stringify({
            content: area.value
          }),
          headers: {
            "X-CSRFToken": token
          }
        })
        .then(response => {
          content.innerHTML = area.value;
          area.style.display = 'none';
          content.style.display = 'block';
          button.innerHTML = 'Edit';
        });
      }
    })
  });

  document.querySelectorAll('.like-button').forEach(like => {
    like.addEventListener('click', function() {
      const postId = like.dataset.post;
      const button = document.querySelector(`.like-button[data-post="${postId}"]`);
      const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

      if (button.innerHTML === 'Like') {
        fetch(`/posts/${postId}/like`, {
          method: 'PUT',
          headers: {
            "X-CSRFToken": token
          }
        })
        .then(response => {
          button.innerHTML = 'Unlike';
        });
      } else {
        fetch(`/posts/${postId}/unlike`, {
          method: 'PUT',
          headers: {
            "X-CSRFToken": token
          }
        })
        .then(response => {
          button.innerHTML = 'Like';
        });
      }
    })
  });

});