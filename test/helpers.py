from youtube.request import get_cache_key, get_full_url

generate_cache_key = lambda url, params: get_cache_key(get_full_url(url, params))
