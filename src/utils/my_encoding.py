import pandas as pd


def fix_encoding(problem_string):
    """
    Função para corrigir a codificação de uma string
    """
    if isinstance(
        problem_string, str
    ):  # Checar se é uma string, foi necessário por ter valores nulos
        return problem_string.encode("Windows-1252", errors="ignore").decode(
            "utf-8", errors="ignore"
        )
    else:
        return problem_string


if __name__ == "__main__":
    df = pd.read_csv("data/Listings.csv", encoding="utf-8", encoding_errors="ignore")
    df["name"] = df["name"].apply(fix_encoding)
    df.to_csv("data/Listings_new.csv", encoding="utf-8", index=False)
