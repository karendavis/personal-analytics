from data_loader import screen_time
from data_loader.screen_time import ScreenTimeItem

mock_screen_time_data = ScreenTimeItem(date='Today, 13 February',
                                       total_time='3h 19min.',
                                       applications={
                                            'Safari': '2h 49min.',
                                            'Messages': '13min.',
                                            'DuckDuckGo': '3min.'
                                       })


def test_load_screen_time_data():
    result = screen_time.load_screen_time_data("test_data/13_Feb_2024_at_10.png")
    assert result is not None
    assert result == mock_screen_time_data
