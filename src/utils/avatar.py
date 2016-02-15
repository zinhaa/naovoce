import os
import urllib.parse

import cairosvg

from django.core.cache import cache
from django.template import loader, Context
from django.conf import settings

from . import colors as col
from .full_url import get_full_url


AVATAR_SIZE_MIN = getattr(settings, 'AVATAR_SIZE_MIN', 20)
AVATAR_SIZE_MAX = getattr(settings, 'AVATAR_SIZE_MAX', 200)
AVATAR_SIZE_DEFAULT = getattr(settings, 'AVATAR_SIZE_DEFAULT', 60)
AVATARS_URL = getattr(settings, 'AVATARS_URL', 'avatars/')

AVATARS_PATH = str(os.path.join(settings.MEDIA_URL, AVATARS_URL))
AVATARS_ABS_PATH = str(os.path.join(settings.MEDIA_ROOT, AVATARS_URL))

if not os.path.exists(AVATARS_ABS_PATH):
    os.makedirs(AVATARS_ABS_PATH)


def get_avatar(request, user, size=None, bg_shade=0):
    if size is None:
        size = AVATAR_SIZE_DEFAULT
    else:
        size = int(size)
        if AVATAR_SIZE_MAX < size < AVATAR_SIZE_MIN:
            size = AVATAR_SIZE_DEFAULT

    filename = cache_key = '{pk:08d}-{size:03d}-{bg:03d}.png'.format(
        size=size,
        pk=user.pk,
        bg=int(bg_shade*100)
    )

    path = cache.get(cache_key)

    if not path:
        abs_path = AVATARS_ABS_PATH+filename
        path = AVATARS_PATH+filename

        if not os.path.isfile(abs_path):
            color = col.from_hex(user.hash[:6])

            template = loader.get_template('pickers/avatar.html')

            icon = template.render(Context({
                'size': size,
                'bg': color.complementary().shade(bg_shade).hexcode() if bg_shade else 0,
                'color': color.hexcode(),
            }))

            with open(abs_path, 'wb') as f:
                f.write(cairosvg.svg2png(bytestring=icon))

        cache.set(cache_key, path)

    return 'https://secure.gravatar.com/avatar/{hash}?{params}'.format(
        hash=user.hash,
        params=urllib.parse.urlencode({
            'd': get_full_url(request, path),
            's': str(size),
        }),
    )
