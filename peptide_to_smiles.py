import pandas as pd
from rdkit import Chem

# 读取 CSV 文件
input_file = "/tmp/pycharm_project_MC/data/remove_strange_values/mic_b.csv"
df = pd.read_csv(input_file)

# 确保 CSV 包含所需列
if "sequence" not in df.columns or "mic_value" not in df.columns:
    raise ValueError("CSV 文件必须包含 'sequence' 和 'mic_value' 列")

# 处理序列并转换为 SMILES
peptide_smiles_list = []
for idx, row in df.iterrows():
    seq = row["sequence"].strip()
    mic_value = row["mic_value"]

    try:
        smiles = Chem.MolToSmiles(Chem.MolFromFASTA(seq))
        peptide_smiles_list.append([idx + 1, smiles, mic_value])
    except Exception as e:
        print(f"转换失败: {seq}, 错误: {e}")
        peptide_smiles_list.append([idx + 1, "", mic_value])  # 失败的填充空值

# 转换为 DataFrame 并保存
output_df = pd.DataFrame(peptide_smiles_list, columns=["peptide_number", "SMILES", "mic_value"])
output_file = "converted_peptides.csv"
output_df.to_csv(output_file, index=False)

print(f"转换完成，结果保存在 {output_file}")
