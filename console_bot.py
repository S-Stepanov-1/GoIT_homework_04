from user_error import AddError, ChangeError, CommandError, ShowError

phone_book = {}


def input_error(function):
    def inner(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyError:
            return "The requested contact was not found in the phone book."
        except TypeError:
            return "Give me name and phone please."
        except AddError:
            return f"{args[0]} is already exist in phone book."
        except ChangeError:
            return f"'{args[0]}' isn't in phone book."
        except CommandError:
            return "Enter correct command please."
        except ShowError:
            return "The phone book is empty."

    return inner


@input_error
def greeting():
    return "How can I help you?"


@input_error
def add_to_book(name, phone):
    if name not in phone_book:
        phone_book[name] = phone
        return f"'{name}' with the phone number '{phone}' was added to phone book"
    raise AddError


@input_error
def change_number(name, phone):
    if phone_book[name]:
        phone_book[name] = phone
        return f"The phone number for contact {name} has been changed to {phone}."
    raise ChangeError


@input_error
def give_phone_number(name):
    return f"{name}: {phone_book[name]}"


@input_error
def show_all():
    if len(phone_book) > 0:
        output = ""
        for name, phone in phone_book.items():
            output += f"{name}: {phone}\n"
        return output.strip()
    raise ShowError


@input_error
def say_good_bye():
    return "Good bye!"


@input_error
def delete_number(name):
    del phone_book[name]
    return f"{name} was deleted."


@input_error
def get_handler(user_input):
    user_input = user_input

    if user_input.lower() in ("hello", "show all", "good bye", "close", "exit"):
        return BOT_OPERATIONS[user_input]()

    user_input = user_input.split()
    command = user_input[0].lower()

    if command in BOT_OPERATIONS.keys():
        return BOT_OPERATIONS[command](*user_input[1:])
    raise CommandError


def main():
    while True:
        user_input = input("> ")
        handler = get_handler(user_input)
        print(handler)

        if handler == "Good bye!":
            exit()


BOT_OPERATIONS = {
    "hello": greeting,
    "show all": show_all,
    "good bye": say_good_bye,
    "close": say_good_bye,
    "exit": say_good_bye,
    "add": add_to_book,
    "change": change_number,
    "phone": give_phone_number,
    "delete": delete_number,
}

if __name__ == '__main__':
    main()
