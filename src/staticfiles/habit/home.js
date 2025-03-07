document.addEventListener('DOMContentLoaded', function() {
    // Удаляем существующие стили анимации, если они есть
    const existingAnimation = document.querySelector('#calendarAnimation');
    if (existingAnimation) {
        existingAnimation.remove();
    }

    // Удаляем анимацию с существующих успешных дней
    document.querySelectorAll('.bg-success').forEach(element => {
        element.style.animation = 'none';
        element.style.boxShadow = 'none';
    });

    const habitButtons = document.querySelectorAll('.habit-toggle');

    habitButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.disabled) return;
            this.disabled = true;

            const habitId = this.getAttribute('data-habit-id');
            
           
            const achievementIds = [];
            
            // Получаем ID всех карточек достижений
            const achievementCards = document.querySelectorAll('.achievement-card');
            achievementCards.forEach(card => {
                const achievementId = card.getAttribute('data-achievement-id');
                if (achievementId) {
                    achievementIds.push(achievementId);
                }
            });
            
            fetch(`/api/habits/${habitId}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': Cookies.get('csrftoken')
                },
                body: JSON.stringify({
                    achievement_ids: achievementIds
                })
            })
            .then(response => response.json())
            .then(data => {
                    console.log(data);  
                    // Находим родительский элемент привычки и плавно скрываем его
                    const habitElement = document.querySelector(`[data-habit-id="${habitId}"]`);
                    if (habitElement) {
                        habitElement.style.transition = 'all 0.3s ease';
                        habitElement.style.opacity = '0';
                        habitElement.style.transform  = 'translateX(20px)';
                        
                        setTimeout(() => {
                            habitElement.style.display = 'none';
                        }, 300);
                    }

                    // Обновляем счетчик серии
                    const streakElement = document.getElementById('streaks');
                    if (streakElement && data.streaks !== undefined) {
                        const currentStreak = parseInt(streakElement.textContent);
                        const newStreak = data.streaks;
                        
                        if (currentStreak !== newStreak) {
                            streakElement.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
                            streakElement.style.transform = 'translateY(-20px)';
                            streakElement.style.opacity = '0';
                            
                            
                            const currentDay = document.querySelector('.bg-secondary.bg-opacity-75');
                            if (currentDay) {
                                currentDay.style.transition = 'all 0.5s ease';
                                currentDay.classList.remove('bg-secondary', 'bg-opacity-75');
                                currentDay.classList.add('bg-success');
                                
                              
                                currentDay.style.boxShadow = '0 0 15px rgba(40, 167, 69, 0.5)';
                                setTimeout(() => {
                                    currentDay.style.boxShadow = 'none';
                                }, 500);
                            }
                            
                            setTimeout(() => {
                                streakElement.textContent = newStreak;
                                streakElement.style.transform = 'translateY(20px)';
                                
                                requestAnimationFrame(() => {
                                    streakElement.style.transform = 'translateY(0)';
                                    streakElement.style.opacity = '1';
                                });
                            }, 300);
                        }
                    }

                    // Обновляем достижения
                    if (data.achievements) {
                        Object.entries(data.achievements).forEach(([achievementId, achievement]) => {
                            const actualId = achievement.id;
                            const achievementCards = document.querySelectorAll(`[data-achievement-id="${actualId}"]`);
                            
                            achievementCards.forEach(card => {
                                const progressBar = card.querySelector('.progress-bar');
                                const isNextAchievement = card.id === 'nextAchievement';
                                const progressText = isNextAchievement ? 
                                    card.querySelector('small.text-white') : 
                                    card.querySelector('p.text-white');
                                
                               
                                const progress = parseFloat(achievement.progress);
                                if (progress >= 100) {
                                    // Анимация завершения достижения
                                    card.style.transition = 'all 0.3s ease';
                                    card.style.opacity = '0';
                                    
                                    setTimeout(() => {
                                        const progressContainer = card.querySelector('.flex-grow-1');
                                        const progressBarContainer = progressContainer.querySelector('.progress');
                                        const progressText = progressContainer.querySelector('#achievementProgress');
                                        
                                        if (progressBarContainer) progressBarContainer.remove();
                                        if (progressText) progressText.remove();
                                        
                                        const checkmark = document.createElement('div');
                                        checkmark.className = 'achievement-completed';
                                        checkmark.innerHTML = `
                                            <div class="d-flex align-items-center mt-2">
                                                <svg width="30" height="30" viewBox="0 0 40 40" class="me-2">
                                                    <circle cx="20" cy="20" r="19" fill="none" stroke="#28a745" stroke-width="2"/>
                                                    <path d="M10 20l7 7 13-13" fill="none" stroke="#28a745" stroke-width="3"/>
                                                </svg>
                                                <span class="text-success">Completed!</span>
                                            </div>
                                        `;
                                        progressContainer.appendChild(checkmark);
                                        
                                        card.style.opacity = '1';
                                    }, 300);
                                } else {
                                    card.style.transition = 'opacity 0.3s ease';
                                    card.style.opacity = '0';
                                    
                                    setTimeout(() => {
                                        if (progressBar) {
                                            // Убедимся, что progress содержит значение в процентах
                                            const progressValue = achievement.progress.toString();
                                            progressBar.style.width = progressValue.includes('%') ? progressValue : `${progressValue}%`;
                                            progressBar.setAttribute('aria-valuenow', parseFloat(progressValue));
                                        }
                                        
                                        if (progressText) {
                                            const currentValue = achievement.current_value;
                                            const targetValue = achievement.target_value;
                                            progressText.textContent = `${currentValue} / ${targetValue}`;
                                        }
                                        
                                        card.style.opacity = '1';
                                    }, 150);
                                }
                            });
                        });
                    } 
                }
            )
        
        });
    });

    // Добавляем обработчик для кнопки переключения достижений
    const toggleButton = document.getElementById('toggleAchievements');
    const achievementsSection = document.getElementById('allAchievements');
    const contentContainer = document.getElementById('content');
    
    if (toggleButton && achievementsSection) {
        toggleButton.addEventListener('click', function() {
            const isHidden = getComputedStyle(achievementsSection).display === 'none';
            const nextAchievement = document.getElementById('nextAchievement');
            const hideButton = document.getElementById('hideAchievements');
            const footer = document.querySelector('footer');
            const achievementsTitle = document.querySelector('.card-body h4');
            
            if (isHidden) {
                achievementsTitle.style.transition = 'opacity 0.3s ease';
                achievementsTitle.style.opacity = '0';
                setTimeout(() => {
                    achievementsTitle.textContent = 'Достижения';
                    achievementsTitle.style.opacity = '1';
                }, 150);

                achievementsSection.style.display = 'block';
                achievementsSection.style.opacity = '0';
                achievementsSection.style.transform = 'translateY(-10px)';
                
                contentContainer.classList.add('expanded-content');
                footer.style.transition = 'transform 0.3s ease';
                footer.style.transform = 'translateY(100px)'; 
                
                if (nextAchievement) {
                    const startRect = nextAchievement.getBoundingClientRect();
                    
                    achievementsSection.style.opacity = '1';
                    achievementsSection.style.transform = 'translateY(0)';
                    
                    const firstAchievement = achievementsSection.querySelector('.achievement-card');
                    const endRect = firstAchievement.getBoundingClientRect();
                    
                    achievementsSection.style.opacity = '0';
                    achievementsSection.style.transform = 'translateY(-10px)';
                    
                    
                    nextAchievement.style.transition = 'all 0.3s ease';
                    nextAchievement.style.position = 'relative';
                    nextAchievement.style.transform = `translate(${endRect.left - startRect.left}px, ${endRect.top - startRect.top}px)`;
                    nextAchievement.style.opacity = '0';
                    
                    setTimeout(() => {
                        nextAchievement.style.display = 'none';
                        
                        requestAnimationFrame(() => {
                            achievementsSection.style.transition = 'all 0.3s ease';
                            achievementsSection.style.opacity = '1';
                            achievementsSection.style.transform = 'translateY(0)';
                        });
                    }, 300);
                }
                
                toggleButton.style.opacity = '0';
                setTimeout(() => {
                    toggleButton.style.display = 'none';
                    hideButton.style.display = 'inline-block';
                    requestAnimationFrame(() => {
                        hideButton.style.opacity = '1';
                    });
                }, 150);
            }
        });

        const hideButton = document.getElementById('hideAchievements');
        if (hideButton) {
            hideButton.addEventListener('click', function() {
                const nextAchievement = document.getElementById('nextAchievement');
                const footer = document.querySelector('footer');
                const achievementsTitle = document.querySelector('.card-body h4');
                
                achievementsTitle.style.transition = 'opacity 0.3s ease';
                achievementsTitle.style.opacity = '0';
                setTimeout(() => {
                    achievementsTitle.textContent = 'Ближайшее достижение';
                    achievementsTitle.style.opacity = '1';
                }, 150);

                achievementsSection.style.transition = 'all 0.3s ease';
                achievementsSection.style.opacity = '0';
                achievementsSection.style.transform = 'translateY(-10px)';
                
                footer.style.transition = 'transform 0.3s ease';
                footer.style.transform = 'translateY(0)';
                
                if (nextAchievement) {
                    nextAchievement.style.display = 'block';
                    nextAchievement.style.opacity = '0';
                    nextAchievement.style.transform = 'none';
                    nextAchievement.style.position = 'static';
                    
                    setTimeout(() => {
                        nextAchievement.style.transition = 'all 0.3s ease';
                        nextAchievement.style.opacity = '1';
                    }, 10);
                }
                
                contentContainer.classList.remove('expanded-content');
                
                hideButton.style.opacity = '0';
                setTimeout(() => {
                    hideButton.style.display = 'none';
                    toggleButton.style.display = 'inline-block';
                    requestAnimationFrame(() => {
                        toggleButton.style.opacity = '1';
                    });
                }, 150);
                
                setTimeout(() => {
                    achievementsSection.style.display = 'none';
                }, 300);
            });
        }
    }

    animateFire();
});



// Анимация огня
function animateFire() {
    const fireIcon = document.querySelector('.fire-icon');
    if (!fireIcon) return;

    let time = 0;

    function animate() {
        time += 0.015;
        
        const scaleWave = Math.sin(time * 1.2) * 0.08; 
        const rotationWave = Math.sin(time * 1.5) * 0.8;
        const horizontalWave = Math.sin(time * 1.8) * 1;
        
        const secondaryScale = Math.sin(time * 2.2) * 0.05;
        const secondaryRotation = Math.cos(time * 2.5) * 0.5;
        
        const scale = 1.15 + scaleWave + secondaryScale; 
        const rotation = rotationWave + secondaryRotation;
        const translateX = horizontalWave;
        
        fireIcon.style.transform = `
            translate(${translateX}px, ${-scaleWave * 2}px)
            rotate(${rotation}deg)
            scale(${scale})
        `;
        
        const glowIntensity = 5 + Math.abs(Math.sin(time) * 4);
        const glowColor = `#ff${Math.floor(60 + Math.abs(Math.sin(time * 1.2) * 20)).toString(16)}00`;
        fireIcon.style.filter = `drop-shadow(0 0 ${glowIntensity}px ${glowColor})`;
        
        requestAnimationFrame(animate);
    }

    animate();
}