import os
from app.infrastructure.config.settings import Settings
from app.infrastructure.graphql.github_gateway import GithubGateway
from app.infrastructure.git.git_cloner import GitCloner
from app.infrastructure.analysis.ck_analyzer import CkAnalyzer
from app.infrastructure.reports.excel_report_generator import ExcelReportGenerator
from app.core.use_cases.analyze_repositories import AnalyzeRepositories

def main():
    if not Settings.GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN not found in .env file or settings.")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    REPO_COUNT = int(os.getenv("REPO_COUNT", "1000"))
    TEMP_CLONE_PATH = os.path.join(BASE_DIR, "temp_repos")
    CK_JAR_PATH = os.path.join(BASE_DIR, "ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar")
    CK_OUTPUT_DIR = os.path.join(BASE_DIR, "ck_output")
    FINAL_REPORT_PATH = os.path.join(BASE_DIR, "analysis_report.xlsx")
    
    if not os.path.exists(CK_JAR_PATH):
        raise FileNotFoundError(f"CK JAR not found at: {CK_JAR_PATH}")

    github_gateway = GithubGateway()
    git_cloner = GitCloner()
    ck_analyzer = CkAnalyzer(ck_jar_path=CK_JAR_PATH, output_dir=CK_OUTPUT_DIR)
    report_generator = ExcelReportGenerator()

    analyze_use_case = AnalyzeRepositories(
        repository_gateway=github_gateway,
        repository_cloner=git_cloner,
        static_analyzer=ck_analyzer,
    )

    print(f"Starting analysis of {REPO_COUNT} repositories...")
    analyzed_repositories = analyze_use_case.execute(REPO_COUNT, TEMP_CLONE_PATH)
    
    if analyzed_repositories:
        print(f"Analysis complete. Generating report for {len(analyzed_repositories)} repositories...")
        report_generator.generate(analyzed_repositories, FINAL_REPORT_PATH)
        print(f"Report successfully generated at: {FINAL_REPORT_PATH}")
    else:
        print("No repositories were analyzed. Report not generated.")

if __name__ == "__main__":
    main()