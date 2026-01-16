from datetime import datetime
import hashlib

class CalendarExporter:
    def __init__(self):
        pass

    def _generate_uid(self, event_data):
        """
        Generates a deterministic UID for the event.
        UID = hash(student_id + day_of_week + time)
        This ensures that if we update the schedule for the same slot, 
        re-importing the ICS will UPDATE the existing event in the calendar (not duplicate).
        """
        # Unique enough string
        raw_id = f"{event_data.get('student_id', 'user')}_{event_data.get('day_of_week')}_{event_data.get('block_start')}"
        return hashlib.md5(raw_id.encode()).hexdigest() + "@lgszeka.app"

    def _format_datetime(self, date_str, time_str):
        """
        Converts date (YYYY-MM-DD) and time (HH:MM) to ICS format (YYYYMMDDTHHMMSS).
        """
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        return dt.strftime("%Y%m%dT%H%M00")

    def generate_ics(self, schedule_data):
        """
        Generates ICS file content from the schedule data.
        """
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//LGS Zeka//Student Planner//TR",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            "X-WR-CALNAME:LGS Çalışma Programı",
            "X-WR-TIMEZONE:Europe/Istanbul"
        ]

        for item in schedule_data:
            # Skip empty or utility blocks if needed (though breaks might be useful too)
            # For now, let's include everything or just 'etut'? User focused on 'etut'.
            # Let's include everything but make breaks visually distinct.
            
            if not item.get('is_active', True):
                continue
                
            uid = self._generate_uid(item)
            dt_start = self._format_datetime(item['date'], item['block_start'])
            dt_end = self._format_datetime(item['date'], item['block_end'])
            
            summary = item.get('target_desc', 'Etüt')
            if item['block_type'] == 'mola':
                summary = "☕ " + summary
            elif item['block_type'] == 'etut':
                summary = "📚 " + summary
                
            description = f"LGS Çalışma Programı\nBlok: {item['block_type']}\nHedef: {item.get('target_desc')}"

            lines.extend([
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M00Z')}",
                f"DTSTART:{dt_start}",
                f"DTEND:{dt_end}",
                f"SUMMARY:{summary}",
                f"DESCRIPTION:{description}",
                "STATUS:CONFIRMED",
                "SEQUENCE:0",
                "BEGIN:VALARM",
                "TRIGGER:-PT15M",
                "DESCRIPTION:Ders Başlıyor!",
                "ACTION:DISPLAY",
                "END:VALARM",
                "END:VEVENT"
            ])

        lines.append("END:VCALENDAR")
        return "\n".join(lines)
