import logging
import requests
import sys
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
)


# Initialize logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class ShopListing(NamedTuple):
    title: str
    description: str


class ShopListingsDownloader:
    '''This class is used to download listings for a given shop.'''

    ETSY_API_BASE_URL = 'https://openapi.etsy.com/v2'

    def __init__(self, shop_id: str, api_key: str) -> None:
        self._shop_id = shop_id
        self._api_key = api_key

    def get_active_listings(self) -> List[ShopListing]:
        '''Returns all active listings in our shop.'''
        listings = []

        page = 1
        while page is not None:
            json_dict = self._get_active_listings_for_page(page)
            for result in json_dict['results']:
                listings.append(ShopListing(
                    title = result['title'],
                    description = result['description'],
                ))
            page = json_dict['pagination']['next_page']

        return listings


    def _get_active_listings_for_page(self, page: int) -> Dict[str, Any]:
        '''Returns all active listings for the specified page as JSON.'''
        uri = self._get_active_listings_uri(page)
        logger.info(f'Fetching active listings from "{uri}"')

        try:
            response = requests.get(uri)
        except Exception as e:
            logger.error(f'Something went wrong: {str(e)}')
            # TODO: Implement retry loop. For now simply re-raise the exception.
            raise

        status_code = response.status_code
        if status_code != requests.status_codes.codes.OK:
            logger.error(f'Unexpected status code {status_code} returned')
            # TODO: Implement retry loop. For now simply raise a exception.
            raise ValueError(f'{status_code} returned by querying "{uri}"')

        return response.json()

    def _get_active_listings_uri(self, page: int) -> str:
        '''Returns the URI to get all active listings for the specified page.'''
        return f'{self.ETSY_API_BASE_URL}/shops/{self._shop_id}/listings/active?page={page}&api_key={self._api_key}'
