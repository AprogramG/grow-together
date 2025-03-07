   // Добавляем стили для эффекта наведения
   const style = document.createElement('style');
   style.textContent = `
       .hover-success:hover {
           color: #198754 !important;
           border-color: #198754 !important;
       }
   `;
   document.head.appendChild(style);
   
   const postLikes = document.querySelectorAll('#postLike');
   postLikes.forEach(like => {
       like.addEventListener('click', () => {
           const postId = like.getAttribute('data-post-id');
           console.log(postId);
           fetch(`/community/api/like/${postId}/`, {
               method: 'PATCH',
               headers: {
                   'Content-Type': 'application/json',
                   'X-CSRFToken': Cookies.get('csrftoken')
               }
           })
           .then(response => response.json())
           .then(data => {
               console.log(data);
               like.innerHTML = `
                  ${data.like} <i class="bi bi-heart"></i>
               `;
           });
       });
   });
   const comment = document.querySelectorAll('#postComment');
   comment.forEach(comment => {
       comment.addEventListener('click', () => {
           const postId = comment.getAttribute('data-post-id');
           
           const commentForm = document.createElement('div');
           commentForm.className = 'mt-3';
           commentForm.innerHTML = `
               <div class="input-group">
                   <textarea class="form-control bg-success bg-opacity-10 text-white" placeholder="Write a comment..."></textarea>
                   <button class="btn btn-outline-light" type="button" id="submitComment">Post</button>
               </div>
           `;
           
           comment.parentNode.insertBefore(commentForm, comment.nextSibling);
           
           // Обрабатываем отправку комментария
           const submitBtn = commentForm.querySelector('#submitComment');
           const textarea = commentForm.querySelector('textarea');
           
           submitBtn.addEventListener('click', () => {
               fetch(`/community/api/comment/${postId}/`, {
                   method: 'POST',
                   headers: {
                       'Content-Type': 'application/json',
                       'X-CSRFToken': Cookies.get('csrftoken')
                   },
                   body: JSON.stringify({
                       content: textarea.value
                   })
               })
               .then(response => {
                   if(response.ok) {
                       commentForm.remove();
                   }
               });
           });
       });
   });
   
   // Обновляем обработчик переключения комментариев
   const toggleButtons = document.querySelectorAll('.toggle-comments');
   toggleButtons.forEach(button => {
       button.addEventListener('click', () => {
           const postId = button.getAttribute('data-post-id');
           const commentsSection = document.getElementById(`comments-${postId}`);
           
           commentsSection.classList.toggle('show');
           const isVisible = commentsSection.classList.contains('show');
           
           button.innerHTML = isVisible ? 
               '<i class="bi bi-chevron-up"></i> Скрыть комментарии' : 
               '<i class="bi bi-chevron-down"></i> Показать комментарии';
       });
   });

   // Добавляем обработку формы комментария
   document.querySelectorAll('.comments-section').forEach(section => {
       const textarea = section.querySelector('textarea');
       const buttonsDiv = section.querySelector('.d-flex.justify-content-end');
       const submitButton = section.querySelector('.submit-comment');
       const postId = section.id.split('-')[1];
       
       const userAvatar = section.getAttribute('data-user-avatar');
       const username = section.getAttribute('data-username');

       textarea.addEventListener('focus', () => {
           buttonsDiv.style.display = 'flex';
       });

       textarea.addEventListener('input', () => {
           submitButton.disabled = !textarea.value.trim();
       });

       submitButton.addEventListener('click', () => {
           const content = textarea.value.trim();
           if (!content) return;

           fetch(`/community/api/comment/${postId}/`, {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json',
                   'X-CSRFToken': Cookies.get('csrftoken')
               },
               body: JSON.stringify({
                   content: content
               })
           })
           .then(response => response.json())
           .then(data => {
               const commentElement = document.createElement('div');
               commentElement.className = 'd-flex mb-2 new-comment-animation';
               
               const avatarHTML = userAvatar ? 
                   `<img src="${userAvatar}" alt="avatar" class="rounded-circle" style="width: 30px; height: 30px; object-fit: cover;">` :
                   username.charAt(0).toUpperCase();

               commentElement.innerHTML = `
                   <div class="rounded-circle bg-light text-dark d-flex align-items-center justify-content-center me-2" style="width: 30px; height: 30px;">
                       ${avatarHTML}
                   </div>
                   <div class="bg-light bg-opacity-25 rounded p-2">
                       <small class="text-white">${username}</small>
                       <p class="text-white-50 mb-0">${content}</p>
                   </div>
               `;

               const commentsSection = document.getElementById(`comments-${postId}`);
               
               const noCommentsHeader = commentsSection.querySelector('h6');
               if (noCommentsHeader && noCommentsHeader.textContent === 'Комментариев пока нет') {
                   noCommentsHeader.textContent = 'Комментарии';
               }

               const header = commentsSection.querySelector('h6');
               if (header) {
                   header.after(commentElement);
               } else {
                   commentsSection.appendChild(commentElement);
               }

               textarea.value = '';
               submitButton.disabled = true;
               submitButton.parentElement.style.display = 'none';
           })
           .catch(error => {
               console.error('Error:', error);
           });
       });
   });

   document.querySelectorAll('.edit-post-btn').forEach(button => {
       button.addEventListener('click', () => {
           const postId = button.getAttribute('data-post-id');
           
           document.getElementById(`postTitle-${postId}`).style.display = 'none';
           document.getElementById(`postContent-${postId}`).style.display = 'none';
           document.querySelectorAll(`.edit-form-${postId}`).forEach(el => {
               el.style.display = 'block';
           });
           
           document.querySelector(`.edit-buttons-${postId}`).style.display = 'none';
       });
   });

   document.querySelectorAll('.cancel-edit-btn').forEach(button => {
       button.addEventListener('click', () => {
           const postId = button.getAttribute('data-post-id');
           
           document.getElementById(`postTitle-${postId}`).style.display = 'block';
           document.getElementById(`postContent-${postId}`).style.display = 'block';
           document.querySelectorAll(`.edit-form-${postId}`).forEach(el => {
               el.style.display = 'none';
           });
           
           document.querySelector(`.edit-buttons-${postId}`).style.display = 'block';
       });
   });

   // Обработка сохранения изменений
   document.querySelectorAll('.save-edit-btn').forEach(button => {
       button.addEventListener('click', () => {
           const postId = button.getAttribute('data-post-id');
           const title = document.getElementById(`editTitle-${postId}`).value;
           const content = document.getElementById(`editContent-${postId}`).value;
           
           fetch(`/community/api/post/${postId}/`, {
               method: 'PUT',
               headers: {
                   'Content-Type': 'application/json',
                   'X-CSRFToken': Cookies.get('csrftoken')
               },
               body: JSON.stringify({
                   title: title,
                   content: content
               })
           })
           .then(response => {
               if (response.status === 200) {
                   window.location.reload();
               }
           });
       });
   });

   // Обработка подтверждения удаления
   document.querySelectorAll('.confirm-delete-btn').forEach(button => {
       button.addEventListener('click', () => {
           const postId = button.getAttribute('data-post-id');
           
           fetch(`/community/api/post/${postId}/`, {
               method: 'DELETE',
               headers: {
                   'X-CSRFToken': Cookies.get('csrftoken')
               }
           })
           .then(response => {
               if (response.status === 204) {
                   window.location.reload();
               }
           });
       });
   });