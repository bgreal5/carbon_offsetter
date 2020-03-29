from argparse import ArgumentParser
from flight import Flight
from converter import Converter

def get_parser():
    parser = ArgumentParser(description='Calcuate carbon emission eq for plane flights.')

    parser.add_argument(
        "places",
        nargs='+',
        type=str,
        help="Your flight path, formatted as a list of airports ordered chronologically",
    )

    parser.add_argument(
        "--flight_class",
        type=str,
        default='economy',
        help="Your flight path, formatted as a list of airports ordered chronologically",
        choices=['economy', 'business', 'first']
    )

    return parser

if __name__ == "__main__":
    args = get_parser().parse_args()
    flight = Flight(args.places, args.flight_class)
    converter = Converter()
    tree_count = converter.emission_to_trees(flight.carbon_eq)
    month_count = converter.emission_to_subscription(flight.carbon_eq)