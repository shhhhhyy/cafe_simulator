import pandas as pd
import argparse

def best_for_X(df, Xw, Xtwo, Xfour):
    df_sub = df[
        (df["w"] <= Xw) &
        (df["two"] <= Xtwo) &
        (df["four"] <= Xfour)
    ]

    if df_sub.empty:
        print("❌ 해당 조건에 해당하는 row 없음")
        return

    print("\n========= X에서 가능한 subset ==========")
    print(df_sub.head())

    # alpha별 best score 선택
    best = df_sub.loc[df_sub.groupby("alpha")["score"].idxmax()]

    print("\n======= α별 최적 조합(Y) =======")
    print(best)
    print("===============================")

    return best

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=str, default="master_results.csv")
    parser.add_argument("--Xw", type=int, required=True)
    parser.add_argument("--Xtwo", type=int, required=True)
    parser.add_argument("--Xfour", type=int, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.csv)

    best_for_X(df, args.Xw, args.Xtwo, args.Xfour)