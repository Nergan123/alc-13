from alice import Alice
import logging
import os


def main():
    alice = Alice('en')
    alice.run()


if __name__ == '__main__':
    if not os.path.isdir('alice_logs'):
        os.makedirs('alice_logs')

    logging.basicConfig(
        filename='alice_logs/alice.log',
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s [%(name)s]: %(levelname)s: %(message)s'
    )
    main()
