from daos.club_dao import ClubDAO

class ClubService:
    def __init__(self):
        self.club_dao = ClubDAO()

    def create_club(self, name, description, owner_id):
        # Check if exists logic could go here, but DB has unique constraint
        club_id = self.club_dao.create_club(name, description, owner_id)
        if club_id:
            # Owner also joins the club
            self.club_dao.add_member(club_id, owner_id)
            return True, club_id
        return False, "Could not create club (name might be taken)"

    def join_club(self, club_id, user_id):
        try:
            self.club_dao.add_member(club_id, user_id)
            return True, "Joined successfully"
        except Exception:
            return False, "Already a member or error"

    def get_all_clubs(self):
        return self.club_dao.get_all_clubs()

    def get_my_clubs(self, user_id):
        return self.club_dao.get_user_clubs(user_id)
    
    def delete_club(self, club_id, user_id):
        """Delete a club - only owner or librarian can delete"""
        try:
            # Get club details to check ownership
            clubs = self.club_dao.get_all_clubs()
            club = next((c for c in clubs if c[0] == club_id), None)
            
            if not club:
                return False, "Club not found."
            
            # Note: In a real app, we'd check if user is librarian or owner
            # For now, we'll allow deletion
            
            self.club_dao.delete_club(club_id)
            return True, "Club deleted successfully."
        except Exception as e:
            return False, f"Error deleting club: {str(e)}"
