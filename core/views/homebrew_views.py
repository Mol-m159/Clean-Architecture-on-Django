from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json

from infrastructure.di_config import container
from .decorators import role_required


class HomebrewListView(View):
    """
    Список homebrew контента пользователя.
    Соответствует шаблону user/homebrew/list.html
    """
    
    @method_decorator(role_required(['user', 'moderator', 'admin']))
    def get(self, request):
        user_id = request.session.get('user_id')
        
        # Получаем контент пользователя
        result = container.get_user_homebrew_uc.execute(user_id)
        
        # Подсчет по статусам
        status_counts = {
            'approved': 0,
            'moderation': 0,
            'rejected': 0,
            'draft': 0,
        }
        
        # Получаем системы для формы создания
        systems_result = container.get_active_systems_uc.execute()
        systems = []
        if systems_result.success:
            systems = [
                {'system_id': s.system_id, 'name': f'System #{s.system_id}'}
                for s in systems_result.systems
            ]
        
        # Преобразуем для шаблона и считаем статусы
        homebrew_items = []
        for h in result.homebrew_items:
            view_count = container.homebrew_repository.get_view_count(h.entity_id)
            # Получаем количество версий через читатель
            edit_history = container.homebrew_edit_reader.get_by_entity(h.entity_id)
            version_count = len(edit_history) if edit_history else 1
            
            item = {
                'entity_id': h.entity_id,
                'author_id': h.author_id,
                'system_id': h.system_id,
                'entity_type': h.entity_type.value,
                'created_date': h.created_date,
                'status': h.status.value,
                'view_count': view_count,
                'version_count': version_count,
                'title': f"{h.entity_type.value} #{h.entity_id}",
                'description': None,
            }
            homebrew_items.append(item)
            status_counts[h.status.value] += 1
        
        context = {
            'homebrew_items': homebrew_items,
            'systems': systems,  # Для формы создания
            'total_count': len(homebrew_items),
            'approved_count': status_counts['approved'],
            'moderation_count': status_counts['moderation'],
            'rejected_count': status_counts['rejected'],
            'draft_count': status_counts['draft'],
            'user_id': user_id,
            'user_type': request.session.get('user_type'),
            'user_name': request.session.get('user_name'),
        }
        return render(request, 'user/homebrew/list.html', context)


class HomebrewDetailView(View):
    """
    Детальная информация о homebrew контенте.
    Соответствует шаблону user/homebrew/detail.html
    """
    
    @method_decorator(role_required(['user', 'moderator', 'admin']))
    def get(self, request, entity_id):
        user_id = request.session.get('user_id')
        user_type = request.session.get('user_type')

        # Получаем контент
        result = container.get_homebrew_uc.execute(entity_id)
        
        if not result.success:
            messages.error(request, result.error_message)
            return redirect('homebrew_list')
        
        homebrew = result.homebrew

        
        can_view_result = container.can_view_homebrew_uc.execute(
            user_id=user_id,
            user_role=user_type,
            homebrew=homebrew
        )
        
        if not can_view_result:
            messages.error(request, 'У вас нет доступа к этому контенту')
            return redirect('homebrew_list')

        
        # Получаем количество просмотров через репозиторий
        view_count = container.homebrew_repository.get_view_count(entity_id)
        
        # Получаем историю изменений через читатель
        edit_history = container.homebrew_edit_reader.get_by_entity(entity_id)
        
        edit_history_list = []
        for e in edit_history:
            edit_history_list.append({
                'edit_id': e.edit_id,
                'entity_id': e.entity_id,
                'edit_date': e.edit_date,
                'version_number': e.version_number,
            })
        
        # Получаем историю модерации через читатель
        moderation_history = container.moderation_reader.get_by_entity(entity_id)
        
        moderation_history_list = []
        for m in moderation_history:
            moderation_history_list.append({
                'moderation_id': m.moderation_id,
                'moderator_id': m.moderator_id,
                'entity_id': m.entity_id,
                'moderation_date': m.moderation_date,
                'old_status': m.old_status,
                'new_status': m.new_status,
            })
        
        # Цвета статусов для шаблона
        status_colors = {
            'approved': 'success',
            'moderation': 'warning',
            'rejected': 'danger',
            'draft': 'secondary'
        }
        
        context = {
            'homebrew': {
                'entity_id': homebrew.entity_id,
                'author_id': homebrew.author_id,
                'system_id': homebrew.system_id,
                'entity_type': homebrew.entity_type.value,
                'created_date': homebrew.created_date,
                'status': homebrew.status.value,
                'status_color': status_colors.get(homebrew.status.value, 'light'),
                'view_count': view_count,
                'title': f"{homebrew.entity_type.value} #{homebrew.entity_id}",
                'description': None,
                'content': None,
            },
            'edit_history': edit_history_list,
            'moderation_history': moderation_history_list,
            'user_id': user_id,
            'user_type': user_type,
            'user_name': request.session.get('user_name'),
        }
        return render(request, 'user/homebrew/detail.html', context)


# =============== API VIEWS (для вызовов из JavaScript) ===============

class HomebrewCreateAPIView(View):
    """Создание homebrew через API"""
    
    @method_decorator(role_required(['user', 'moderator', 'admin']))
    def post(self, request):
        user_id = request.session.get('user_id')
        
        try:
            data = json.loads(request.body) if request.body else {}
            system_id = data.get('system_id')
            entity_type = data.get('entity_type', 'other')
            
            if not system_id:
                return JsonResponse({'error': 'system_id required'}, status=400)
            
            result = container.create_homebrew_uc.execute(
                author_id=user_id,
                system_id=int(system_id),
                entity_type=entity_type
            )
            
            if result.success:
                return JsonResponse({
                    'success': True,
                    'entity_id': result.homebrew.entity_id,
                    'message': 'Контент создан'
                }, status=201)
            else:
                return JsonResponse({'error': result.error_message}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class HomebrewUpdateAPIView(View):
    @method_decorator(role_required(['user', 'moderator', 'admin']))
    def post(self, request, entity_id):
        user_id = request.session.get('user_id')
        
        try:
            data = json.loads(request.body) if request.body else {}
            
            update_data = {}
            
            if 'system_id' in data and data['system_id']:
                update_data['new_system_id'] = int(data['system_id'])
            
            if 'entity_type' in data and data['entity_type']:
                # Сохраняем как есть, Use Case сам преобразует через from_string
                update_data['new_entity_type'] = data['entity_type']
            
            if not update_data:
                return JsonResponse({'error': 'Нет данных для обновления'}, status=400)
            
            homebrew_result = container.get_homebrew_uc.execute(entity_id)
            if not homebrew_result.success:
                return JsonResponse({'error': 'Контент не найден'}, status=404)
            
            if homebrew_result.homebrew.author_id != user_id:
                return JsonResponse({'error': 'Нет прав для редактирования'}, status=403)
            
            result = container.update_homebrew_uc.execute(
                entity_id=entity_id,
                **update_data
            )
            
            if result.success:
                response_data = {
                    'success': True,
                    'entity_id': entity_id,
                    'message': 'Контент обновлен'
                }
                
                if hasattr(result, 'status_changed') and result.status_changed:
                    response_data['status_changed'] = True
                    response_data['new_status'] = 'draft'
                    response_data['message'] = 'Статус изменен на "Черновик"'
                
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': result.error_message}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class HomebrewSubmitAPIView(View):
    """Отправка homebrew на модерацию"""
    
    @method_decorator(role_required(['user', 'moderator', 'admin']))
    def post(self, request, entity_id):
        user_id = request.session.get('user_id')
        
        try:
            # Проверяем, что пользователь владеет контентом
            homebrew_result = container.get_homebrew_uc.execute(entity_id)
            if not homebrew_result.success:
                return JsonResponse({'error': 'Контент не найден'}, status=404)
            
            if homebrew_result.homebrew.author_id != user_id:
                return JsonResponse({'error': 'Нет прав для отправки на модерацию'}, status=403)
            
            # Отправляем на модерацию
            result = container.submit_moderation_uc.execute(entity_id)
            
            if result.success:
                return JsonResponse({
                    'success': True,
                    'entity_id': entity_id,
                    'status': 'moderation',
                    'message': 'Контент отправлен на модерацию'
                })
            else:
                return JsonResponse({'error': result.error_message}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class HomebrewDeleteAPIView(View):
    """Удаление homebrew"""
    
    @method_decorator(role_required(['user', 'moderator', 'admin']))
    def delete(self, request, entity_id):
        user_id = request.session.get('user_id')
        
        try:
            # Проверяем, что пользователь владеет контентом
            homebrew_result = container.get_homebrew_uc.execute(entity_id)
            if not homebrew_result.success:
                return JsonResponse({'error': 'Контент не найден'}, status=404)
            
            if homebrew_result.homebrew.author_id != user_id:
                return JsonResponse({'error': 'Нет прав для удаления'}, status=403)
            
            # Удаляем
            result = container.delete_homebrew_uc.execute(entity_id)
            
            if result.success:
                return JsonResponse({
                    'success': True,
                    'entity_id': entity_id,
                    'message': 'Контент удален'
                })
            else:
                return JsonResponse({'error': result.error_message}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)