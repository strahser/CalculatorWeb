R_test = 6
R_wall1 = R_test  # 3.34
R_wall2 = R_test  # 3.16
R_wall3 = R_test  # 3.19
R_wall4 = R_test  # 3.42
k_win = 0.98  # 0.56

k_ed = 0.913 * (
            50 / R_wall2 + 336 / R_wall1 + 55 / R_wall3 + 130 / R_wall4 + 430 / k_win + 1296 / 5.55 + 339 / 4.48 + 64 / 0.83)
k_ob = 1 / 34229 * (
            3406 / R_wall2 + 608 / R_wall1 + 1783 / R_wall3 + 447 / R_wall4 + 1383 / k_win + 85 / 4.86 + 0.519 * 1550 / 1.32 + k_ed)
print(k_ob)
