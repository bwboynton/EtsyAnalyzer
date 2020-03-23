import argparse
import sys

from tabulate import tabulate

from downloader import ShopListingsDownloader
from relevance import Relevance


# We download listings from these shops.
ETSY_SHOP_IDS = frozenset({
    'ArtisticAnyaDesigns',  # 78 listings
    'AtelierDmontreal',  # 9 listings
    'AtlanticHardware',  # 11 listings
    'banadesigns',  # 158 listings
    'ConnectCo',  # 286 listings
    'fruitionjewelry',  # 53 listings
    'ExGlow',  # 61 listings
    'RenzRags',  # 853 listings
    'RusticWoodSlices',  # 34 listings
    'TheCrystalAngel888',  # 1304 listings
})

NUM_RELEVANT_WORDS_PER_SHOP = 5


def main() -> None:
    # Parse CLI argument(s).
    cliParser = argparse.ArgumentParser()
    cliParser.add_argument('--api_key', required=True, type=str, help='Etsy API key')
    cliArgs = cliParser.parse_args()

    # For each shop fetch all active listings.
    shop2listings = {}
    for shop_id in ETSY_SHOP_IDS:
        downloader = ShopListingsDownloader(
            shop_id=shop_id,
            api_key=cliArgs.api_key,
        )
        shop2listings[shop_id] = downloader.get_active_listings()

    # Compute the most relevant words for each shop.
    relevance = Relevance(shop2listings)
    shop2words = relevance.compute_relevant_words(NUM_RELEVANT_WORDS_PER_SHOP)

    # Output the results.
    print()
    print(f'TOP {NUM_RELEVANT_WORDS_PER_SHOP} RELEVANT WORDS FOR EACH SHOP')
    table = [[shop_id] + words for shop_id, words in sorted(shop2words.items())]
    print(tabulate(table))


if __name__ == '__main__':
    main()
