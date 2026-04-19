from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from itertools import product

class ProphetTuner:

    def __init__(self, df):
        self.df = df

    def train_model(self, cps, sps, mode, fourier_order):

        m = Prophet(
            changepoint_prior_scale=cps,
            seasonality_prior_scale=sps,
            seasonality_mode=mode
        )

        m.add_seasonality(
            name='monthly',
            period=30.5,
            fourier_order=fourier_order
        )

        m.fit(self.df)

        return m

    def evaluate(self, model):
        df_cv = cross_validation(
            model,
            initial='365 days',
            period='30 days',
            horizon='90 days'
        )

        df_p = performance_metrics(df_cv)
        return df_p['rmse'].mean()

    def tune(self):

        param_grid = {
            'changepoint_prior_scale': [0.01, 0.05, 0.1],
            'seasonality_prior_scale': [0.1, 1.0],
            'seasonality_mode': ['additive', 'multiplicative'],
            'fourier_order': [3, 5, 10, 15]
        }

        results = []

        for cps, sps, mode, fo in product(
            param_grid['changepoint_prior_scale'],
            param_grid['seasonality_prior_scale'],
            param_grid['seasonality_mode'],
            param_grid['fourier_order']
        ):

            model = self.train_model(cps, sps, mode, fo)
            score = self.evaluate(model)

            results.append({
                "changepoint_prior_scale": cps,
                "seasonality_prior_scale": sps,
                "mode_seasonality": mode,
                "fourier_order": fo,
                "rmse": score
            })

        best = min(results, key=lambda x: x["rmse"])

        return best, results
