from unittest.mock import patch
from app.services import lookup_ids_bulk

STEVE_ID = "76561197999528143"
STEVE = {"steamid": STEVE_ID, "personaname": "Steve"}

JIM_ID = "76561198047699484"
JIM = {"steamid": JIM_ID, "personaname": "Jim"}

FILLER_IDS = ["7656119" + str(i).zfill(10) for i in range(300)]


@patch("app.services.lookup_ids")
def test_bulk_empty(mock_lookup_ids):
    result = lookup_ids_bulk([])
    assert result == {}
    mock_lookup_ids.assert_not_called()


@patch("app.services.lookup_ids")
def test_bulk_single_batch(mock_lookup_ids):
    mock_lookup_ids.return_value = {STEVE_ID: STEVE, JIM_ID: JIM}

    result = lookup_ids_bulk([STEVE_ID, JIM_ID])

    assert result == {STEVE_ID: STEVE, JIM_ID: JIM}
    mock_lookup_ids.assert_called_once_with([STEVE_ID, JIM_ID])


@patch("app.services.lookup_ids")
def test_bulk_batches_correctly(mock_lookup_ids):
    mock_lookup_ids.return_value = {}
    ids = FILLER_IDS[:250]

    lookup_ids_bulk(ids, batch_size=100)

    assert mock_lookup_ids.call_count == 3
    call_sizes = sorted(len(c.args[0]) for c in mock_lookup_ids.call_args_list)
    assert call_sizes == [50, 100, 100]


@patch("app.services.lookup_ids")
def test_bulk_results_merged(mock_lookup_ids):
    ids = [STEVE_ID] + FILLER_IDS[:99] + [JIM_ID] + FILLER_IDS[99:149]
    mock_lookup_ids.side_effect = lambda batch: (
        {STEVE_ID: STEVE} if STEVE_ID in batch else {JIM_ID: JIM}
    )

    result = lookup_ids_bulk(ids, batch_size=100)

    assert result == {STEVE_ID: STEVE, JIM_ID: JIM}
