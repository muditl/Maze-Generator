from src.Generator import Generator
from src.Analysis import Analysis
import unittest


class TestGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = Generator(10, 10)

    def test_binary_algorithm(self):
        self.assertTrue(Analysis(self.generator.binary_algorithm()).is_perfect_maze())

    def test_sidewinder(self):
        self.assertTrue(Analysis(self.generator.sidewinder()).is_perfect_maze())

    def test_aldous_broder(self):
        self.assertTrue(Analysis(self.generator.aldous_broder()).is_perfect_maze())

    # def test_wilson(self):
    #     self.assertTrue(Analysis(self.generator.wilson()).is_perfect_maze())

    def test_hunt_and_kill(self):
        self.assertTrue(Analysis(self.generator.hunt_and_kill()).is_perfect_maze())
