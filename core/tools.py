from core.models import ParameterConfig
import numpy as np
import csv
import pandas as pd
import io


def get_param_config_tag(tag):
    """ Get all param configs related to the tag"""
    recs = ParameterConfig.objects.filter(tag=tag)
    if not recs:
        return None

    return {rec.name: rec.content for rec in recs}


def handle_config_file(csv_file):
    df = pd.read_csv(io.StringIO(csv_file.read().decode('utf-8')), delimiter=',')
    ParameterConfig.objects.all().delete()

    configs = [
        ParameterConfig(
            name=row.name,
            nick_name=row.nick_name,
            tag=row.tag,
            description=row.description,
            comment=row.comment,
            content=row.content,
        ) for row in df.itertuples()
    ]
    ParameterConfig.objects.bulk_create(configs)


def calculate_rsi(df):
    """Calculate RSI dataframe has close price"""
    df['change'] = df['close'].diff(1)  # Calculate change

    # calculate gain / loss from every change
    df['gain'] = np.select([df['change'] > 0, df['change'].isna()],
                           [df['change'], np.nan],
                           default=0)
    df['loss'] = np.select([df['change'] < 0, df['change'].isna()],
                           [-df['change'], np.nan],
                           default=0)

    # create avg_gain /  avg_loss columns with all nan
    df['avg_gain'] = np.nan
    df['avg_loss'] = np.nan

    n = 14  # what is the window

    # Alternatively
    df['avg_gain'][n] = df.loc[:n, 'gain'].mean()
    df['avg_loss'][n] = df.loc[:n, 'loss'].mean()

    # This is not a pandas way, looping through the pandas series, but it does what you need
    for i in range(n + 1, df.shape[0]):
        df['avg_gain'].iloc[i] = (df['avg_gain'].iloc[i - 1] * (n - 1) + df['gain'].iloc[i]) / n
        df['avg_loss'].iloc[i] = (df['avg_loss'].iloc[i - 1] * (n - 1) + df['loss'].iloc[i]) / n

    # calculate rs and rsi
    df['rs'] = df['avg_gain'] / df['avg_loss']
    df['rsi'] = 100 - (100 / (1 + df['rs']))

    # return df['rsi'].iloc[-3], df['rsi'].iloc[-2], df['rsi'].iloc[-1]
    return df
