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

        df.columns = df.columns.str.lower()

        user_feedback = df.loc[df['discord username'] == str(ctx.author).lower(), 'feedback'].values
        return user_feedback
    except Exception as e:
        return e

def getGraphData(feedback_file: str):
    try:
        df = fetchExcelFile(feedback_file)

        df.columns = df.columns.str.lower()

        grade_column = 'grade' if 'grade' in df.columns else 'points' if 'points' in df.columns else None

        if grade_column:
        
            # Count the occurrence of each grade in the 'Grade' column
            grade_counts = df[grade_column].value_counts().sort_index()

            x = grade_counts.index.tolist()

            y = grade_counts.values.tolist()

            # Filter out grades/points with a count of 0
            x_filtered, y_filtered = zip(*[(grade, count) for grade, count in zip(x, y) if count > 0])
            return list(x_filtered), list(y_filtered)
        else:
            print("Grade or Points column not found.")
            return [], []
            
    except Exception as e:
        print(e)
        return [], []