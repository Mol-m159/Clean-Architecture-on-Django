from typing import Dict, Any, List, Tuple, Optional
from django.db import connection


class PaginationHelper:
    """Пагинация SQL запросов (MS SQL Server)"""
    
    @staticmethod
    def get_paginated_data(
        base_query: str,
        params: List,
        page: int,
        per_page: int,
        order_by: str = "ORDER BY 1 DESC"
    ) -> Dict[str, Any]:
        """Выполняет запрос с пагинацией"""
        offset = (page - 1) * per_page
        
        with connection.cursor() as cursor:
            # Count query
            count_query = f"SELECT COUNT(*) FROM ({base_query}) AS subquery"
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]
            
            # Data query with pagination
            paginated_query = f"""
                {base_query}
                {order_by}
                OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """
            params_extended = params + [offset, per_page]
            cursor.execute(paginated_query, params_extended)
            
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return {
                'data': data,
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': (total + per_page - 1) // per_page
            }
    
    @staticmethod
    def build_where_clause(filters: Dict[str, Any], field_mapping: Dict[str, str]) -> Tuple[str, List]:
        """Строит WHERE clause из фильтров"""
        clauses = []
        params = []
        
        for filter_key, db_field in field_mapping.items():
            value = filters.get(filter_key)
            if value is not None:
                clauses.append(f"{db_field} = %s")
                params.append(value)
        
        if filters.get('date_from'):
            clauses.append("login_date >= %s")
            params.append(filters['date_from'])
        
        if filters.get('date_to'):
            clauses.append("login_date <= %s")
            params.append(filters['date_to'])
        
        if filters.get('active_only'):
            clauses.append("logout_date IS NULL")
        
        where_clause = " AND ".join(clauses) if clauses else "1=1"
        return where_clause, params


def dict_fetch_all(cursor) -> List[Dict]:
    """Преобразует cursor результат в список словарей"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]