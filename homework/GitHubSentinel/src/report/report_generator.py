# src/report/report_generator.py

class ReportGenerator:
    def generate_report(self, updates):
        report = "GitHub Sentinel Report\n\n"
        for repo, commits in updates.items():
            report += f"Repository: {repo}\n"
            for commit in commits:
                report += f"- {commit['commit']['message']}\n"
            report += "\n"
        return report
