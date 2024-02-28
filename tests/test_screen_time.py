import pytest
import pathlib

from data_loader.screen_time import ScreenTimeItem, ApplicationItem, load_screen_time_item, \
    load_screen_time_data, create_screen_time_item_from_text, FolderDoesNotExistError, create_application_item_from_text

mock_screen_time_data = ScreenTimeItem(day='13',
                                       month='February',
                                       year='2024',
                                       total_hour=3,
                                       total_min=19,
                                       applications=[ApplicationItem(application_name='Safari',
                                                                     application_hour=2,
                                                                     application_min=49),
                                                     ApplicationItem(application_name='Messages',
                                                                     application_hour=0,
                                                                     application_min=13),
                                                     ApplicationItem(application_name='DuckDuckGo',
                                                                     application_hour=0,
                                                                     application_min=3)
                                                     ])

mock_screen_time_data_again = ScreenTimeItem(day='16',
                                             month='February',
                                             year='2024',
                                             total_hour=2,
                                             total_min=32,
                                             applications=[ApplicationItem(application_name='Safari',
                                                                           application_hour=1,
                                                                           application_min=59),
                                                           ApplicationItem(application_name='MyFitnessPal',
                                                                           application_hour=0,
                                                                           application_min=8),
                                                           ApplicationItem(application_name='Messages',
                                                                           application_hour=0,
                                                                           application_min=8)
                                                           ])

mock_screen_time_data_with_missing_applications = ScreenTimeItem(day='29',
                                                                 month='January',
                                                                 year='2024',
                                                                 total_hour=1,
                                                                 total_min=42,
                                                                 applications=[
                                                                     ApplicationItem(application_name='Safari',
                                                                                     application_hour=1,
                                                                                     application_min=4),
                                                                     ApplicationItem(application_name='WhatsApp',
                                                                                     application_hour=0,
                                                                                     application_min=16),
                                                                     ])

mock_test_data = ['10:00', '. atl > (_', 'Week Day', 'SCREEN TIME',
                  'Today,', '16', 'February', '2h', '32min', '! — 0', 'M Tu Ww ‘Th F Sa Su', ', 60min.', '= 30min',
                  "'12am ‘6am '12pm ‘6pm", 'Health & Fitness Social Education', 'Smin. Smin. 2min.',
                  'MOST USED SHOW CATEGORIES', 'Safari', '1h', '59min', 'MyFitnessPal', '8min', 'Messages',
                  '8min', 'yy SChO0 kiiytGae N']

folder_path = f"{pathlib.Path(__file__).parent.resolve()}/test_data"


def test_load_screen_time_data():
    results = load_screen_time_data(folder_path)
    assert results.shape == (6, 14)


def test_load_screen_time_data_with_invalid_folder_path():
    fake_folder = "FakeFolder"
    with pytest.raises(FolderDoesNotExistError) as excinfo:
        results = load_screen_time_data(fake_folder)
    assert str(excinfo.value) == f"Folder `{fake_folder}` does not exist"


def test_load_screen_time_item():
    result = load_screen_time_item(f"{folder_path}/13_Feb_2024_at_10.png")
    assert result is not None
    assert result.day == mock_screen_time_data.day
    assert result.month == mock_screen_time_data.month
    assert result.total_hour == mock_screen_time_data.total_hour
    assert result.total_min == mock_screen_time_data.total_min
    assert result.applications == mock_screen_time_data.applications


def test_load_screen_time_item_with_different_file():
    result = load_screen_time_item(f"{folder_path}/16 Feb 2024 at 10.png")
    assert result is not None
    assert result.day == mock_screen_time_data_again.day
    assert result.month == mock_screen_time_data_again.month
    assert result.total_hour == mock_screen_time_data_again.total_hour
    assert result.total_min == mock_screen_time_data_again.total_min
    assert result.applications == mock_screen_time_data_again.applications


def test_load_screen_time_item_with_image_with_no_today_text_found():
    result = load_screen_time_item(f"{folder_path}/25_Jan_2024.png")
    assert result is not None
    assert result.day == "23"
    assert result.month == "January"


def test_load_screen_time_item_with_image_with_yesterday_screen_time_data():
    result = load_screen_time_item(f"{folder_path}/20 Feb 2024 at 10pm.png")
    assert result is not None
    assert result.day == "19"
    assert result.month == 'February'


def test_load_screen_time_item_with_no_screen_time_data():
    result = load_screen_time_item(f"{folder_path}/28 Jan 2024 at 10pm.png")
    assert result is not None
    assert result.day == "28"
    assert result.month == 'Jan'
    assert result.year == '2024'


def test_create_screen_time_item_from_text():
    result = create_screen_time_item_from_text(mock_test_data)
    assert result is not None
    assert result.day == mock_screen_time_data_again.day
    assert result.month == mock_screen_time_data_again.month
    assert result.total_hour == mock_screen_time_data_again.total_hour
    assert result.total_min == mock_screen_time_data_again.total_min
    assert result.applications == mock_screen_time_data_again.applications


def test_create_screen_time_item_where_limited_application_entries():
    result = load_screen_time_item(f"{folder_path}/29 Jan 2024 at 10:15pm.png")
    assert result is not None
    assert result.day == mock_screen_time_data_with_missing_applications.day
    assert result.month == mock_screen_time_data_with_missing_applications.month
    assert result.total_hour == mock_screen_time_data_with_missing_applications.total_hour
    assert result.total_min == mock_screen_time_data_with_missing_applications.total_min
    assert result.applications == mock_screen_time_data_with_missing_applications.applications


def test_create_application_item_from_text():
    text = ["Safari", '1h', '2min']
    application_index = 0
    expected = ApplicationItem(application_name=text[0], application_hour=1, application_min=2)
    result = create_application_item_from_text(text, application_index)
    assert result == expected


def test_create_application_item_from_text_with_no_minutes():
    text = ["Safari", "1h"]
    application_index = 0
    expected = ApplicationItem(application_name=text[0], application_hour=1, application_min=0)
    result = create_application_item_from_text(text, application_index)
    assert result == expected


def test_create_application_item_from_text_with_no_minutes_and_other_application_in_minute_spot():
    text = ["Safari", "1h", 'Roblox']
    application_index = 0
    expected = ApplicationItem(application_name=text[0], application_hour=1, application_min=0)
    result = create_application_item_from_text(text, application_index)
    assert result == expected


def test_create_application_item_from_text_with_seconds():
    text = ["Safari", "32s", 'Roblox']
    application_index = 0
    expected = ApplicationItem(application_name=text[0], application_hour=0, application_min=1)
    result = create_application_item_from_text(text, application_index)
    assert result == expected


def test_create_application_with_no_time():
    text = ["Safari"]
    application_index = 0
    expected = None
    result = create_application_item_from_text(text, application_index)
    assert result == expected


def test_create_application_item_from_text_with_no_digits_for_minutes():
    text = ["Safari", "min", 'Roblox']
    application_index = 0
    expected = ApplicationItem(application_name=text[0], application_hour=0, application_min=0)
    result = create_application_item_from_text(text, application_index)
    assert result == expected


def test_create_application_item_from_text_with_no_digits_for_hours():
    text = ["Safari", "h"]
    application_index = 0
    expected = ApplicationItem(application_name=text[0], application_hour=0, application_min=0)
    result = create_application_item_from_text(text, application_index)
    assert result == expected

