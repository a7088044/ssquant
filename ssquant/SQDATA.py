import requests
from requests.exceptions import RequestException, Timeout
import pandas as pd

class TakeData:
    """
    Client for accessing futures data from a Flask backend with user authentication.
    """

    def __init__(self, base_url='http://kanpan789.com:8086', username=None, password=None): 
        """
        Initializes the FlaskClient with a base URL and optional authentication credentials.
        
        :param base_url: The base URL of the Flask backend server.
        :param username: The username for authentication.
        :param password: The password for authentication.
        """
        if  not username or not password:
            raise ValueError("用户名和密码不能为空")
        self.base_url = base_url
        self.username=username
        self.password=password
    def get_data(self, symbol, start_date, end_date, kline_period='1M', adjust_type=0):
        """
        Retrieves futures data from the Flask backend with authentication.

        :param symbol: The symbol for the futures contract.
        :param start_date: The start date for the data retrieval.
        :param end_date: The end date for the data retrieval.
        :param kline_period: The period of the K-line data.
        :param adjust_type: The type of adjustment for the data.
        :return: JSON response from the server or None in case of error.
        """
        if not symbol or not start_date or not end_date:
            print("请检查要获取的品种或开始结束日期是否输入有问题")
            return None

        params = {
            'username':self.username,
            'password': self.password,
            'symbol': symbol,
            'start_date': start_date,
            'end_date': end_date,
            'kline_period': kline_period,
            'adjust_type': adjust_type
        }

        try:
            response = requests.get(
                f'{self.base_url}/Futures_data',
                params=params,
                timeout=30  # 设置30秒超时
            )
            response.raise_for_status()  # 检查HTTP响应状态
            # 从响应中获取 JSON 数据并转换为 DataFrame
            df = pd.read_json(response.text, orient='records')
            # 按照您想要的顺序指定列的名称
            columns_ordered = ['datetime', 'symbol', 'open', 'high', 'low', 'close', 'volume','amount', 'cumulative_openint','openint', 'open_bidp', 'open_askp', 'close_bidp', 'close_askp']
            # 重新排列 DataFrame 的列
            df = df[columns_ordered]
            # 将 datetime 列转换为 datetime 类型（如果尚未转换）
            df['datetime'] = pd.to_datetime(df['datetime'])
            # 更改时间显示的格式，例如 "YYYY-MM-DD HH:MM:SS"
            # 将 UTC 时间转换为本地时区，例如 'Asia/Shanghai'
            df['datetime'] = df['datetime'].dt.tz_convert('Asia/Shanghai')
            df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
            return df  # 返回 DataFrame
        except Timeout:
            print("超时请求了")
            return None
        except RequestException as e:
            print(f"An error occurred: {e}")
            return None

