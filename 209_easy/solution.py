import sys

def get_users():
    with open(sys.argv[1]) as infile:
        num_users = int(infile.readline().strip())
        users = []
        for i in range(num_users):
            user_name, btn_time = infile.readline().strip().split(":")
            btn_time = float(btn_time.strip())
            users.append((btn_time, user_name))
    return users

def main():
    users = get_users()

    BTN_MAX_TIME = 60
    last_reset_time = 0
    for btn_time, user_name in sorted(users):
        time_elapsed = btn_time - last_reset_time
        btn_time_remaining = BTN_MAX_TIME - time_elapsed
        if btn_time_remaining < 0:
            raise SystemError("Button reached 0 seconds!")
        flair_number = int(btn_time_remaining)
        print("%s: %d" % (user_name, flair_number))
        last_reset_time = btn_time

if __name__ == '__main__': main()
