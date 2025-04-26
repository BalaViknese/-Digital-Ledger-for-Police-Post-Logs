import pandas as pd

df = pd.read_csv("E:/GUVI/Police_Dataset - file.csv")

print("Original dataset shape:", df.shape)
print("Columns with only NaNs:")
print(df.columns[df.isna().all()])


threshold = df.shape[1] / 2
df_cleaned = df.dropna(thresh=threshold)

df_cleaned.reset_index(drop=True, inplace=True)

df_cleaned.to_csv("E:/GUVI/STOPS.csv", index=False)

print(f"Cleaned data saved to: E:/GUVI/STOPS.csv")
