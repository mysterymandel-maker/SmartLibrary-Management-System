from daos.base_dao import BaseDAO

class ClubDAO(BaseDAO):
    def create_club(self, name, description, owner_id):
        query = """
            INSERT INTO book_clubs (name, description, created_by)
            VALUES (%s, %s, %s) RETURNING id
        """
        result = self.execute_query(query, (name, description, owner_id), fetch_one=True)
        return result[0] if result else None

    def add_member(self, club_id, user_id):
        query = "INSERT INTO club_members (club_id, user_id) VALUES (%s, %s)"
        self.execute_query(query, (club_id, user_id))

    def get_all_clubs(self):
        query = """
            SELECT c.id, c.name, c.description, u.username as owner
            FROM book_clubs c
            JOIN users u ON c.created_by = u.id
        """
        return self.execute_query(query, fetch_all=True)

    def get_user_clubs(self, user_id):
         query = """
            SELECT c.id, c.name, c.description
            FROM book_clubs c
            JOIN club_members cm ON c.id = cm.club_id
            WHERE cm.user_id = %s
        """
         return self.execute_query(query, (user_id,), fetch_all=True)
    
    def delete_club(self, club_id):
        """Delete a club and all its memberships"""
        # First delete all memberships
        query1 = "DELETE FROM club_members WHERE club_id = %s"
        self.execute_query(query1, (club_id,))
        
        # Then delete the club
        query2 = "DELETE FROM book_clubs WHERE id = %s"
        self.execute_query(query2, (club_id,))
        return True
