# tap-trello

This tap is designed as a *hack* to get around the limitations of the [StitchData integration](https://www.stitchdata.com/integrations/trello/) which does not support [*Custom Fields*](https://developers.trello.com/reference#cardsidcustomfielditems) and [*Organizations*](https://developers.trello.com/reference#organizationsid). It's not intended to be a replacement, but instead a companion which adds the missing schemas.

Unfortunately, the Trello API requires us to iterate over the entire relational model of Organizations, Boards, Cards, Custom Field Items, Custom Fields, etc to retrieve the missing data.

## Usage

1. Obtain your [Trello API Keys](https://trello.com/app-key).
2. Export these environment variables:
   - `TRELLO_API_KEY`
   - `TRELLO_API_TOKEN`
   - `TRELLO_USERNAME`
3. Install requirements: `pip install -r requirements.txt` 
4. Run `tap_trello.py`
