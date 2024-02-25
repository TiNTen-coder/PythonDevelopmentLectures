import argparse
import cowsay

cow_pars = argparse.ArgumentParser()

cow_pars.add_argument('-e', '--eyes', default='oo', help='choose cow eyes')
cow_pars.add_argument('-f', '--file', default='default')
cow_pars.add_argument('-l', '--list', action='store_true')
cow_pars.add_argument('-n', '--nspace', action='store_false')
cow_pars.add_argument('-t', '--tongue', default='', help='tongue')
cow_pars.add_argument('-c', '--character', default='default', help='choose cow')
cow_pars.add_argument('message', default='', nargs='*', help='what to say')

cow_args = cow_pars.parse_args()
if cow_args.list:
    print(cowsay.list_cows())
else:
    print(cowsay.cowsay(cow_args.message, cow=cow_args.character, tongue=cow_args.tongue, eyes=cow_args.eyes))
