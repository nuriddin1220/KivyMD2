def format_duration(duration_sec):
    minutes, remaining_seconds = divmod(duration_sec, 60)
    hours, remaining_minutes = divmod(minutes, 60)
    duration = ""
    if hours > 0:
        duration += f"{hours} hour{'s' if hours > 1 else ''}, "
    if remaining_minutes > 0:
        duration += f"{remaining_minutes} minute{'s' if remaining_minutes > 1 else ''}, "
    if remaining_seconds > 0:
        duration += f"{remaining_seconds} second{'s' if remaining_seconds > 1 else ''}"
    return duration.rstrip(", ")

print(format_duration(3586))