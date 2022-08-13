import config
from ts.client import TradeStationClient

ts_client = TradeStationClient(
    username=config.USERNAME,
    client_id=config.API_KEY,
    client_secret=config.API_SECRET,
    paper_trading=True
)


ts_client.login()
