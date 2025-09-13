import pandas as pd
from io import BytesIO
import requests
import re
import matplotlib.pyplot as plt
import dataframe_image as dfi

def fetchExcelFile(feedback_file: str):
    try:
        print(f"[FETCH] Starting fetchExcelFile with URL: {feedback_file}")
        response = requests.get(feedback_file)
        print(f"[FETCH] HTTP response status code: {response.status_code}")
        response.raise_for_status()
        print(f"[FETCH] Response content length: {len(response.content)} bytes")
        
        with BytesIO(response.content) as f:
            df = pd.read_excel(f)
        print(f"[FETCH] Successfully loaded Excel file, shape: {df.shape}")
        return df
    except Exception as e:
        print(f"[FETCH] ERROR in fetchExcelFile: {type(e).__name__}: {e}")
        import traceback
        print(f"[FETCH] Full traceback:")
        traceback.print_exc()
        return e

def requestExcelFile(feedback_file: str, ctx, username: str = None, grade: bool = False):
    try:
        print(f"[EXCEL] Starting requestExcelFile with feedback_file: {feedback_file}")
        print(f"[EXCEL] Username parameter: {username}")
        print(f"[EXCEL] Grade parameter: {grade}")
        print(f"[EXCEL] Context author: {ctx.author if hasattr(ctx, 'author') else 'No author attribute'}")
        
        df = fetchExcelFile(feedback_file)
        print(f"[EXCEL] fetchExcelFile returned: {type(df)}")
        
        if isinstance(df, Exception):
            print(f"[EXCEL] fetchExcelFile returned an exception: {df}")
            return df

        print(f"[EXCEL] DataFrame shape: {df.shape}")
        print(f"[EXCEL] DataFrame columns: {list(df.columns)}")

        df.columns = df.columns.str.lower()
        print(f"[EXCEL] Columns after lowercase: {list(df.columns)}")

        if 'discord username' in df.columns:
            df['discord username'] = df['discord username'].str.lower()
            print(f"[EXCEL] Converted discord username column to lowercase")
        else:
            print(f"[EXCEL] WARNING: 'discord username' column not found!")

        lookup_username = username.lower() if username else str(ctx.author).lower()
        print(f"[EXCEL] Looking for username: '{lookup_username}'")
        
        # Show available usernames for debugging
        if 'discord username' in df.columns:
            available_usernames = df['discord username'].unique()
            print(f"[EXCEL] Available usernames in file: {available_usernames}")

        user_feedback = df.loc[df['discord username'] == lookup_username, 'feedback'].values
        print(f"[EXCEL] Found feedback entries: {len(user_feedback)}")

        if grade:
            if 'grade' in df.columns:
                user_grade = df.loc[df['discord username'] == lookup_username, 'grade'].values
                print(f"[EXCEL] Found grade entries: {len(user_grade)}")
            else:
                print(f"[EXCEL] WARNING: 'grade' column not found, using empty array")
                user_grade = []
            print(f"[EXCEL] Returning tuple: (feedback_array_size={len(user_feedback)}, grade_array_size={len(user_grade)})")
            return user_feedback, user_grade

        print(f"[EXCEL] Returning feedback only: array_size={len(user_feedback)}")
        return user_feedback

    except Exception as e:
        print(f"[EXCEL] ERROR in requestExcelFile: {type(e).__name__}: {e}")
        import traceback
        print(f"[EXCEL] Full traceback:")
        traceback.print_exc()
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