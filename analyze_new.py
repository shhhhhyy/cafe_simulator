import pandas as pd
import argparse
import os
import csv

# ------------------------------------
# XY 저장 함수
# ------------------------------------
def append_xy(out_path, Xw, Xtwo, Xfour, best_df):
    write_header = not os.path.exists(out_path)

    with open(out_path, "a", newline="") as f:
        writer = csv.writer(f)

        if write_header:
            writer.writerow([
                "Xw", "Xtwo", "Xfour",
                "Yw", "Ytwo", "Yfour"
            ])

        for _, row in best_df.iterrows():
            writer.writerow([
                Xw, Xtwo, Xfour,
                int(row["w"]),
                int(row["two"]),
                int(row["four"])
            ])


# ------------------------------------
# 최적 조합(Y) 찾기 — 순수익만 고려
# ------------------------------------
def best_for_X(df, Xw, Xtwo, Xfour, out_csv=None):
    df_sub = df[
        (df["w"] <= Xw) &
        (df["two"] <= Xtwo) &
        (df["four"] <= Xfour)
    ]

    if df_sub.empty:
        print("❌ 해당 조건에 해당하는 row 없음")
        return None

    print(f"\n========= X({Xw},{Xtwo},{Xfour}) subset ==========")
    print(df_sub.head())

    # 🔥 순수익만 고려하는 score (turnover 제거)
    df_sub["score_norm"] = df_sub["profit_norm"]

    # best 선택
    best = df_sub.loc[df_sub["score_norm"].idxmax()].to_frame().T

    print("\n======= Best Result (Profit Only) =======")
    print(best)
    print("========================================")

    # CSV 저장
    if out_csv is not None:
        append_xy(out_csv, Xw, Xtwo, Xfour, best)
        print(f"\n📌 XY 데이터 저장됨 → {out_csv}")

    return best


# ------------------------------------
# 메인
# ------------------------------------
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=str, default="master_results.csv")
    parser.add_argument("--Xw", type=int, required=True)
    parser.add_argument("--Xtwo", type=int, required=True)
    parser.add_argument("--Xfour", type=int, required=True)
    parser.add_argument("--out_csv", type=str, default="xy_dataset.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.csv)

    # ------------------------------------
    # 🔥 순수익 정규화 (turnover 제거)
    # ------------------------------------
    print("🔄 profit_norm 정규화 진행중...")

    df["profit_norm"] = df["net_profit"] / df["net_profit"].max()

    # ------------------------------------
    # Y 선택 및 저장
    # ------------------------------------
    best_for_X(df, args.Xw, args.Xtwo, args.Xfour, out_csv=args.out_csv)