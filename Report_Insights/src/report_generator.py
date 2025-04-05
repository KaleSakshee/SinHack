# src/report_generator.py

def generate_report(system_info):
    """
    This function generates a system health report from the provided system info.
    :param system_info: A dictionary containing system health information.
    :return: A formatted report string.
    """
    report = f"System Health Report:\n"
    report += f"CPU Usage: {system_info['cpu']}%\n"
    report += f"Memory Usage: {system_info['memory']}%\n"
    report += f"Disk Usage: {system_info['disk']}%\n"
    return report
