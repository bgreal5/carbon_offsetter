class Converter:

    def __init__(self):
        """ Class to handle conversions to actionable items """
        pass

    def emission_to_trees(self, emission):
        tree_expected_offset = ((1 - .35) / .35) * ( 48 / 2.205 ) + ( (13.8 + 48) / 2 )
        tree_count = int(emission / tree_expected_offset) + 1
        print("Plant", tree_count, "tree(s) in order to offset your emissions!")
        return tree_count