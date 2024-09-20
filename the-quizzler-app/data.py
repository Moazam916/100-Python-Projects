import requests as rq


class Data:
    def __init__(self, url, parameters):
        self.questions = self.questions_data(url, parameters)

    def questions_data(self, data_base_url, url_parameters):
        response = rq.get(url=data_base_url, params=url_parameters)
        response.raise_for_status()
        question_data_api = response.json()
        return question_data_api
