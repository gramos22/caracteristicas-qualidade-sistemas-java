import subprocess
import os
import pandas as pd
from typing import Dict
from app.core.interfaces.static_analyzer import StaticAnalyzer

class CkAnalyzer(StaticAnalyzer):
    def __init__(self, ck_jar_path: str, output_dir: str = "/tmp/ck_reports"):
        if not os.path.exists(ck_jar_path):
            raise FileNotFoundError(f"CK JAR not found at: {ck_jar_path}")
        self.ck_jar_path = ck_jar_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def analyze(self, repo_path: str) -> Dict[str, float]:
        try:
            for f in os.listdir(self.output_dir):
                os.remove(os.path.join(self.output_dir, f))

            subprocess.run(
                [
                    "java", "-jar", self.ck_jar_path,
                    repo_path, "true", "0", "False", self.output_dir
                ],
                check=True,
                capture_output=True,
                text=True
            )

            class_csv_path = os.path.join(self.output_dir, "class.csv")
            if not os.path.exists(class_csv_path):
                return {"cbo": 0, "dit": 0, "lcom": 0}

            df = pd.read_csv(class_csv_path)
            return {
                "cbo": df["cbo"].mean(),
                "dit": df["dit"].mean(),
                "lcom": df["lcom"].mean(),
            }
        except (subprocess.CalledProcessError, FileNotFoundError, pd.errors.EmptyDataError):
            return {"cbo": 0, "dit": 0, "lcom": 0}