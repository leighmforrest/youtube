from youtube.channels import (extract_channel_api_data,
                              extract_channel_statistics,
                              get_channel_data_from_api,
                              get_channel_statistics_from_api)


def test_get_channel_data_from_api(
    mock_response_channel_data, channel_data, test_handle
):
    results = get_channel_data_from_api(test_handle)
    test_channel_data = extract_channel_api_data(channel_data, test_handle)

    for key, value in results.items():
        assert results[key] == test_channel_data[key]


def test_get_channel_statistics_from_api(
    mock_response_channel_statistics, channel_statistics, test_handle
):
    results = get_channel_statistics_from_api(test_handle)
    test_channel_statistics = extract_channel_statistics(channel_statistics)

    for key, value in results.items():
        assert results[key] == test_channel_statistics[key]
