import pandas as pd
from typing import List
from app.core.entities.repository import Repository
from app.core.interfaces.report_generator import ReportGenerator

class ExcelReportGenerator(ReportGenerator):
    def generate(self, repositories: List[Repository], output_path: str):
        repo_data = []
        for repo in repositories:
            data = repo.model_dump()
            data['age_in_years'] = repo.age_in_years
            repo_data.append(data)
        
        if not repo_data:
            return

        df = pd.DataFrame(repo_data)
        column_order = [
            'name', 'url', 'age_in_years', 'releases', 'stars',
            'total_loc', 'total_comments', 'java_files',
            'avg_loc_per_file', 'avg_comments_per_file',
            'cbo_avg', 'dit_avg', 'lcom_avg',
            'cbo_total', 'dit_total', 'lcom_total'
        ]
        df_ordered = df[[col for col in column_order if col in df.columns]]
        df_ordered = df_ordered.sort_values("total_loc", ascending=False)
        df_ordered.to_excel(output_path, index=False)