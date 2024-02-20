import pytest

from data_loader.screen_time import ScreenTimeItem, ApplicationItem, load_screen_time_item, \
    load_screen_time_data, create_screen_time_item_from_text, FolderDoesNotExistError

mock_screen_time_data = ScreenTimeItem(date='Today, 13 February',
                                       total_time='3h 19min.',
                                       applications=[ApplicationItem(application_name='Safari',
                                                                     application_time='2h 49min.'),
                                                     ApplicationItem(application_name='Messages',
                                                                     application_time='13min.'),
                                                     ApplicationItem(application_name='DuckDuckGo',
                                                                     application_time='3min.')]
                                       )

mock_screen_time_data_again = ScreenTimeItem(date='Today, 16 February',
                                             total_time='1 1 1 1 1 1 8h',
                                             applications=[ApplicationItem(application_name='re) Safari',
                                                                           application_time='1h 59min.'),
                                                           ApplicationItem(application_name='. MyFitnessPal',
                                                                           application_time='8min.'),
                                                           ApplicationItem(application_name='O Messages >',
                                                                           application_time='8min.')]
                                             )

mock_test_data = ['10:00', '. atl > (_', 'Week Day', 'SCREEN TIME',
                  'Today, 16 February', '1 1 1 1 1 1 8h', '! — 0', 'M Tu Ww ‘Th F Sa Su', ', 60min.', '= 30min.',
                  "'12am ‘6am '12pm ‘6pm", 'Health & Fitness Social Education', 'Smin. Smin. 2min.',
                  'MOST USED SHOW CATEGORIES', 're) Safari', '1h 59min.', '. MyFitnessPal', '8min.', 'O Messages >',
                  '8min.', 'yy SChO0 kiiytGae N']

folder_path = "test_data"


def test_load_screen_time_data():
    results = load_screen_time_data(folder_path)
    assert results.shape == (2, 8)


def test_load_screen_time_data_with_invalid_folder_path():
    fake_folder = "FakeFolder"
    with pytest.raises(FolderDoesNotExistError) as excinfo:
        results = load_screen_time_data(fake_folder)
    assert str(excinfo.value) == f"Folder `{fake_folder}` does not exist"


def test_load_screen_time_item():
    result = load_screen_time_item(f"{folder_path}/13_Feb_2024_at_10.png")
    assert result is not None
    assert result.date == mock_screen_time_data.date
    assert result.total_time == mock_screen_time_data.total_time
    assert result.applications == mock_screen_time_data.applications


def test_load_screen_time_item_with_different_file():
    result = load_screen_time_item(f"{folder_path}/16_Feb_2024_at_10.png")
    assert result is not None
    assert result.date == mock_screen_time_data_again.date
    assert result.total_time == mock_screen_time_data_again.total_time
    assert result.applications == mock_screen_time_data_again.applications


def test_create_screen_time_item_from_text():
    result = create_screen_time_item_from_text(mock_test_data)
    assert result is not None
    assert result.date == mock_screen_time_data_again.date
    assert result.total_time == mock_screen_time_data_again.total_time
    assert result.applications == mock_screen_time_data_again.applications
