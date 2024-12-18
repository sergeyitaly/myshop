import logging
from urllib.parse import unquote
from django.utils.timezone import now
from .models import TeamMember
from logs.models import APILog

logger = logging.getLogger('team')


class TeamMemberLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.log_team_member_click(request)
        response = self.get_response(request)
        return response

    def log_team_member_click(self, request):
        path = unquote(request.path)
        team_member, link_type, clicked_link = self.get_team_member_and_link(path)

        if team_member and clicked_link:
            logger.info(f"Team Member: {team_member}, Link Type: {link_type}, Link: {clicked_link}")
            self.log_to_database(clicked_link)

    def get_team_member_and_link(self, path):
        try:
            if 'team_member' in path:
                team_member_id = path.split('/')[-2]  # Adjust this based on your URL structure
                team_member = TeamMember.objects.get(id=team_member_id)
                if 'linkedin' in path:
                    return team_member, 'LinkedIn', team_member.linkedin
                elif 'github' in path:
                    return team_member, 'GitHub', team_member.github
                elif 'behance' in path:
                    return team_member, 'Behance', team_member.behance
                elif 'telegram' in path:
                    return team_member, 'Telegram', team_member.link_to_telegram

        except TeamMember.DoesNotExist:
            logger.warning(f"No TeamMember found for path: {path}")
        except Exception as e:
            logger.error(f"Error while processing path {path}: {e}")

        return None, None, None

    def log_to_database(self, clicked_link):
        try:
            APILog.objects.create(
                endpoint=clicked_link,
                request_count=1,
                timestamp=now()
            )
            logger.info(f"Successfully logged link: {clicked_link} to the database.")
        except Exception as e:
            logger.error(f"Failed to log clicked link to the database: {e}")
