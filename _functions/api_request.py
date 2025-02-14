import requests

def api_request(*match_ids):
    location = []
    for match in match_ids:
        # Create a session
        session = requests.Session()

        # Set the User-Agent
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        })

        # Add cookies to the session
        cookies = [
            {"name": "MatchFilter", "value": "{%22active%22:false%2C%22live%22:false%2C%22stars%22:1%2C%22lan%22:false%2C%22teams%22:[]}", "domain": "www.hltv.org", "path": "/"},
            {"name": "CookieConsent", "value": "{stamp:%273NgGg27hj0ejKpNtm87m/YBPSLnL4lNd/yPbJihd+Z9o9RYqFbPN7w==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1733077873420%2Cregion:%27br%27}", "domain": "www.hltv.org", "path": "/"},
            {"name": "statsTablePadding", "value": "medium", "domain": "www.hltv.org", "path": "/"},
            {"name": "__cf_bm", "value": "Szqh7H3goQyxtOGltGDj3JTi5AxfM7o8BtlyRREBKUM-1739387417-1.0.1.1-wFe_izUohFuhoOtPdSCoQh1dVsFIVKshKM_UcRAMW79ydlMLqOBeG12UCC7SyCrKvuTz0ehnU.j2G9rQ25jO6A", "domain": ".hltv.org", "path": "/"},
            {"name": "cf_clearance", "value": "yJF7r97wuRGreobMDmO_qrMka5365vYtJ89ivg7Pfww-1739388252-1.2.1.1-cX9fFGx0W8Ao.V0lNYEcP0b_s8wqF8JE8_mTdbdAQ6O04DCqvxbhqC1um1GuCZ.yzWMGnulO20odhLbWhBJVX9HYIjFRVH6cmSwquhhI8jbvuP3mvTYnqDWe.H05n6NIWHj8PmEjY00iOn_dEmUExShnyHwghnyM5q8z_MLvN_lXFxXOISxwbybH_Ot11hNrkXDsCNWpsphJsLoJW75I5s.RJ3LSFte9Zb.CIvBf8CTpXWGzN3dHG9sOdvNkuWlSctjDec6zeTgJ14MSOlUyfBPQTEM_2L1yBhc9EIBhwP.OWKabcgbiOd8k6L3iL289h2V89XiCFwHgzRGvEFQ0eg", "domain": ".hltv.org", "path": "/"}
        ]

        for cookie in cookies:
            session.cookies.set(cookie["name"], cookie["value"], domain=cookie["domain"], path=cookie["path"])

        # Set the headers
        headers = {
            "authority": "www.hltv.org",
            "method": "GET",
            "path": f"/download/demo/{match}",
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "priority": "u=0, i",
            "referer": "https://www.hltv.org/",
            "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            "sec-ch-ua-arch": '"x86"',
            "sec-ch-ua-bitness": '"64"',
            "sec-ch-ua-full-version": '"132.0.6834.160"',
            "sec-ch-ua-full-version-list": '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.160", "Google Chrome";v="132.0.6834.160"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"10.0.0"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1"
        }

        # Make the request
        url = f"https://www.hltv.org/download/demo/{match}"
        response = session.get(url, headers=headers, allow_redirects=False)
        
        # Location header contains the download link
        location.append(response.headers.get("Location"))

    return location