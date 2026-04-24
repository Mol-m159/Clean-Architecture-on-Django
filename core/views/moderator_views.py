"""
Moderator Views - панель модератора и очередь модерации
Соответствует старому moder.py
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator

from infrastructure.di_config import container
from .decorators import role_required


class ModeratorDashboardView(View):
    """Панель модератора"""
    
    @method_decorator(role_required(['moderator', 'admin']))
    def get(self, request):
        # Получаем очередь с приоритетами
        queue_result = container.get_queue_priority_uc.execute()
        
        # Преобразуем для шаблона
        moderation_queue = []
        for item in queue_result.high_priority + queue_result.medium_priority + queue_result.low_priority:
            moderation_queue.append({
                'entity_id': item.homebrew.entity_id,
                'entity_type': item.homebrew.entity_type.value,
                'author_id': item.homebrew.author_id,
                'created_date': item.homebrew.created_date,
                'days_in_queue': item.days_in_queue,
                'priority': item.priority.value,
            })
        
        context = {
            'moderation_queue': moderation_queue[:5],  # Первые 5 записей
            'queue_count': queue_result.total_count,
            'high_count': queue_result.high_count,
            'medium_count': queue_result.medium_count,
            'low_count': queue_result.low_count,
            'user_id': request.session.get('user_id'),
            'user_type': request.session.get('user_type'),
            'user_name': request.session.get('user_name'),
        }
        return render(request, 'moderator/dashboard.html', context)


class ModerationQueueView(View):
    """Полная очередь модерации"""
    
    @method_decorator(role_required(['moderator', 'admin']))
    def get(self, request):
        queue_result = container.get_queue_priority_uc.execute()
        
        moderation_queue = []
        for item in queue_result.high_priority + queue_result.medium_priority + queue_result.low_priority:
            moderation_queue.append({
                'entity_id': item.homebrew.entity_id,
                'entity_type': item.homebrew.entity_type.value,
                'author_id': item.homebrew.author_id,
                'created_date': item.homebrew.created_date,
                'days_in_queue': item.days_in_queue,
                'priority': item.priority.value,
            })
        
        context = {
            'queue': moderation_queue,
            'high_priority_count': queue_result.high_count,
            'medium_priority_count': queue_result.medium_count,
            'low_priority_count': queue_result.low_count,
            'user_id': request.session.get('user_id'),
            'user_type': request.session.get('user_type'),
            'user_name': request.session.get('user_name'),
        }
        return render(request, 'moderator/moderation_queue.html', context)


class ModerateItemView(View):
    """Страница модерации конкретного элемента"""
    
    @method_decorator(role_required(['moderator', 'admin']))
    def get(self, request, entity_id):
        # Получаем контент
        homebrew_result = container.get_homebrew_uc.execute(entity_id)
        
        if not homebrew_result.success:
            messages.error(request, f'Элемент #{entity_id} не найден')
            return redirect('moderation_queue')
        

        edit_history = container.homebrew_edit_reader.get_by_entity(entity_id)
        
        homebrew = homebrew_result.homebrew
        item = {
            'entity_id': homebrew.entity_id,
            'entity_type': homebrew.entity_type.value,
            'author_id': homebrew.author_id,
            'system_id': homebrew.system_id,
            'created_date': homebrew.created_date,
            'status': homebrew.status.value,
        }
        
        edit_history_list = []
        for e in edit_history:  # edit_history уже список
            edit_history_list.append({
                'edit_id': e.edit_id,
                'edit_date': e.edit_date,
                'version_number': e.version_number,
            })
        
        context = {
            'item': item,
            'edit_history': edit_history,
            'user_id': request.session.get('user_id'),
            'user_type': request.session.get('user_type'),
            'user_name': request.session.get('user_name'),
        }
        return render(request, 'moderator/moderate_item.html', context)
    
    @method_decorator(role_required(['moderator', 'admin']))
    def post(self, request, entity_id):
        decision = request.POST.get('decision')
        moderator_id = request.session.get('user_id')
        
        if decision == 'approved':
            result = container.approve_uc.execute(entity_id, moderator_id)
        elif decision == 'rejected':
            result = container.reject_uc.execute(entity_id, moderator_id)
        else:
            messages.error(request, 'Необходимо выбрать решение')
            return redirect('moderation_queue')
        
        if result.success:
            messages.success(request, f'Элемент {entity_id} успешно {decision}')
        else:
            messages.error(request, f'Ошибка при модерации: {result.error_message}')
        
        return redirect('moderation_queue')