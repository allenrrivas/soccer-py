import ScraperFC as sfc
import traceback
import pandas as pd

# Initialize the FBRef scraper
scraper = sfc.FBRef()
try:
    # Scrape the match using the FBRef match link
    player = scraper.complete_report_from_player_link(player_link="https://fbref.com/en/players/6ce1f46f/Toni-Kroos")
except:
    # Catch and print any exceptions.
    traceback.print_exc()
finally:
    # Again, make sure to close the scraper when you're done
    scraper.close()

print(player)