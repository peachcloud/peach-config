import subprocess

if __name__ == '__main__':
    print("peach-img test message")
    with open("/srv/test_file_write.txt", 'w') as f:
        f.write("peach image test file write")

    # test download
    subprocess.call(["wget", "-O", "/srv/pubkey.gpg", "http://apt.peachcloud.org/pubkey.gpg"])

    # test apt-get install
    subprocess.call(["apt-get", "install", "-y", "nginx"])