from data_loader import screen_time
from data_loader.screen_time import ScreenTimeItem

mock_screen_time_data = ScreenTimeItem(date='Today, 13 February',
                                       total_time='3h 19min.',
                                       applications={
                                            'Safari': '2h 49min.',
                                            'Messages': '13min.',
                                            'DuckDuckGo': '3min.'
                                       })

mock_test_data = ['10:00', '. atl > (_', 'Week Day', 'SCREEN TIME',
                  'Today, 16 February', '1 1 1 1 1 1 8h', '! — 0', 'M Tu Ww ‘Th F Sa Su', ', 60min.', '= 30min.',
                  "'12am ‘6am '12pm ‘6pm", 'Health & Fitness Social Education', 'Smin. Smin. 2min.',
                  'MOST USED SHOW CATEGORIES', 're) Safari', '1h 59min.', 'MyFitnessPal', '8min.', 'O Messages >',
                  '8min.', 'yy SChO0 kiiytGae N']


def test_load_screen_time_data():
    result = screen_time.load_screen_time_data("test_data/13_Feb_2024_at_10.png")
    assert result is not None
    assert result.date == mock_screen_time_data.date
    assert result.total_time == mock_screen_time_data.total_time
    assert result.applications == mock_screen_time_data.applications


def test_load_screen_time_data_with_different_file():
    result = screen_time.load_screen_time_data("test_data/16_Feb_2024_at_10.png")
    assert result is not None
    assert result.date == 'Today, 16 February'
    assert result.total_time == '1 1 1 1 1 1 8h'
    assert result.applications == {'re) Safari': '1h 59min.', '. MyFitnessPal': '8min.', 'O Messages >': '8min.'}


def test_create_screen_time_item_from_text():
    result = screen_time.create_screen_time_item_from_text(mock_test_data)
    assert result is not None
    assert result.date == 'Today, 16 February'
    assert result.total_time == '1 1 1 1 1 1 8h'
    assert result.applications == {'re) Safari': '1h 59min.',  'MyFitnessPal': '8min.', 'O Messages >': '8min.'}
