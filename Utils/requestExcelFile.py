import pandas as pd
from io import BytesIO
import requests

def requestExcelFile(feedback_file: str, ctx):
    try:
        response = requests.get(feedback_file)
        response.raise_for_status()
        with BytesIO(response.content) as f:
            df = pd.read_excel(f)

        user_feedback = df.loc[df['Discord Username'] == str(ctx.author), 'Feedback'].values
        return user_feedback
    except Exception as e:
        return e