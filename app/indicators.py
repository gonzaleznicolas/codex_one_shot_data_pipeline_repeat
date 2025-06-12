import pandas as pd


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Compute SMA30, price_over_sma_30, bb_pct and positions."""
    df = df.copy()
    df['sma30'] = df['Close'].rolling(window=30).mean()
    df['price_over_sma_30'] = df['Close'] / df['sma30']
    df['std30'] = df['Close'].rolling(window=30).std()
    df['upper_bb'] = df['sma30'] + 2 * df['std30']
    df['lower_bb'] = df['sma30'] - 2 * df['std30']
    df['bb_pct'] = (df['Close'] - df['lower_bb']) / (df['upper_bb'] - df['lower_bb'])

    # Price over SMA position
    def sma_pos(x: float) -> str:
        if pd.isna(x):
            return 'cash'
        if x > 1:
            return 'long'
        if x < 1:
            return 'short'
        return 'cash'

    df['pos_sma'] = df['price_over_sma_30'].apply(sma_pos)

    # Bollinger band position with state machine
    bb_positions = []
    state = 'cash'
    for bb in df['bb_pct']:
        if pd.isna(bb):
            bb_positions.append('cash')
            continue
        if state == 'cash' and bb < 0:
            state = 'long'
        elif state == 'long' and bb > 1:
            state = 'short'
        elif state == 'short' and bb < 0:
            state = 'long'
        bb_positions.append(state if state != 'cash' else 'cash')
    df['pos_bb'] = bb_positions

    def final_pos(row) -> str:
        if row['pos_sma'] == row['pos_bb']:
            return row['pos_sma']
        return 'cash'

    df['suggested'] = df.apply(final_pos, axis=1)
    return df
