'''

'''


import os
import sys




if __name__ == "__main__":
    if not 'DJANGO_SETTINGS_MODULE' in os.environ:
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TwatBot.settings')
        from django.conf import settings
      
    from django.db import connection   
    import tweets.models