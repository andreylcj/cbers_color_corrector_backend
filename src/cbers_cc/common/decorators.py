

def log_details(text: str=None, omit_start: str=True, self_key_text: str=None):
    def wrapper0(f):
        def wrapper1(self, *args, **kwargs):
            _text = f'{text}...'
            if not omit_start:
                print(_text)
            response = f(self, *args, **kwargs)
            if self_key_text is not None:
                _text = getattr(self, self_key_text)
            else:
                _text = f'{_text} Done!'
            print(_text)
            return response
        return wrapper1
    return wrapper0