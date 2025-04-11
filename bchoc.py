# Main command-line interface (CLI) that parses user commands and calls methods from other modules like 
# blockchain.py, user_auth.py, and encryption.py.

import argparse
import os
from blockchain import Blockchain
from user_auth import verify_password

blockchain = Blockchain()

parser = argparse.ArgumentParser(description='Blockchain Chain of Custody (BCHOC)')
subparsers = parser.add_subparsers(dest='command')

# init
subparsers.add_parser('init')

# verify
subparsers.add_parser('verify')

# add
add_parser = subparsers.add_parser('add')
add_parser.add_argument('-c', '--case_id', required=True)
add_parser.add_argument('-i', '--item_id', nargs='+', required=True)
add_parser.add_argument('-g', '--creator', required=True)
add_parser.add_argument('-p', '--password', required=True)

# checkout
checkout_parser = subparsers.add_parser('checkout')
checkout_parser.add_argument('-i', '--item_id', required=True)
checkout_parser.add_argument('-p', '--password', required=True)

# checkin
checkin_parser = subparsers.add_parser('checkin')
checkin_parser.add_argument('-i', '--item_id', required=True)
checkin_parser.add_argument('-p', '--password', required=True)

# show cases
show_cases_parser = subparsers.add_parser('show')
show_cases_parser.add_argument('type', choices=['cases', 'items', 'history'])
show_cases_parser.add_argument('-c', '--case_id')
show_cases_parser.add_argument('-i', '--item_id')
show_cases_parser.add_argument('-n', '--num_entries', type=int)
show_cases_parser.add_argument('-r', '--reverse', action='store_true')
show_cases_parser.add_argument('-p', '--password', required=True)

# remove
remove_parser = subparsers.add_parser('remove')
remove_parser.add_argument('-i', '--item_id', required=True)
remove_parser.add_argument('-y', '--reason', required=True, choices=['DISPOSED', 'DESTROYED', 'RELEASED'])
remove_parser.add_argument('-p', '--password', required=True)

args = parser.parse_args()

if args.command == 'init':
    blockchain.init()

elif args.command == 'verify':
    blockchain.verify()

elif args.command == 'add':
    if not verify_password(args.password, 'creator', args.creator):
        print("Unauthorized creator password")
    else:
        for item in args.item_id:
            blockchain.add_evidence(args.case_id, item, args.creator)

elif args.command == 'checkout':
    if not verify_password(args.password):
        print("Unauthorized")
    else:
        blockchain.checkout(args.item_id)

elif args.command == 'checkin':
    if not verify_password(args.password):
        print("Unauthorized")
    else:
        blockchain.checkin(args.item_id)

elif args.command == 'show':
    if not verify_password(args.password):
        print("Unauthorized")
    else:
        if args.type == 'cases':
            blockchain.show_cases()
        elif args.type == 'items':
            blockchain.show_items(args.case_id)
        elif args.type == 'history':
            blockchain.show_history(args.case_id, args.item_id, args.num_entries, args.reverse)

elif args.command == 'remove':
    if not verify_password(args.password, 'creator'):
        print("Unauthorized creator password")
    else:
        blockchain.remove_item(args.item_id, args.reason)

else:
    parser.print_help()
