import csv
import random
import re
class Node:
    def __init__(self, row):
        props = ['name', 'wanted', 'not wanted', 'gift types', 'address', 'misc']
        self.props = {}
        elements = len(row)
        # cut timestamp
        for i in range(1, len(row)):
            prop = props[i - 1]
            self.props[prop] = row[i]

    def __repr__(self):
        # string_rep = ''
        # for prop, val in self.props.iteritems():
        #     string_rep += prop + ": " + val + "\n"
        # string_rep += "\n"

        string_rep = self.props['name'] + " "
        if hasattr(self, 'cheer_receiver'):     
            string_rep += "is cheering " + self.cheer_receiver.get_name()
        string_rep += "\n"
        return string_rep

    def set_cheer_receiver(self, name):
        self.cheer_receiver = name

    def get_name(self):
        return self.props['name']

    def get_wants(self):
        return self.props['wanted']

    def get_not_wanted(self):
        return self.props['not wanted']

    def get_gift_types(self):
        return self.props['gift types']

    def get_address(self):
        return self.props['address']

    def get_misc(self):
        return self.props['misc']    

    def check_cheer_prop(self, prop):
        if hasattr(self, 'cheer_receiver'):
            return prop
        else:
            return None

    def receiver_address(self):
        return self.check_cheer_prop(self.cheer_receiver.get_address())

    def receiver_wants(self):
        return self.check_cheer_prop(self.cheer_receiver.get_wants())

    def receiver_gift_types(self):
        return self.check_cheer_prop(self.cheer_receiver.get_gift_types())

    def receiver_not_wanted(self):
        return self.check_cheer_prop(self.cheer_receiver.get_not_wanted())

    def receiver_misc(self):
        return self.check_cheer_prop(self.cheer_receiver.get_misc())

    def receiver_name(self):
        return self.check_cheer_prop(self.cheer_receiver.get_name())

def main():
    peeps = make_train()
    # shuffle train
    random.shuffle(peeps)
    # verify everyone's there!
    print peeps

    set_cheerleaders(peeps)
    # verify the cheer
    print peeps
    write_love_letters(peeps)

def set_cheerleaders(peeps):
    num_peeps = len(peeps)
    for i in range(num_peeps - 1):
        peep = peeps[i]
        peep.set_cheer_receiver(peeps[i + 1])

    peeps[num_peeps - 1].set_cheer_receiver(peeps[0])

def make_train():
    peeps = []
    with open('names.csv') as f:
        f = csv.reader(f)
        # strip first row, just headers
        f.next()
        for row in f:
            peeps.append(Node(row))
    return peeps

def write_love_letters(peeps):
    for peep in peeps:
        peep_file_name = clean_name(peep.get_name()) + "_cheer_train.txt"
        with(open('assignments/' + peep_file_name, "w+")) as output:
            letter = ''
            me = peep.get_name()
            them = peep.receiver_name() 
            lines = [
                'Dearest ' + me + ',' ,
                '',
                'Thank you for boarding the cheer train! We hope you enjoy your ride!',
                '',
                'This season, please spread some holiday cheer to ' + them + '. ' + them + " requests:",
                '',
                peep.receiver_wants(),
            ]
            dislikes = peep.receiver_not_wanted()
            if has_alpha(dislikes):
                lines += [
                    '',
                    them + ' does *not* desire:',
                    '',
                    dislikes,
                    '', 
                    ':)',
                ]
            lines += [
                '',
                them + ' will humbly accept gifts of any of these forms:',
                peep.receiver_gift_types(),
            ]
            addy = peep.receiver_address().strip()
            if has_alpha(addy):
                lines += [
                    '',
                    'should you choose to gift a treasure of physical form, ' + them + ' can be found at: ',
                    addy,
                ]
            misc = peep.receiver_misc()
            if has_alpha(misc):
                lines += [
                    '',
                    'ps: a message from the legend themselves:',
                     misc,
                ]
            s = '\n'
            letter = s.join(lines)
            output.write(letter)


def has_alpha(word):
    for x in word:
        if x.isalpha():
            return True
    return False

def clean_name(name):
    output = ''
    for symbol in name:
        if symbol == '/':
            output += ' also known as '
        else:
            output += symbol
    return output

if __name__ == '__main__':
    main()