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
    

    def get_columns(
        self,
        folder,
        cycle_no
    ):

        return self.service.get_columns(
            folder,
            cycle_no
        )