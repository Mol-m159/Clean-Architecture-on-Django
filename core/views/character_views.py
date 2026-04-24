# user/views/character_views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json

from infrastructure.di_config import container
from .decorators import role_required


class CharacterListView(View):
    """Список персонажей пользователя"""
    
    @method_decorator(role_required(['user', 'moderator', 'admin']))
    def get(self, request):
        user_id = request.session.get('user_id')
        
        result = container.get_user_characters_uc.execute(user_id)
        
        characters = []
        if result.success:
            for char in result.characters:
                characters.append({
                    'character_id': char.character_id,
                    'user_id': char.user_id,
                    'system_id': char.system_id,
                    'created_date': char.created_date,
                    'last_modified_date': char.last_modified_date,
                })
        
        # Получаем системы для формы создания
        systems_result = container.get_active_systems_uc.execute()
        systems = []
        if systems_result.success:
            systems = [
                {'system_id': s.system_id, 'name': f'System #{s.system_id}'}
                for s in systems_result.systems
            ]
        
        context = {
            'characters': characters,
            'systems': systems,  # Нужно для модального окна
            'character_count': len(characters),
            'user_id': user_id,
            'user_type': request.session.get('user_type'),
            'user_name': request.session.get('user_name'),
        }
        return render(request, 'user/characters/list.html', context)


class CharacterDetailView(View):
    """Детальная информация о персонаже"""
    
    @method_decorator(role_required(['user', 'moderator', 'admin']))
    def get(self, request, character_id):
        user_id = request.session.get('user_id')
        user_type = request.session.get('user_type')
        
        result = container.get_character_uc.execute(character_id)
        
        if not result.success:
            messages.error(request, result.error_message or 'Персонаж не найден')
            return redirect('character_list')
        
        character = result.character
        
        if character.user_id != user_id and user_type not in ['moderator', 'admin']:
            messages.error(request, 'У вас нет доступа к этому персонажу')
            return redirect('character_list')
        
        history_result = container.get_character_edits_uc.execute(character_id)
        
        edit_history = []
        if history_result.success:
            edit_history = [
                {'edit_date': edit.edit_date, 'edit_type': edit.edit_type}
                for edit in history_result.edits
            ]
        
        context = {
            'character': {
                'character_id': character.character_id,
                'user_id': character.user_id,
                'system_id': character.system_id,
                'created_date': character.created_date,
                'last_modified_date': character.last_modified_date,
            },
            'edit_history': edit_history,
            'user_id': user_id,
            'user_type': user_type,
            'user_name': request.session.get('user_name'),
        }
        return render(request, 'user/characters/detail.html', context)


# =============== API VIEWS (для вызовов из JavaScript) ===============

class CharacterCreateAPIView(View):
    """Создание персонажа через API"""
    
    @method_decorator(role_required(['user', 'moderator', 'admin']))
    def post(self, request):
        user_id = request.session.get('user_id')
        
        try:
            data = json.loads(request.body) if request.body else {}
            system_id = data.get('system_id')
            
            if not system_id:
                return JsonResponse({'error': 'system_id required'}, status=400)
            
            result = container.create_character_uc.execute(
                user_id=user_id,
                system_id=int(system_id)
            )
            
            if result.success:
                return JsonResponse({
                    'success': True,
                    'character_id': result.character.character_id,
                    'message': 'Персонаж создан'
                }, status=201)
            else:
                return JsonResponse({'error': result.error_message}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class CharacterUpdateAPIView(View):
    """Обновление персонажа через API"""
    
    @method_decorator(role_required(['user', 'moderator', 'admin']))
    def post(self, request, character_id):  # POST для простоты, можно и PUT
        user_id = request.session.get('user_id')
        
        try:
            data = json.loads(request.body) if request.body else {}
            new_system_id = data.get('system_id')
            
            if not new_system_id:
                return JsonResponse({'error': 'system_id required'}, status=400)
            
            result = container.update_character_uc.execute(
                character_id=character_id,
                user_id=user_id,
                new_system_id=int(new_system_id)
            )
            
            if result.success:
                return JsonResponse({
                    'success': True,
                    'character_id': character_id,
                    'message': 'Персонаж обновлен'
                })
            else:
                return JsonResponse({'error': result.error_message}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class CharacterDeleteAPIView(View):
    """Удаление персонажа через API"""
    
    @method_decorator(role_required(['user', 'moderator', 'admin']))
    def post(self, request, character_id):  # POST для простоты
        user_id = request.session.get('user_id')
        
        try:
            result = container.delete_character_uc.execute(character_id, user_id)
            
            if result.success:
                return JsonResponse({
                    'success': True,
                    'character_id': character_id,
                    'message': 'Персонаж удален'
                })
            else:
                return JsonResponse({'error': result.error_message}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)