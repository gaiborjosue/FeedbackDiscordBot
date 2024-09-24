import pandas as pd
from io import BytesIO
import requests
import re
import matplotlib.pyplot as plt
import dataframe_image as dfi

def fetchExcelFile(feedback_file: str):
    try:
        response = requests.get(feedback_file)
        response.raise_for_status()
        with BytesIO(response.content) as f:
            df = pd.read_excel(f)
        return df
    except Exception as e:
        return e

def requestExcelFile(feedback_file: str, ctx, username: str = None, grade: bool = False):
    try:
        df = fetchExcelFile(feedback_file)

        df.columns = df.columns.str.lower()

        if 'discord username' in df.columns:
            df['discord username'] = df['discord username'].str.lower()

        lookup_username = username.lower() if username else str(ctx.author).lower()

        user_feedback = df.loc[df['discord username'] == lookup_username, 'feedback'].values

        if grade:
            user_grade = df.loc[df['discord username'] == lookup_username, 'grade'].values
            return user_feedback, user_grade

        return user_feedback

    except Exception as e:
        return e

def getGraphData(feedback_file: str):
    try:
        df = fetchExcelFile(feedback_file)

        df.columns = df.columns.str.lower()

        grade_column = 'grade' if 'grade' in df.columns else 'points' if 'points' in df.columns else None

        if grade_column:
        
            grade_counts = df[grade_column].value_counts().sort_index()

            x = grade_counts.index.tolist()

            y = grade_counts.values.tolist()

            x_filtered, y_filtered = zip(*[(grade, count) for grade, count in zip(x, y) if count > 0])
            return list(x_filtered), list(y_filtered)
        else:
            print("Grade or Points column not found.")
            return [], []

    except Exception as e:
        print(e)
        return [], []


def getRubric(feedback_file: str):
    try:
        df = fetchExcelFile(feedback_file)

        # Initialize an empty list to store the tasks
        tasks = []

        # Iterate over the column headers
        for header in df.columns:
            # Use a regular expression to extract the task prompt and points
            match = re.match(r"(.*) \((\d+) points\).*", header)
            if match:
                # If the header matches the pattern, add it to the tasks list
                tasks.append({
                    "Task": match.group(1),
                    "Points": int(match.group(2))
                })

        return tasks
    except Exception as e:
        return e

def buildRubric(feedback_file: str):
    tasks = getRubric(feedback_file)

    df = pd.DataFrame(tasks)

    df['IsBonus'] = df['Task'].str.contains('BONUS')

    def highlight_bonus(s):
        return ['background-color: yellow' if 'BONUS' in v else '' for v in s]

    df_styled = df.drop(columns=['IsBonus']).style.apply(highlight_bonus, subset=['Task'])

    df_styled = df_styled.background_gradient(cmap='Oranges', subset=['Points'])

    buffer = BytesIO()

    dfi.export(df_styled, buffer)

    buffer.seek(0)

    return buffer