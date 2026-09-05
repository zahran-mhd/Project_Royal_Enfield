# from line_regulation_report import LineRegulationReport

# report = LineRegulationReport(
#     report_folder="Report"
# )

# report_path = report.start_report(
#     test_name="OBC_Line_Regulation"
# )

# print(
#     "REPORT GENERATED:",
#     report_path
# )



from loadRegulationReport import LoadRegulationReport

report = LoadRegulationReport(
    report_folder="Report"
)

report_path = report.start_report(
    test_name="Load_Regulation"
)

print(
    "REPORT GENERATED:",
    report_path
)
