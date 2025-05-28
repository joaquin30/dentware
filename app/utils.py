def remove_csrf_token(form_data: dict):
    data = dict(form_data)
    if 'csrf_token' in data:
        del data['csrf_token']
    return data