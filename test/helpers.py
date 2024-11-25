from test.factories import YouTubePlaylistItemFactory, YouTubePlaylistResponseFactory


def generate_paginated_responses(total_items=20, items_per_page=5):
    """
    Generate paginated videos responses simulating a real API pagination system.

    Args:
        total_items (int): Total number of items to simulate.
        items_per_page (int): Number of items per page.

    Returns:
        dict: A dictionary of paginated responses keyed by page tokens.
    """
    # Generate a consistent pool of items
    all_items = [YouTubePlaylistItemFactory() for _ in range(total_items)]

    # Calculate total pages
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # Create paginated responses
    responses = {}
    for page in range(total_pages):
        # Slice items for the current page
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
