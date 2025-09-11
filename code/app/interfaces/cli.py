import os
from pathlib import Path
from app.infrastructure.graphql.github_gateway import GitHubGateway
from app.infrastructure.reports.excel_report_generator import ExcelReportGenerator
from app.core.use_cases.list_popular_repos import ListPopularRepos
from app.infrastructure.analysis.ck_analyzer import CkAnalyzer
from app.infrastructure.git.git_cloner import GitCloner

def get_downloads_path() -> Path:
    downloads = Path.home() / "Downloads"
    return downloads if downloads.exists() else Path.home()


def run_cli():
    print("=== RELATÓRIOS ===")
    print("1) Repositórios populares (Java)")
    choice = input("Escolha: ").strip()
    if choice == "1":
        ck_jar_path = "ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"
        if not os.path.exists(ck_jar_path):
            print(f"Erro: {ck_jar_path} não encontrado.")
            return

        n = int(input("Quantos repositórios (max 1000): ").strip() or "10")
        dest = get_downloads_path() / f"relatorio_populares_{n}.xlsx"

        use_case = ListPopularRepos(
            github_gateway=GitHubGateway(),
            report_generator=ExcelReportGenerator(),
            cloner=GitCloner(),
            analyzer=CkAnalyzer(ck_jar_path)
        )
        path = use_case.execute(n, str(dest))
        print(f"Relatório gerado em: {path}")
