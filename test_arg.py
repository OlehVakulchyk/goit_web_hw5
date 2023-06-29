import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number",
                    type=int, choices=[1,2,3,4,5,6,7,8,9,10])
parser.add_argument('foo', action='append', default=['eur', 'usd'])
parser.add_argument('-bar', action='extend', default=['eur', 'usd'], nargs="+", type=str)
args = parser.parse_args()
print(args.foo)
print(args.bar)
print(args.square**2)