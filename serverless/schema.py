from typing import List, Dict
INPUT_SCHEMA = {
    'query': {
        'type': str,
        'required': True
    },
    'candidates': {
        'type': List,
        'required': True,
    },
    'key_weights': {
        'type': Dict,
        'required': True
    }
}
