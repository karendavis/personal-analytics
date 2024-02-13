from data_loader import screen_time


def test_load_screen_time_data():
    data = screen_time.load_screen_time_data("test_data")
    assert data is not None