"""
Ensure stats module loads properly and has some basic components.
"""

from miaguila.stats import increment_stat

class TestStats: # pylint: disable=too-few-public-methods
    """
    Test stats load properly
    """

    @staticmethod
    def test_increment_happy_path():
        """
        Incrementing stats should not fail
        """
        increment_stat('test_statistic')
