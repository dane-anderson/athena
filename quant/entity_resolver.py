COMPANY_MAP = {

    "apple": "AAPL",
    "apple inc": "AAPL",

    "nvidia": "NVDA",
    "nvidia corporation": "NVDA",

    "microsoft": "MSFT",
    "microsoft corporation": "MSFT",

    "spy": "SPY",
    "qqq": "QQQ"

}


def resolve_assets(text):

    text = text.lower()

    assets = []

    for name, ticker in COMPANY_MAP.items():

        if name in text:
            assets.append(ticker)

    return list(set(assets))