import cmd
import shlex
import cowsay

class CowShlex(cmd.Cmd):
    prompt = '>>> '
    
    def do_EOF(self, args):
        return True

    def do_list_cows(self, args):
        """Lists all cow file names in the given directory"""
        print(cowsay.list_cows())

    def do_make_bubble(self, text="Hello world!"):
        """
        Wraps text, then pads text and sets inside a bubble.
        This is the text that appears above the cows
        """
        print(cowsay.make_bubble(text))

    def do_cowsay(self, args):
        """
        Similar to the cowsay command. Parameters are listed with their
        corresponding options in the cowsay command. Returns the resulting cowsay
        string

        :param message: The message to be displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        """
        shlexed_args = shlex.split(args)
        if len(shlexed_args) != 4:
            print('Invalid argumets')
        else:
            msg = 'Hello world!'
            msg, cow, eye, tongue = shlexed_args
            print(cowsay.cowsay(message=msg, cow=cow, eyes=eye, tongue=tongue))

    def do_cowthink(self, args):
        """
        Similar to the cowthink command. Parameters are listed with their
        corresponding options in the cowthink command. Returns the resulting
        cowthink string
        
        :param message: The message to be displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        """
        shlexed_args = shlex.split(args)
        if len(shlexed_args) != 4:
            print('Invalid argumets')
        else:
            msg = 'Hello world!'
            msg, cow, eye, tongue = shlex.split(args)
            print(cowsay.cowthink(message=msg, cow=cow, eyes=eye, tongue=tongue))


if __name__ == '__main__':
    CowShlex().cmdloop()
