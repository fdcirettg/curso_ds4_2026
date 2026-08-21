""" Calculate the area of a rectangle given its length and width. """
import argparse
def calculate_rectangle_area(length:float, width:float) -> float:
    """Calculate the area of a rectangle.
    Returns:
        float: The area of the rectangle.
    """
    return length * width

def main():
    """Main function to parse command line arguments and calculate the area."""
    parser = argparse.ArgumentParser(description="Calculate the area of a rectangle.")
    parser.add_argument("-l", "--length",
                        default=10.0, type=float, help="The length of the rectangle.")
    parser.add_argument("-w", "--width", default=5.0,
                         type=float, help="The width of the rectangle.")
    args = parser.parse_args()

    area = calculate_rectangle_area(args.length, args.width)
    print(f"The area of the rectangle is: {area}")

if __name__ == "__main__":
    main()
