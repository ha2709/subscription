
def format_paginated_response(items, total, page, page_size):
    return {
        'results': [
            {
                'id': row[0],
                'user_id': row[1],
                'created_at': row[2],
                'deleted_at': row[3],
            }
            for row in items
        ],
        'total': total,
        'page': page,
        'page_size': page_size
    }
