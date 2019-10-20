

class UtilsTestFactory(object):

    def given_a_3x3x3_game(self, status='playing'):
        """
        Returns a game with 3 rows, 3 cols and 3 mines.
        All cells not revealed
        :param status:
        :return:
        """
        return {
            "id": "5dacd6539a8b06ed2d956236",
            "status": status,
            "rows": 3,
            "cols": 3,
            "mines": 3,
            "board": [[{"revealed": False, "has_mine": True}, {"revealed": False}, {"revealed": False}],
                      [{"revealed": False}, {"revealed": False, "has_mine": True}, {"revealed": False}],
                      [{"revealed": False}, {"revealed": False}, {"revealed": False, "has_mine": True}]]
        }

    def given_a_won_game(self, status='playing'):
        """
        Returns a game with 3 rows, 3 cols and 3 mines.
        All cells with no mines are revealed.
        :param status:
        :return:
        """
        return {
            "id": "5dacd6539a8b06ed2d956236",
            "status": status,
            "rows": 3,
            "cols": 3,
            "mines": 3,
            "board": [[{"revealed": False, "has_mine": True}, {"revealed": True}, {"revealed": True}],
                      [{"revealed": True}, {"revealed": False, "has_mine": True}, {"revealed": True}],
                      [{"revealed": True}, {"revealed": True}, {"revealed": False, "has_mine": True}]]
        }

    def given_a_3x3x3_game_no_mines(self, status='playing'):
        """
        Returns a game with 3 rows, 3 cols and 3 not placed mines.
        :return:
        """
        return {
            "id": "5dacd6539a8b06ed2d956236",
            "status": status,
            "rows": 3,
            "cols": 3,
            "mines": 3,
            "board": [[{}, {}, {}],
                      [{}, {}, {}],
                      [{}, {}, {}]]
        }
