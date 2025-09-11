from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.chart import BarChart, Reference
from typing import List
from app.core.entities.repository import Repository
from app.core.interfaces.report_generator import ReportGenerator

class ExcelReportGenerator(ReportGenerator):
    def generate(self, repos: List[Repository], file_path: str) -> None:
        wb = Workbook()
        ws = wb.active
        ws.title = f"Top {len(repos)} Repos"

        headers = ["Nome", "Estrelas", "URL", "Criado em", "Atualizado em",
                   "Releases", "Linguagem", "PRs Mergeados", "Issues Fechadas %",
                   "CBO Médio", "DIT Médio", "LCOM Médio"]
        ws.append(headers)

        for cell in ws[1]:
            cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")

        for r in repos:
            ws.append([
                r.name, r.stargazer_count, r.url, r.created_at, r.updated_at,
                r.releases_count, r.primary_language or "", r.merged_pull_requests,
                round(r.closed_issues_percentage, 2),
                r.cbo, r.dit, r.lcom
            ])

        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=ws.max_column):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical="top")

        values = Reference(ws, min_col=2, min_row=2, max_row=ws.max_row)
        cats = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
        chart = BarChart()
        chart.title = "Estrelas por Repositório"
        chart.add_data(values)
        chart.set_categories(cats)
        ws.add_chart(chart, "K2")

        wb.save(file_path)
