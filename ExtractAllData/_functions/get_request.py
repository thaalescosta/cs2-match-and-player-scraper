import cloudscraper

def get_request(tournaments_df):

    scraper = cloudscraper.create_scraper()

    for i, match in enumerate(tournaments_df['match_id']):

        response = scraper.get(f"https://www.hltv.org/download/demo/{match}", allow_redirects=False)
        if 'Location' in response.headers:
            direct_link = response.headers['Location']
        else:
            print(f"Error downloading demo. Match ID: {i}")
            
        tournaments_df.at[i, 'url_request'] = f"https://www.hltv.org/download/demo/{match}"
        tournaments_df.at[i, 'direct_url_demo'] = direct_link

    return tournaments_df