import requests
from loguru import logger


def get_request(url, headers, params):

	"""
		Функция для выполнения запроса к API.
		:param url - вэб-сайт для подключения
		:param heders - APIHost и APIKey
		:param params - параметры для поиска отелей

	"""
	try:
		response = requests.get(url=url, headers=headers, params=params, timeout=10)
		if response.status_code == requests.codes.ok:
			return response
	except(requests.RequestException, TimeoutError) as exc:
		logger.exception(exc)
