import pandas as pd
from io import BytesIO
import requests

def fetchExcelFile(feedback_file: str):
    try:
        response = requests.get(feedback_file)
        response.raise_for_status()
        with BytesIO(response.content) as f:
            df = pd.read_excel(f)
        return df
    except Exception as e:
        return e

def requestExcelFile(feedback_file: str, ctx):
    try:
        df = fetchExcelFile(feedback_file)

        user_feedback = df.loc[df['Discord Username'] == str(ctx.author), 'Feedback'].values
        return user_feedback
    except Exception as e:
        return e

def getGraphData(feedback_file: str):
    try:
        df = fetchExcelFile(feedback_file)
        
        # Count the occurrence of each grade in the 'Grade' column
        grade_counts = df['Grade'].value_counts().sort_index()

        x = grade_counts.index.tolist()

        y = grade_counts.values.tolist()

        # Filter out grades with a count of 0
        x_filtered = []
        y_filtered = []
        for i in range(len(x)):
            if y[i] > 0:
                x_filtered.append(x[i])
                y_filtered.append(y[i])

        return x_filtered, y_filtered
    except Exception as e:
        print(e)
        return [], []