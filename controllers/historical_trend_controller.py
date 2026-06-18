from services.historical_trend_service import (
    HistoricalTrendService
)


class HistoricalTrendController:

    def __init__(self,app):

        self.app = app

        self.service = (
            HistoricalTrendService(app)
        )

    def get_graph_data(
        self,
        folder,
        start_cycle,
        end_cycle,
        parameter
    ):

        return self.service.get_trend_data(
            folder,
            start_cycle,
            end_cycle,
            parameter
        )