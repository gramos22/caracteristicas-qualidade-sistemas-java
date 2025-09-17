import subprocess
import os
import pandas as pd
from typing import Dict
from app.core.interfaces.static_analyzer import StaticAnalyzer

class CkAnalyzer(StaticAnalyzer):
    def __init__(self, ck_jar_path: str, output_dir: str):
        if not os.path.exists(ck_jar_path):
            raise FileNotFoundError(f"CK JAR not found at: {ck_jar_path}")
        self.ck_jar_path = ck_jar_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _count_lines_and_comments(self, repo_path: str) -> Dict[str, int]:
        total_loc = 0
        total_comments = 0
        java_files = 0
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".java"):
                    java_files += 1
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                            in_block_comment = False
                            for line in f:
                                total_loc += 1
                                stripped_line = line.strip()
                                if in_block_comment:
                                    total_comments += 1
                                    if '*/' in stripped_line:
                                        in_block_comment = False
                                    continue
                                if stripped_line.startswith('//'):
                                    total_comments += 1
                                elif '/*' in stripped_line:
                                    total_comments += 1
                                    if '*/' not in stripped_line:
                                        in_block_comment = True
                    except Exception:
                        continue
        return {"total_loc": total_loc, "total_comments": total_comments, "java_files": java_files}

    def analyze(self, repo_path: str) -> Dict[str, float]:
        repo_name = os.path.basename(repo_path)
        metrics = {
            "cbo_avg": 0.0, "dit_avg": 0.0, "lcom_avg": 0.0,
            "cbo_total": 0, "dit_total": 0, "lcom_total": 0.0,
        }

        try:
            for f in os.listdir(self.output_dir):
                os.remove(os.path.join(self.output_dir, f))

            subprocess.run(
                ["java", "-Xmx4g", "-jar", self.ck_jar_path, repo_path, "true", "0", "True", self.output_dir],
                check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=600
            )

            class_csv_path = os.path.join(self.output_dir, "class.csv")
            if os.path.exists(class_csv_path) and os.path.getsize(class_csv_path) > 0:
                df = pd.read_csv(class_csv_path)
                metric_cols = ['cbo', 'dit', 'lcom']
                for col in metric_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                        df = df.dropna(subset=metric_cols)
                        if not df.empty:
                            metrics["cbo_avg"] = df["cbo"].mean()
                            metrics["dit_avg"] = df["dit"].mean()
                            metrics["lcom_avg"] = df["lcom"].mean()
                            metrics["cbo_total"] = int(df["cbo"].sum())
                            metrics["dit_total"] = int(df["dit"].sum())
                            metrics["lcom_total"] = df["lcom"].sum()

        except subprocess.TimeoutExpired:
            pass
        except subprocess.CalledProcessError:
            pass
        except Exception:
            pass

        line_counts = self._count_lines_and_comments(repo_path)
        metrics.update(line_counts)

        if metrics.get("java_files", 0) > 0:
            metrics["avg_loc_per_file"] = metrics.get("total_loc", 0) / metrics["java_files"]
            metrics["avg_comments_per_file"] = metrics.get("total_comments", 0) / metrics["java_files"]
        else:
            metrics["avg_loc_per_file"] = 0.0
            metrics["avg_comments_per_file"] = 0.0
        
        return metrics