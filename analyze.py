import pandas as pd
import argparse
import os
import csv

def append_xy(out_path, Xw, Xtwo, Xfour, best_df):
    write_header = not os.path.exists(out_path)

    with open(out_path, "a", newline="") as f:
        writer = csv.writer(f)

        if write_header:
            writer.writerow(["Xw", "Xtwo", "Xfour", "Xstay", "Yw", "Ytwo", "Yfour"])

        for _, row in best_df.iterrows():
            writer.writerow([
                Xw, Xtwo, Xfour, 
                int(row["max_stay"]),
                int(row["w"]),
                int(row["two"]),
                int(row["four"])
            ])


def best_for_X(df, Xw, Xtwo, Xfour, out_csv=None):
    df_sub = df[
        (df["w"] <= Xw) &
        (df["two"] <= Xtwo) &
        (df["four"] <= Xfour)
    ]

    if df_sub.empty:
        print("❌ 해당 조건에 해당하는 row 없음")
        return None

    # max_stay별 best score 선택
    best = df_sub.loc[df_sub.groupby("max_stay")["score"].idxmax()]

    # 🚨 max_stay 순으로 정렬 (여기가 핵심)
    best = best.sort_values("max_stay")

    if out_csv is not None:
        append_xy(out_csv, Xw, Xtwo, Xfour, best)

    return best


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=str, default="master_results.csv")
    parser.add_argument("--Xw", type=int, required=True)
    parser.add_argument("--Xtwo", type=int, required=True)
    parser.add_argument("--Xfour", type=int, required=True)
    parser.add_argument("--out_csv", type=str, default=None)
    args = parser.parse_args()

    df = pd.read_csv(args.csv)

    best_for_X(df, args.Xw, args.Xtwo, args.Xfour, out_csv=args.out_csv)