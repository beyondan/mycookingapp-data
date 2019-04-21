import mysql.connector

con = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='recipes'
)
cursor = con.cursor()

cursor.execute(
    "SELECT recipe_id, step, direction "
    "FROM Directions "
    "ORDER BY recipe_id, step"
)

default_duration = 10

steps = {}
for recipe_id, step, direction in cursor:
    if recipe_id not in steps.keys():
        steps[recipe_id] = []
        starttime = 0
    else:
        starttime = endtime

    endtime = starttime + default_duration

    steps[recipe_id].append({
        'step_order': step,
        'step_starttime': starttime,
        'step_endtime': endtime,
        'step_text': direction
    })

for recipe_id in steps.keys():
    for step in steps[recipe_id]:
        step_order = step['step_order']
        step_starttime = step['step_starttime']
        step_endtime = step['step_endtime']
        step_text = step['step_text']
        print(f"({step_order}, {step_starttime}, {step_endtime}, {step_text})")
        cursor.execute((
                "INSERT INTO Steps (recipe_id, step_order, step_starttime, step_endtime, step_text) "
                "VALUES (%s, %s, %s, %s, %s)"
            ),
            (recipe_id, step_order, step_starttime, step_endtime, step_text)
        )

con.commit()
con.close()
