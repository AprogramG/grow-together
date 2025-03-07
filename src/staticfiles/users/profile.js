document.addEventListener('DOMContentLoaded', function() {
	// Обработчик для кнопки подписки
	const followButton = document.getElementById('followButton');
	if (followButton) {
		followButton.addEventListener('click', async function() {
			const userId = this.dataset.userId;
			
			try {
				const response = await fetch(`/accounts/api/follow/${userId}/`, {
					method: 'PATCH',
					headers: {
						'X-CSRFToken': Cookies.get('csrftoken'),
						'Content-Type': 'application/json'
					}
				});

				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}

				if (response.status === 201) { 
					this.textContent = 'Отписаться';
				} else if (response.status === 204) { 
					this.textContent = 'Подписаться';
				}
				
			} catch (error) {
				console.error('Ошибка:', error);
				alert('Произошла ошибка при обновлении подписки');
			}
		});
	}

	
	const editBtn = document.getElementById('edit_profile');
	if (editBtn) {
		let isEditing = false;
		
		let currentDesc, currentName, currentEmail, currentAbout;
		
		editBtn.addEventListener('click', async function() {
			if (!isEditing) {
				isEditing = true;
				editBtn.textContent = 'Save';
				editBtn.classList.remove('btn-outline-light');
				editBtn.classList.add('btn-success');
				
				// Сохраняем текущие значения
				currentDesc = descValue.textContent.trim();
				currentName = nameValue.textContent.trim(); 
				currentEmail = emailValue.textContent.trim();
				currentAbout = aboutMe.textContent.trim();
				
				// Заменяем текст на поля ввода
				if (!descValue.querySelector('textarea')) {
					descValue.innerHTML = `<textarea class="form-control bg-dark text-white text-center w-75 fs-4" rows="3">${currentDesc}</textarea>`;
				}
				if (!nameValue.querySelector('input')) {
					nameValue.innerHTML = `<input type="text" class="form-control bg-dark text-white w-50" value="${currentName}">`;
				}
				if (!emailValue.querySelector('input')) {
					emailValue.innerHTML = `<input type="email" class="form-control bg-dark text-white w-50" value="${currentEmail}">`;
				}
				if (!aboutMe.querySelector('input')) {
					aboutMe.innerHTML = `<input type="text" class="form-control bg-dark text-white text-center " value="${currentAbout}">`;
				}
			} else {
				isEditing = false;
				editBtn.textContent = 'Edit';
				editBtn.classList.remove('btn-success');
				editBtn.classList.add('btn-outline-light');
				
				
				const newDesc = descValue.querySelector('textarea').value;
				const newName = nameValue.querySelector('input').value;
				const newEmail = emailValue.querySelector('input').value;
				const newAbout = aboutMe.querySelector('input').value;
				
				try {
					// Отправляем запрос на обновление на сервер
					const response = await fetch('/api/update-profile', {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
							'X-CSRFToken': Cookies.get('csrftoken')
						},
						body: JSON.stringify({
							description: newDesc,
							fullName: newName,
							email: newEmail,
							about_me: newAbout
						})
					});

					if (!response.ok) {
						throw new Error('Failed to update profile');
					}

					descValue.textContent = newDesc;
					nameValue.textContent = newName;
					emailValue.textContent = newEmail;
					aboutMe.textContent = newAbout;
				} catch (error) {
					descValue.textContent = currentDesc;
					nameValue.textContent = currentName;
					emailValue.textContent = currentEmail;
					aboutMe.textContent = currentAbout;
				}
			}
		});
	}
	
});