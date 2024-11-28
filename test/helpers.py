from test.factories.videos import YouTubePlaylistItemFactory, YouTubePlaylistResponseFactory


def generate_paginated_responses(total_items=150, items_per_page=50):
    """Generate paginated responses simulating a real API pagination system.
    Returns a dictionary of paginated responses keyed by page tokens."""
    # generate a pool of items
    all_items = [YouTubePlaylistItemFactory() for _ in range(total_items)]

    # calculate total pages
    total_pages = (total_items + items_per_page - 1) // items_per_page

    responses = {}
    for page in range(total_pages):
        start_idx = page * items_per_page
        end_idx = start_idx + items_per_page
        page_items = all_items[start_idx:end_idx]

        # Generate a nextPageToken if there is another page
        next_page_token = f"page_{page + 1}" if page + 1 < total_pages else None

        # Create the response
        responses[f"page_{page}" if page > 0 else None] = (
            YouTubePlaylistResponseFactory(
                items=page_items,
                nextPageToken=next_page_token,
                pageInfo={
                    "totalResults": total_items,
                    "resultsPerPage": items_per_page,
                },
            )
        )
    
    return responses