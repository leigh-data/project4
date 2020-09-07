document.addEventListener('DOMContentLoaded', () => {
  // Click handler for toggling edit panel
  const handleLinkClick = (e) => {
    e.preventDefault();
    cardContent = e.target.parentNode;
    cardText = cardContent.getElementsByClassName('card-text')[0];
    editForm = cardContent.getElementsByClassName('edit-form')[0];

    cardText.classList.toggle('hide');
    editForm.classList.toggle('hide');
  };

  // click handler for submitting an update.
  const handleFormSubmit = (e) => {
    e.preventDefault();

    const postId = e.target.dataset.postId;
    const content = e.target.content.value.trim();
    const csrftoken = Cookies.get('csrftoken');
    const link = e.target.parentNode.getElementsByClassName('card-link')[0];
    const textarea = e.target.getElementsByTagName('textarea')[0];
    const display = e.target.parentNode.getElementsByTagName('p')[0];
    const data = { content: content };

    // send the update if there is content
    if (content) {
      // Send request here
      fetch(`/api/posts/${postId}/`, {
        method: 'PUT',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json;charset=UTF-8',
        },
        body: JSON.stringify(data),
      })
        .then((res) => {
          // successful update actions: update display panel and display it
          display.innerHTML = content;
          textarea.style.borderColor = 'lightgray';
          link.click();
        })
        .catch((err) => console.log(err));
    } else {
      textarea.style.borderColor="red";
    }

  };

  // Click handler for liking/unliking
  const handleLikeClick = e => {
    const button = e.target;
    const postId = e.target.dataset.postId;
    const csrftoken = Cookies.get('csrftoken');
    const likeCount = e.target.parentNode.getElementsByClassName('like-count')[0]
    
    if (button.classList.contains('like')) {
      fetch(`/api/posts/${postId}/like/`, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json;charset=UTF-8',
        },
      });
      likeCount.innerHTML = parseInt(likeCount.innerHTML) - 1;
    } else {
      fetch(`/api/posts/${postId}/like/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json;charset=UTF-8',
        },
      });
      likeCount.innerHTML = parseInt(likeCount.innerHTML) + 1;
    }

    button.classList.toggle('like');
  }

  const handleFollowClick = e => {
    const button = e.target;
    const authorId = e.target.dataset.authorId;
    const csrftoken = Cookies.get('csrftoken');

    if (button.classList.contains('following')) {
      fetch(`/api/users/${authorId}/follow/`, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json;charset=UTF-8',
        },
      });
    } else {
      fetch(`/api/users/${authorId}/follow/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json;charset=UTF-8',
        },
      });
    }
      // Button display logic
      button.classList.toggle('following');
      button.classList.toggle('btn-success');
      button.classList.toggle('btn-danger');
      
      if (button.classList.contains('btn-danger')) {
        button.innerHTML = 'Unfollow';
      } else {
        button.innerHTML = 'Follow';
      }
  }

  const posts = document.getElementsByClassName('card-body');
  const followButton = document.getElementsByClassName('follow-button')[0];

  // add follow button handler if followButton exists
  if (followButton) {
    followButton.addEventListener('click', handleFollowClick);
  }

  // add event handlers to posts
  for (let i = 0; i < posts.length; i++) {
    let post = posts[i];
    let link = post.getElementsByClassName('card-link')[0];
    let form = post.getElementsByClassName('edit-form')[0];

    let likeButton = post.getElementsByClassName('like-button')[0];

    likeButton.addEventListener('click', handleLikeClick);

    if (link) {
      link.addEventListener('click', handleLinkClick);
      form.addEventListener('submit', handleFormSubmit);
    }
  }
});
