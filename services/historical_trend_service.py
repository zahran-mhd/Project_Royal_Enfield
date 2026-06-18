import os
import pandas as pd


class HistoricalTrendService:

    def __init__(self, app):

        self.app = app

    def get_trend_data(
        self,
        folder,
        start_cycle,
        end_cycle,
        parameter
    ):

        x_values = []
        y_values = []

        for cycle in range(
            start_cycle,
            end_cycle + 1
        ):

            file_path = os.path.join(
                folder,
                f"Cycle_{cycle}.csv"
            )

            if not os.path.exists(file_path):
                continue

            try:

                df = pd.read_csv(file_path)

                if parameter not in df.columns:
                    continue

                avg_value = (
                    df[parameter]
                    .mean()
                )

                x_values.append(cycle)

                y_values.append(avg_value)

            except Exception as ex:

                print(ex)

        return x_values, y_values