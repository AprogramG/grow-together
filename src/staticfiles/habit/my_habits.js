document.addEventListener('DOMContentLoaded', function() {
    // Обработка кнопок редактирования
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const habitId = this.getAttribute('data-habit-id');
            const card = document.querySelector(`.card[data-habit-id="${habitId}"]`);
            const editMode = this.getAttribute('data-edit-mode') === 'true';
            
            const nameElement = card.querySelector('.habit-name');
            const descriptionElement = card.querySelector('.habit-description');
            const editForm = card.querySelector('.edit-form');
            const nameInput = editForm.querySelector('.name-input');
            const descriptionInput = editForm.querySelector('.description-input');

            if (!editMode) {
                nameElement.style.display = 'none';
                if (descriptionElement) {
                    descriptionElement.style.display = 'none';
                }
                editForm.classList.remove('d-none');
                this.innerHTML = '<i class="bi bi-check-lg"></i>';
                this.setAttribute('data-edit-mode', 'true');
            } else {
                const newName = nameInput.value.trim();
                const newDescription = descriptionInput.value.trim();

                if (newName) {
                    fetch(`/api/habits/${habitId}/`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': Cookies.get('csrftoken')
                        },
                        body: JSON.stringify({
                            name: newName,
                            description: newDescription
                        })
                    })
                    .then(response => {
                        if (response.ok) {
                            nameElement.textContent = newName;
                            if (descriptionElement) {
                                descriptionElement.textContent = newDescription;
                            }
                            
                            nameElement.style.display = 'block';
                            if (descriptionElement) {
                                descriptionElement.style.display = 'block';
                            }
                            editForm.classList.add('d-none');
                            this.innerHTML = '<i class="bi bi-pencil-square"></i>';
                            this.setAttribute('data-edit-mode', 'false');
                        }
                    });
                }
            }
        });
    });

    // Обработка подтверждения удаления
    document.querySelectorAll('.confirm-delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const habitId = this.getAttribute('data-habit-id');
            const modal = document.getElementById(`deleteModal${habitId}`);
            
            
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
            
            modal.addEventListener('hidden.bs.modal', function() {
                modal.removeAttribute('aria-hidden');
            }, { once: true });
            
            fetch(`/api/habits/${habitId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    
                    const card = document.querySelector(`.card[data-habit-id="${habitId}"]`).closest('.col-12');
                    card.remove();
                    
                    
                    modal.remove();
                    
                    
                    if (document.querySelectorAll('.card').length === 0) {
                        const container = document.getElementById('habits-list');
                        container.innerHTML = `
                            <div class="row">
                                <p class="text-center text-white fs-2">Вы ещё не создали ни одной привычки</p>
                                <div class="col-12 d-flex justify-content-center">
                                    <button class="btn btn-success" onclick="window.location.href='/habits/create/'">Создать привычку</button>
                                </div>
                            </div>
                        `;
                    }
                }
            });
        });
    });

    // Обработчик для модальных окон
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            
            document.activeElement.blur();
        });
        
        modal.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            }
        });
    });

  
}); 