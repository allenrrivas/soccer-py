import ScraperFC as sfc
import traceback
import pandas as pd

# Initialize the FBRef scraper
scraper = sfc.FBRef()
try:
    # Scrape the table
    lg_table = scraper.scrape_league_table(year=2023, league='La Liga')
except:
    # Catch and print any exceptions. This allows us to still close the
    # scraper below, even if an exception occurs.
    traceback.print_exc()
finally:
    # It's important to close the scraper when you're done with it. Otherwise,
    # you'll have a bunch of webdrivers open and running in the background.
    scraper.close()
    
df = pd.DataFrame(lg_table)
df.to_csv('22-23LaLigaTable.csv', sep='\t', encoding='utf-8')