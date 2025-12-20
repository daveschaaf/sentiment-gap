MIN_CHAR_LENGTH = 3

REVIEW_DATA_TYPES = {
    'rating': 'float32',
    'title': 'string',
    'text': 'string',
    'asin': 'category',
    'parent_asin': 'category',
    'user_id': 'string',
    'helpful_vote': 'int32', 
    'verified_purchase': 'bool',
    'images': 'object'
}

META_DATA_TYPES = {
    'parent_asin': 'category',
    'title': 'string',
    'description': 'string', 
    'features': 'object',
    'average_rating': 'float32',
    'rating_number': 'int32',
    'images': 'object',
    'videos': 'object'
}


