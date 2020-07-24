import pandas as pd
from sqlalchemy import create_engine, text

##############################
# DEFINITIONS
##############################
# CONTENTS
# 1. SQL
# 2. DEA Phase I
# 3. DEA Phase II
# ------------------------------

# ------------------------------
# 1. SQL
# ------------------------------

# 1.1 SQL Connection
# ------------------------------
# maximum number of rows to display
pd.options.display.max_rows = 20

DB_USERNAME = 'alagos'
DB_PASSWORD = 'Team67!'
DB_ENDPOINT = 'ds4a-demo-instance.cqjr4hyu9xaq.us-east-1.rds.amazonaws.com'
DB_NAME = 'desertion_pj_team67'
engine=create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}', max_overflow=20)

# 1.2 SQL query
# ------------------------------
def runQuery(sql):
    result = engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(sql)))
    return pd.DataFrame(result.fetchall(), columns=result.keys())

# ------------------------------
# 2. DEA Phase I
# ------------------------------

# 2.1 Set base model for Phase I
# ------------------------------
def BCCO_Base_PH1(data, inp, out):
    # Initialize components of LP
    global obj1, lhs_eq1, rhs_eq1, lhs_ineq1, rhs_ineq1, bnd1
    obj1, lhs_eq1, rhs_eq1, lhs_ineq1, rhs_ineq1, bnd1 = ([] for i in range(6))

    # Set linear inequalities
    tmp = []
    for i in inp:
        tmp = data[i].tolist()
        tmp.insert(0, 0)
        lhs_ineq1.append(tmp)
    for o in out:
        tmp = data[o].tolist()
        tmp = [-1 * i for i in tmp]
        tmp.insert(0, 0)
        lhs_ineq1.append(tmp)

    obj1 = [-1]
    tmp = [0]
    rhs_eq1 = [1]
    bnd1 = [(float("-inf"), float("inf"))]
    for k in range(len(data[inp[0]])):
        obj1.append(0)
        tmp.append(1)
        bnd1.append((0, float("inf")))
    lhs_eq1.append(tmp)

# 2.2 Set model for each DMU for Phase I
# ------------------------------
def BCCO_DMU_PH1(data, dmu, inp, out):
    # Initialize components of LP
    global rhs_ineq1
    rhs_ineq1 = []
    index = 0

    # Data from selected DMU
    dmu_data = data[data['DMU'] == dmu].reset_index()

    for i in inp:
        lhs_ineq1[index][0] = 0
        rhs_ineq1.append(dmu_data[i][0])
        index = index + 1

    for o in out:
        lhs_ineq1[index][0] = dmu_data[o][0]
        rhs_ineq1.append(0)
        index = index + 1

# 2.3 Define slack/waste variables
# ------------------------------
def BCCO_DMU_VAR(inp, out, slack):
    varset = []
    nInp = len(inp)
    for i in range(len(slack)):
        if slack[i] > 0.01:
            if i < len(inp):
                varset.append(inp[i])
            else:
                varset.append(out[i-nInp])
    return varset


# ------------------------------
# 3. DEA Phase II
# ------------------------------

# 3.1 Set base model for Phase II
# ------------------------------
def BCCO_Base_PH2(data, inp, out):
    # Initialize components of LP
    global obj2, lhs_eq2, rhs_eq2, bnd2
    obj2, lhs_eq2, rhs_eq2, bnd2 = ([] for i in range(4))

    # Set linear inequalities
    nSlk = len(inp) + len(out)
    tmp = []
    index = 0

    for i in inp:
        tmp = data[i].tolist()
        for j in range(nSlk):
            tmp.insert(0, 0)
        tmp[index] = 1
        lhs_eq2.append(tmp)
        index = index + 1

    for o in out:
        tmp = data[o].tolist()
        # tmp = [-1 * i for i in tmp]
        for j in range(nSlk):
            tmp.insert(0, 0)
        tmp[index] = -1
        lhs_eq2.append(tmp)
        index = index + 1

    tmp = []
    for j in range(nSlk):
        obj2.append(1)
        bnd2.append((0, float("inf")))
        tmp.append(0)

    for k in range(len(data[inp[0]])):
        obj2.append(0)
        bnd2.append((0, float("inf")))
        tmp.append(1)
    lhs_eq2.append(tmp)

# 3.2 Set model for each DMU for Phase II
# ------------------------------
def BCCO_DMU_PH2(data, dmu, theta, inp, out):
    # Initialize components of LP
    global rhs_eq2
    rhs_eq2 = []

    # Data from selected DMU
    dmu_data = data[data['DMU'] == dmu].reset_index()

    for i in inp:
        rhs_eq2.append(dmu_data[i][0])

    for o in out:
        rhs_eq2.append(theta * dmu_data[o][0])

    rhs_eq2.append(1)

# 3.2 Determine which DMUs comprise the reference set.
# ------------------------------
def BCCO_DMU_REFSET(data, inp, out, ph2_x):
    dmu_names = data['DMU'].reset_index()
    nSlk = len(inp)+len(out)
    res = ph2_x[nSlk:]
    refset = []
    for i in range(len(res)):
        if res[i] > 0:
            refset.append(dmu_names.iloc[i][1])
    return refset
